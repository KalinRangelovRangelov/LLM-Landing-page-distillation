"""Run the 5 test prompts through the UNTRAINED base model to get a baseline."""

import json
from mlx_lm import load, generate

MODEL = "mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit"

def load_test_prompts(path="data/test.jsonl"):
    prompts = []
    with open(path) as f:
        for line in f:
            item = json.loads(line)
            user_msg = item["messages"][0]["content"]
            expected = item["messages"][1]["content"]
            prompts.append({"prompt": user_msg, "expected": expected})
    return prompts

def run_baseline(prompts, model, tokenizer):
    results = []
    for i, p in enumerate(prompts):
        messages = [{"role": "user", "content": p["prompt"]}]
        prompt_text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        output = generate(
            model, tokenizer, prompt=prompt_text, max_tokens=1024, verbose=False
        )
        results.append({
            "test_id": i + 1,
            "prompt": p["prompt"],
            "expected": p["expected"],
            "baseline_output": output,
        })
        print(f"\n{'='*60}")
        print(f"TEST {i+1}")
        print(f"{'='*60}")
        print(f"PROMPT: {p['prompt'][:80]}...")
        print(f"\nEXPECTED (first 200 chars):\n{p['expected'][:200]}")
        print(f"\nBASELINE OUTPUT (first 200 chars):\n{output[:200]}")
    return results

def main():
    print("Loading model (this may download ~1GB on first run)...")
    model, tokenizer = load(MODEL)
    print(f"Model loaded: {MODEL}\n")

    prompts = load_test_prompts()
    print(f"Loaded {len(prompts)} test prompts\n")

    results = run_baseline(prompts, model, tokenizer)

    with open("results/baseline.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n\nBaseline results saved to results/baseline.json")

if __name__ == "__main__":
    main()
