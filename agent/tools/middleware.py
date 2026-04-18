from json import load

from langchain.agents.middleware import wrap_tool_call,before_model,dynamic_prompt,ModelRequest
from langchain.agents import AgentState
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from  langgraph.types import Command
from typing import Callable

from qwen_agent import Agent
from utils_agent.logger_handler import logger
from langgraph.runtime import Runtime
from utils_agent.prompt_loader import load_report_prompt,load_system_prompt
@wrap_tool_call
def monitor_tool(
    # 请求的数据结构
    request: ToolCallRequest,
    #执行的函数本身(Callable),它接受ToolCallRequest作为输入，并返回ToolMessage或Command
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
)-> ToolMessage | Command:
    
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]执行工具：{request.tool_call['args']}")
    try:
        result= handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}执行完毕")


        if request.tool_call['name']=="fill_context_for_report":
            request.runtime.context["report"]=True
            logger.info(f"[tool monitor]工具{request.tool_call['name']}触发了报告场景的上下文填充")
        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具{request.tool_call['name']}执行失败:{e}")
        raise e


@before_model
def log_before_model(
    state:AgentState,  # Agent状态记录
    runtime:Runtime,    #执行过程中上下文信息
):
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}个消息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__}|{state['messages'][-1].content.strip()}")

    return None


@dynamic_prompt  #每一次生成提示词之前调用
def report_prompt_switch(request:ModelRequest):
    is_report = request.runtime.context.get("report",False)
    if is_report:
        return load_report_prompt()
    
    return load_system_prompt()