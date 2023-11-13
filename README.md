## git-llm

The project integrates Git with a llm (OpenAI, LlamaCpp, and GPT-4-All) to extend the capabilities of git. It supports
offline processing using [GPT4All](https://github.com/nomic-ai/gpt4all) without sharing your code with third parties, or
you can use OpenAI if privacy is not a concern for you. It is only recommended for educational purposes and not for
production use.

### Installation

To install `git-llm`, you need to have Python 3.9 and an OpenAI API
key [api-keys](https://platform.openai.com/account/api-keys). Additionally, if you want to use the GPT4All model, you
need to download the [ggml-gpt4all-j-v1.3-groovy.bin](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin) model.
If you prefer a different model, you can download it from [GPT4All](https://gpt4all.io) and configure path to it in the
configuration and specify its path in the configuration. If you want some files to be ignored, add them to .gitignore.
Alternatively you could point to an [Ollama](https://ollama.ai/) server.

To install `git-llm`, run the following command in your terminal:

```bash
pip install git-llm
```

### Usage

To use `git-llm`, you need to configure it first. To do this, run the following command:

```bash
git-llm config
```

Use a llm to generate a list of changes, then review the staged changes using `git diff --staged`.

```bash
git-llm changelog
```

Use a llm to generate a commit message following the Conventional format, then review the staged changes
using `git diff --staged`.

```bash
git-llm commit
```

You can also edit the configuration manually by editing the `~/.git_llm_config.yaml` file. If for some reason you cannot
find the configuration file, just run the tool and at the very beginning it will output the path to the configuration
file.

```yaml
# The OpenAI API key. You can get it from https://beta.openai.com/account/api-keys
api_key: sk-xxx
# maximum size of a chunk of text to be sent to the model
chunk_size: 500
# the maximum tokens
max_tokens: 1048
# model name for the OpenAI API
model_name: gpt-3.5-turbo
# model path for the local model
model_path: models/ggml-gpt4all-j-v1.3-groovy.bin
# model type: openai or local
model_type: openai
```

### Features

More commands will be added in the future.

### Contributing

Contributions are always welcome!