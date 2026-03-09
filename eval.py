"""Run the 5 test prompts through the FINE-TUNED model and compare with baseline."""

import json
from mlx_lm import load, generate

MODEL = "mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit"
ADAPTER_PATH = "adapters"

def load_test_prompts(path="data/test.jsonl"):
    prompts = []
    with open(path) as f:
        for line in f:
            item = json.loads(line)
            user_msg = item["messages"][0]["content"]
            expected = item["messages"][1]["content"]
            prompts.append({"prompt": user_msg, "expected": expected})
    return prompts

def similarity_score(expected, actual):
    """Simple line-by-line similarity as a rough metric."""
    exp_lines = set(expected.strip().splitlines())
    act_lines = set(actual.strip().splitlines())
    if not exp_lines:
        return 0.0
    return len(exp_lines & act_lines) / len(exp_lines) * 100

def main():
    print("Loading fine-tuned model...")
    model, tokenizer = load(MODEL, adapter_path=ADAPTER_PATH)
    print(f"Model loaded with adapter: {ADAPTER_PATH}\n")

    prompts = load_test_prompts()

    # Load baseline results
    try:
        with open("results/baseline.json") as f:
            baseline = json.load(f)
    except FileNotFoundError:
        baseline = None
        print("No baseline found. Run baseline_test.py first for comparison.\n")

    results = []
    total_baseline_score = 0
    total_finetuned_score = 0

    for i, p in enumerate(prompts):
        messages = [{"role": "user", "content": p["prompt"]}]
        prompt_text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        output = generate(
            model, tokenizer, prompt=prompt_text, max_tokens=1024, verbose=False
        )

        ft_score = similarity_score(p["expected"], output)
        total_finetuned_score += ft_score

        print(f"\n{'='*60}")
        print(f"TEST {i+1}")
        print(f"{'='*60}")
        print(f"PROMPT: {p['prompt'][:80]}...")
        print(f"\nEXPECTED:\n{p['expected'][:300]}")
        print(f"\nFINE-TUNED OUTPUT:\n{output[:300]}")
        print(f"\nFine-tuned similarity: {ft_score:.1f}%")

        if baseline:
            bl_score = similarity_score(p["expected"], baseline[i]["baseline_output"])
            total_baseline_score += bl_score
            print(f"Baseline similarity:   {bl_score:.1f}%")
            print(f"Improvement:           {ft_score - bl_score:+.1f}%")

        results.append({
            "test_id": i + 1,
            "expected": p["expected"],
            "finetuned_output": output,
            "finetuned_score": ft_score,
        })

    n = len(prompts)
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Average fine-tuned similarity: {total_finetuned_score/n:.1f}%")
    if baseline:
        print(f"Average baseline similarity:   {total_baseline_score/n:.1f}%")
        print(f"Average improvement:           {(total_finetuned_score-total_baseline_score)/n:+.1f}%")

    with open("results/finetuned.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/finetuned.json")

if __name__ == "__main__":
    main()
