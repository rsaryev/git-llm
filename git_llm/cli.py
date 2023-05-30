import fire
import questionary

from git_llm.llm import factory_llm
from git_llm.prompt import c_changelog_prompt, m_changelog_prompt, m_commit_prompt, c_commit_prompt
from git_llm.utils.git import git
from git_llm.utils.helpers import get_config, DEFAULT_CONFIG, save_config


def check_for_changes():
    diff = git.git_diff()
    if not diff:
        print("🤖 No changes found try git add .")
        exit(0)
    return diff


def summarize_docs(llm, docs, message_prompt, changelog_prompt):
    summary = llm.summarize_docs(docs, message_prompt, changelog_prompt)
    print(f"\n{summary}")
    return summary


def changelog():
    config = get_config()
    llm = factory_llm(config)

    diff = check_for_changes()
    docs = llm.text_splitter(diff)
    summarize_docs(llm, docs, m_changelog_prompt, c_changelog_prompt)


def commit():
    config = get_config()
    llm = factory_llm(config)

    diff = check_for_changes()
    docs = llm.text_splitter(diff)

    summary = summarize_docs(llm, docs, m_commit_prompt, c_commit_prompt)
    ask = questionary.confirm(f"🤖 Do you want to commit with message: {summary}?").ask()
    if not ask:
        print("🤖 Bye!")
        exit(0)
    git.git_commit(summary)


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
            "commit": commit,
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
