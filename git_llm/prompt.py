from langchain import PromptTemplate

m_changelog_prompt = PromptTemplate(template="""You are reviewing the git diff and writing a changelog message.
The chunk git diff: 
```{text}```""", input_variables=['text'])

c_changelog_prompt = PromptTemplate(template="""You are reviewing the changelog and combining the changelog.

Answer only change list:
The changelog:
```{text}```""", input_variables=['text'])

m_commit_prompt = PromptTemplate(template="""You are reviewing the git diff and writing a commit message.
Use format Conventional Commits.
The chunk git diff:
```{text}```""", input_variables=['text'])

c_commit_prompt = PromptTemplate(template="""You are reviewing the commit message and combining the commit message.
Use format Conventional Commits. Return only the commit first line.
The commits:
```{text}```""", input_variables=['text'])
