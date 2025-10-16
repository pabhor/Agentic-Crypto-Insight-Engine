# check_models.py
import os
from pathlib import Path

# Path to your local models directory in the project
llm_dir = Path("models/llm")

if not llm_dir.exists():
    print(f"❌ LLM directory not found at {llm_dir.resolve()}")
else:
    print(f"✅ LLM directory found at {llm_dir.resolve()}")
    # List all subdirectories/files (each subfolder is a model)
    for model_folder in llm_dir.iterdir():
        if model_folder.is_dir():
            # Calculate folder size in GB
            total_size = sum(f.stat().st_size for f in model_folder.glob("**/*") if f.is_file())
            size_gb = total_size / (1024**3)
            print(f"Model: {model_folder.name} | Size: {size_gb:.2f} GB")
