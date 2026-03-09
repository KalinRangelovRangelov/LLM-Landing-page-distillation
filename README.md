# Landing Page Generator — Knowledge Distillation Experiment

A hands-on experiment in **knowledge distillation**: training a tiny 1.5B parameter model to generate landing pages by learning from a much larger model's outputs.

## Inspiration

This experiment was inspired by [Bijan Bowen](https://www.youtube.com/@BijanBowen)'s excellent video ["How DeepSeek 'Stole' Claude – Real Distillation Attack Demo"](https://www.youtube.com/watch?v=ase1Qmyo4Wg), which provides a great explanation of what LLM distillation is and how it works in practice.

## The Idea

Can a small model (1.5B params, runs on a laptop) learn to generate beautiful landing pages by studying examples from a large model (685B params, cloud API)?

**Spoiler: Yes.** And the difference between 50 and 500 training examples is dramatic.

## Lessons Learned Along the Way

Our first attempt used a template-based script (`generate_data.py`) that generated 50 training pages by filling in HTML templates with different business names and colors — but the **layout was always the same**. The model learned to produce landing pages, and the improvement over baseline was clearly visible, but the results were mediocre: every output had the same structure, same section order, same design pattern. The model had memorized one layout instead of learning how to build pages.

This taught us that **training data diversity matters as much as quantity**. We switched to `generate_with_deepseek.py`, which uses DeepSeek V3 to create truly diverse pages — varying hero styles, color schemes, navigation patterns, grid layouts, animations, and more. The jump in output quality was immediate.

## How It Works

```
DeepSeek V3 (685B)                    Qwen2.5-Coder (1.5B)
Large "teacher" model                 Small "student" model
        │                                      │
        │ Generate 1000                        │ Learn from
        │ diverse landing pages                │ those examples
        ▼                                      ▼
  Training Data (JSONL)  ──── LoRA ────►  Fine-tuned Model
  prompt → HTML pairs         Training     Runs locally, no API
```

1. **Generate training data** — Ask DeepSeek V3 to create 1000 landing pages across 100 business types, 10 design styles, and 10 layout variations (~$2 in API costs)

<details>
<summary>All 100 business types used in training</summary>

spacecraft manufacturer, semiconductor chip fab, luxury cosmetic salon, defense contractor, elite private school, specialty coffee roastery, veterinary clinic, fintech payment platform, architecture firm, drone delivery startup, yoga studio, cybersecurity firm, space tourism company, organic farm, luxury watch brand, electric vehicle startup, music streaming app, corporate law firm, meal prep delivery service, cloud hosting provider, dental practice, mobile pet grooming service, language learning app, wedding photography studio, moving company, meditation app, surf school, AI research lab, craft brewery, private jet charter, rock climbing gym, botanical garden, 3D printing company, wine vineyard, video game studio, solar energy installer, ski resort, personal trainer platform, escape room venue, book publisher, co-working space, marine biology institute, tattoo studio, children's museum, luxury hotel, robotics company, perfume house, mountain bike park, podcast hosting platform, vintage record store, sushi restaurant, quantum computing startup, dog walking service, Formula 1 racing team, independent bookshop, scuba diving school, artisan bakery, electric bike shop, interior design studio, pet adoption agency, classical music orchestra, food truck collective, sustainable fashion brand, art gallery, coworking cafe, sleep clinic, adventure travel agency, leather goods workshop, aquarium, helicopter tour company, cheese shop, boxing gym, piano tuning service, mushroom farm, ice cream parlor, antique shop, board game cafe, flower delivery service, martial arts dojo, ballet school, VR arcade, custom shoe maker, candle company, astronomy observatory, food bank charity, dating app, genealogy service, haunted house attraction, puzzle company, tiny house builder, hot air balloon rides, ceramics studio, whiskey distillery, cat cafe, drone racing league, bonsai nursery, escape boat experience, rooftop bar, knife sharpening service, beekeeping supplies
</details>

2. **Fine-tune with LoRA** — Train only 0.3% of the small model's weights (5.3M out of 1.5B parameters) on Apple Silicon using MLX
3. **Deploy locally** — Fuse the adapter, quantize, and run via Ollama — no cloud, no API key needed

## Results

We trained 3 models with different amounts of data to see how quantity affects quality:

### Training Loss Comparison

| Model | Training Examples | Best Val Loss | Improvement |
|-------|------------------|---------------|-------------|
| Baseline (no training) | 0 | 0.693 | — |
| `landing-sm` | 50 | 0.353 | 49% |
| `landing-md` | 500 | 0.218 | 69% |

### Quantization Impact

Same model (500 examples), different precision:

| Variant | Precision | Size | Bits/Weight |
|---------|-----------|------|-------------|
| `landing-md` | FP16 | 3.1 GB | 16.0 |
| `landing-md:q8` | Q8_0 | 1.6 GB | 8.5 |
| `landing-md:q4` | Q4_K_M | 986 MB | 5.1 |

Q8 and Q4 produce nearly identical results for this model size. FP16 is noticeably better.

### Example Outputs

All generated from the same prompt: *"Create a landing page for a vintage vinyl record subscription box called CrateDigger"*

| Stage | Output |
|-------|--------|
| [Baseline](results/examples/baseline/) | Untrained model — outputs generic/broken HTML |
| [After 50 examples](results/examples/after50/) | Basic structure, simple styling |
| [After 500 examples](results/examples/after500/) | Full landing page with sections, gradients, responsive design |
| [After 500 (Q8)](results/examples/after500-q8/) | Quantized — nearly identical to FP16 |
| [After 500 (Q4)](results/examples/after500-q4/) | Aggressively quantized — still good |
| [Claude reference](results/examples/claude/) | What a frontier model produces |

## Project Structure

```
├── generate_with_deepseek.py   # Data generation via DeepSeek API
├── lora_config_sm.yaml         # Training config — 50 examples, 200 iters
├── lora_config_md.yaml         # Training config — 500 examples, 600 iters
├── baseline_test.py            # Run test prompts on untrained model
├── eval.py                     # Evaluate fine-tuned model
├── results/examples/           # HTML outputs at each stage
│   ├── baseline/               # Untrained model output
│   ├── after50/                # 50 training examples
│   ├── after500/               # 500 training examples (FP16)
│   ├── after500-q8/            # 500 examples, Q8 quantized
│   ├── after500-q4/            # 500 examples, Q4 quantized
│   ├── claude/                 # Claude output for comparison
│   └── claude-fed/             # Claude with guided prompt
└── .gitignore
```

Models and datasets are on Hugging Face (too large for GitHub):
- Models: *[link TBD]*
- Dataset: *[link TBD]*

## Reproduce It Yourself

### Prerequisites

- Apple Silicon Mac (M1/M2/M3/M4, 16GB+ RAM) or CUDA GPU
- Python 3.10+
- [Ollama](https://ollama.com) installed

### 1. Install dependencies

```bash
pip install mlx-lm openai
brew install llama.cpp  # for quantization
```

### 2. Generate training data

```bash
export DEEPSEEK_API_KEY="your-key-here"
python generate_with_deepseek.py
```

This creates `data_sm/`, `data_md/`, `data_lg/` directories with train/valid/test splits.

### 3. Train

```bash
# Small model (50 examples, ~10 min)
python -m mlx_lm lora -c lora_config_sm.yaml

# Medium model (500 examples, ~60 min)
python -m mlx_lm lora -c lora_config_md.yaml
```

### 4. Fuse and deploy

```bash
# Fuse LoRA adapter into base model
python -m mlx_lm fuse \
  --model mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit \
  --adapter-path adapters_md \
  --de-quantize \
  --save-path fused_md

# Convert to GGUF and quantize
python /opt/homebrew/Cellar/llama.cpp/*/bin/convert_hf_to_gguf.py fused_md --outfile fused_md/model-f16.gguf --outtype f16
llama-quantize fused_md/model-f16.gguf fused_md/model-q8.gguf Q8_0
llama-quantize fused_md/model-f16.gguf fused_md/model-q4.gguf Q4_K_M

# Import to Ollama
ollama create landing-md -f fused_md/Modelfile
```

### 5. Generate

```bash
ollama run landing-md "Create a landing page for a space tourism company called Orbit Adventures"
```

## Key Takeaways

- **50 examples** are enough to teach a model the basic task format
- **500 examples** produce significantly better quality — more diverse layouts, better CSS, proper responsive design
- **Quantization** (Q8, Q4) barely affects output quality for 1.5B models — you can shrink the model 3x with minimal loss
- **LoRA** makes fine-tuning accessible — training only touches 0.3% of weights and runs on a MacBook in under an hour
- **The cost**: ~$2 in API calls + electricity for training. The student model then runs forever for free

## Tech Stack

- **Teacher model**: DeepSeek V3 (685B parameters, via API)
- **Student model**: [Qwen2.5-Coder-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct) (4-bit quantized)
- **Training**: [MLX](https://github.com/ml-explore/mlx) with LoRA on Apple Silicon
- **Quantization**: [llama.cpp](https://github.com/ggerganov/llama.cpp)
- **Inference**: [Ollama](https://ollama.com)

## License

MIT
