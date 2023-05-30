import os

import yaml

config_path = os.path.join(os.path.expanduser("~"), ".git_llm_config.yaml")

MODEL_TYPES = {
    "OPENAI": "openai",
    "LOCAL": "local",
}

DEFAULT_CONFIG = {
    "max_tokens": "1048",
    "model_name": "gpt-3.5-turbo",
    "model_path": "models/ggml-gpt4all-j-v1.3-groovy.bin",
    "model_type": MODEL_TYPES["OPENAI"],
    "chunk_size": 4000,
    "chunk_overlap": 200,
}


def save_config(config):
    print(f"🤖 Saving config to {config_path}")
    with open(config_path, "w") as f:
        yaml.dump(config, f)


def get_config():
    print(f"🤖 Loaded config from {config_path}")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = DEFAULT_CONFIG
        save_config(config)
    return config
