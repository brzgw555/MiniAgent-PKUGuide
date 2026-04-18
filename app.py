from ast import In

import streamlit as st
from agent.react_agent import ReactAgent
import time
from langgraph.checkpoint.memory import InMemorySaver


st.title("小北导游")
st.divider()


if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent(InMemorySaver())
if "message" not in st.session_state:
    st.session_state["message"] = []

config = {"configurable": {"thread_id": "user_001"}}


for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
# 输入提示词
prompt =st.chat_input()


if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})
    response_message=[]

    with st.spinner("小北导游正在思考..."):
        res=st.session_state["agent"].execute_stream(prompt,config)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01) 
                    yield char
            
        st.chat_message("assistant").write(capture(res,response_message))
        st.session_state["message"].append({"role":"assistant","content":response_message[-1]})
        st.rerun()