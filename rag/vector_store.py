import sys
from pathlib import Path
sys.path.append( str(Path(__file__).parent.parent) )
from langchain_chroma import Chroma
from utils_agent import logger_handler
from utils_agent.config_handler import chroma_conf
from model.factory import chat_model,embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils_agent.file_handler import get_file_md5_hex, text_loader,listdir_with_allowed_type
from utils_agent.path_tool import get_abs_path
from utils_agent.logger_handler import logger
from langchain_core.documents import Document


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_conf["persist_directory"])
        )
        self.spliter = RecursiveCharacterTextSplitter(
            separators=chroma_conf["separators"],
            chunk_size = chroma_conf["chunk_size"],
            chunk_overlap = chroma_conf["chunk_overlap"],
            length_function = len
        )
    
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})
    
    def load_document(self):
        """从数据文件夹内读取数据文件,转为向量存入
        要计算md5值
        """

        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]),"w",encoding="utf-8").close()
                return False
            
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip() == md5_for_check:
                        return True
                    
            return False
        
        def save_md5_hex(md5_for_save:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_save+"\n")

        def get_file_documents(read_path:str):
            if read_path.endswith("txt"):
                return text_loader(read_path)
            
            return []
        
        allowed_file_path = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
            )
        for path in allowed_file_path:
            md5_hex=get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"{path}已存在知识库中")
                continue

            try:
                documents:list[Document]=get_file_documents(path)

                split_document:list[Document]=self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"{path}没有内容,跳过")
                    continue

                self.vector_store.add_documents(split_document)

                save_md5_hex(md5_hex)

                logger.info(f"{path}已添加到知识库中")

            except Exception as e:
                logger.error(f"{path}添加到知识库失败,错误信息:{str(e)}",exc_info=True) # exc_info=True 记录详细的报错堆栈
                continue


if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("纪念碑")
    for r in res:
        print(r.page_content)
        print("*"*20)
