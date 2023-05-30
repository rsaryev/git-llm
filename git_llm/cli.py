import fire
import questionary

from git_llm.llm import factory_llm
from git_llm.prompt import c_changelog_prompt, m_changelog_prompt
from git_llm.utils.git import git
from git_llm.utils.helpers import get_config, DEFAULT_CONFIG, save_config


def changelog():
    config = get_config()
    llm = factory_llm(config)

    diff = git.git_diff()
    if not diff:
        raise Exception("No changes found")
    docs = llm.text_splitter(diff)
    git_changelog_message = llm.summarize_docs(docs, m_changelog_prompt, c_changelog_prompt)
    print(f"\n{git_changelog_message}")


def configure():
    config = get_config()
    model_type = questionary.select(
        "🤖 Select model type:",
        choices=[
            {"name": "OpenAI", "value": "openai"},
            {"name": "Local", "value": "local"},
        ]
    ).ask()
    config["model_type"] = model_type
    if model_type == "openai":
        model_name = input("🤖 Enter your model name (default: gpt-3.5-turbo): ") or DEFAULT_CONFIG["model_name"]
        config["model_name"] = model_name

        api_key = questionary.password("🤖 Enter your API key: ").ask()
        config["api_key"] = api_key
    else:
        model_path = input(f"🤖 Enter your model path: (default: {DEFAULT_CONFIG['model_path']}) ")
        config["model_path"] = model_path

    save_config(config)


def main():
    try:
        fire.Fire({
            "changelog": changelog,
            "config": configure,
        })
    except KeyboardInterrupt:
        print("\n🤖 Bye!")
    except Exception as e:
        if str(e) == "<empty message>":
            print("🤖 Please configure your API key. Use talk-codebase configure")
        else:
            raise e


if __name__ == "__main__":
    main()
