from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from torch import embedding
from utils_agent.config_handler import rag_conf
from langchain_community.embeddings import DashScopeEmbeddings


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)->Optional[Embeddings|BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatTongyi(model=rag_conf["chat_model_name"])
    

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self):
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])


chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()