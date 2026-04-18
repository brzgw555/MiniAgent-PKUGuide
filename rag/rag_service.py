"""rag总结服务类"""
from json import load


from .vector_store import VectorStoreService
from utils_agent.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template |self.model|StrOutputParser()
        return chain
    
    def retrieve_docs(self, query:str)->list[Document]:
        return self.retriever.invoke(query)
    
    def rag_summarize(self,query:str)->str:
        context_docs = self.retrieve_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter +=1
            context += f"参考资料{counter}:{doc.page_content}\n"

        return self.chain.invoke({"input":query,"context":context})