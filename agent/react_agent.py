from langchain.agents import create_agent
from model.factory import chat_model
from utils_agent.prompt_loader import load_system_prompt
from agent.tools.agent_tools import rag_summarize,get_user_id,fill_context_for_report
from agent.tools.middleware import log_before_model,monitor_tool,report_prompt_switch

class ReactAgent:
    def __init__(self,checkpointer = None):
        self.agent = create_agent(
            model =chat_model,
            system_prompt =load_system_prompt(),
            tools=[rag_summarize, get_user_id, fill_context_for_report],
            middleware=[log_before_model, monitor_tool, report_prompt_switch],
            checkpointer=checkpointer
        )

    def execute_stream(self,query:str,config:dict=None):
        input_dict={
            "messages":[
                {"role":"user","content":query}
            ]
        }

        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False},config=config):
              # context 添加提示词切换的标记
              latest_messages = chunk["messages"][-1]
              if latest_messages.content:
                   yield latest_messages.content.strip()+"\n"
        