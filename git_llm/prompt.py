from langchain import PromptTemplate

m_changelog_prompt = PromptTemplate(template="""You are reviewing the git diff and writing a changelog message.
The chunk git diff: 
```{text}```""", input_variables=['text'])

c_changelog_prompt = PromptTemplate(template="""You are reviewing the changelog and combining the changelog.

Answer only change list:
The changelog:
```{text}```""", input_variables=['text'])
