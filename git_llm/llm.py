from halo import Halo
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import GPT4All
from langchain.llms import Ollama
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class BaseLLM:
    """
    Base class for LLM instances with common functionality.
    """

    def __init__(self, config):
        self.config = config
        self.llm = self._create_model()

    def _create_model(self):
        """
        Factory method pattern implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @Halo(text='Summarizing', spinner='dots')
    def summarize_docs(self, docs, m_prompt, c_prompt):
        summarize_chain = load_summarize_chain(self.llm,
                                               chain_type="map_reduce",
                                               combine_prompt=c_prompt,
                                               map_prompt=m_prompt)
        return summarize_chain.run(docs)

    def text_splitter(self, text):
        texts = RecursiveCharacterTextSplitter(chunk_size=int(self.config.get("chunk_size")),
                                               chunk_overlap=int(self.config.get("chunk_overlap"))
                                               ).split_text(text)
        docs = [Document(page_content=t) for t in texts]
        return docs


class LocalLLM(BaseLLM):
    """
    LLM that works locally on the user's machine.
    """

    def _create_model(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = GPT4All(
            model=self.config["model_path"],
            n_ctx=int(self.config["max_tokens"]),
            callback_manager=callback_manager
        )
        return llm


class OpenAILLM(BaseLLM):
    """
    LLM that sends queries to OpenAI's API.
    """

    def _create_model(self):
        return ChatOpenAI(
            model_name=self.config["model_name"],
            openai_api_key=self.config["api_key"],
            max_tokens=int(self.config["max_tokens"])
        )


class OLLamaLLM(BaseLLM):
    """
    LLM that works locally on the user's machine.
    """

    def _create_model(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = Ollama( 
            model=self.config["model_name"],
            base_url=self.config["base_url"],
            callback_manager=callback_manager
        )
        return llm

def factory_llm(config):
    """
    Factory function to create an LLM instance based on config.
    """
    if config["model_type"] == "openai":
        return OpenAILLM(config)
    elif config["model_type"] == "ollama":
        return OLLamaLLM(config)
    else:
        return LocalLLM(config)
