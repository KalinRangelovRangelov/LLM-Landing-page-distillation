"""Fine-tune Qwen2.5-Coder-1.5B with LoRA on CSS beautification using MLX."""

import subprocess
import sys

MODEL = "mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit"
ADAPTER_PATH = "adapters"
TRAIN_DATA = "data/train.jsonl"
TEST_DATA = "data/test.jsonl"

# LoRA training config
ITERS = 200        # training iterations (50 examples * ~4 epochs)
BATCH_SIZE = 1     # keep small for memory
LORA_RANK = 16     # rank of LoRA matrices
LEARNING_RATE = 1e-4

cmd = [
    sys.executable, "-m", "mlx_lm.lora",
    "--model", MODEL,
    "--train",
    "--data", "data",
    "--adapter-path", ADAPTER_PATH,
    "--iters", str(ITERS),
    "--batch-size", str(BATCH_SIZE),
    "--lora-rank", str(LORA_RANK),
    "--learning-rate", str(LEARNING_RATE),
]

print(f"Starting LoRA fine-tuning...")
print(f"  Model:         {MODEL}")
print(f"  Iterations:    {ITERS}")
print(f"  LoRA rank:     {LORA_RANK}")
print(f"  Learning rate: {LEARNING_RATE}")
print(f"  Adapter path:  {ADAPTER_PATH}")
print()

subprocess.run(cmd)
