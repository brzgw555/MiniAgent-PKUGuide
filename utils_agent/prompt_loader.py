from .config_handler import prompt_conf
from .path_tool import get_abs_path
from .logger_handler import logger

def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompt_conf['main_prompt_path'])

    except KeyError as e:
        logger.error(f"yaml配置文件没有main_prompt_path")
        raise e

    try:
        return open(system_prompt_path,'r',encoding='utf-8').read()
    
    except Exception as e:
        logger.error(f"加载系统提示语失败:{e}")
        raise e


def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompt_conf['rag_summarize_prompt_path'])

    except KeyError as e:
        logger.error(f"yaml配置文件没有rag_summarize_prompt_path")
        raise e

    try:
        return open(rag_prompt_path,'r',encoding='utf-8').read()
    
    except Exception as e:
        logger.error(f"加载rag总结提示语失败:{e}")
        raise e


def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompt_conf['report_prompt_path'])

    except KeyError as e:
        logger.error(f"yaml配置文件没有report_prompt_path")
        raise e

    try:
        return open(report_prompt_path,'r',encoding='utf-8').read()
    
    except Exception as e:
        logger.error(f"加载report提示语失败:{e}")
        raise e
    

