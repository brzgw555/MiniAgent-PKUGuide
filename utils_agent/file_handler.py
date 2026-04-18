import os
import hashlib
from .logger_handler import *
from langchain_community.document_loaders import TextLoader
def get_file_md5_hex(file_path:str):    #获取文件的md5十六进制字符串
    if not os.path.exists(file_path):    #判断文件是否存在
        logger.error(f'文件不存在:{file_path}')
        return
    if not os.path.isfile(file_path):    #判断是否是文件
        logger.error(f'不是文件:{file_path}')
        return
    
    chunk_size = 4096   # 4kB
    md5_obj = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:   #分chunk计算md5值必须读文件二进制
            while chunk:=f.read(chunk_size):
                md5_obj.update(chunk)

            md5_hex = md5_obj.hexdigest()
            return md5_hex
        
    except Exception as e:
        logger.error(f'获取文件md5十六进制字符串失败:{file_path},错误信息:{e}')
        return None



def listdir_with_allowed_type(path:str,allowed_type:tuple[str]):
    files= []

    if not os.path.isdir(path):
        logger.error(f'路径不是文件夹:{path}')
        return

    for f in os.listdir(path):
        if f.endswith(allowed_type):
            files.append(os.path.join(path,f))


    return tuple(files) #不允许修改

def text_loader(file_path:str)->TextLoader:
    return TextLoader(file_path,encoding="utf-8").load()