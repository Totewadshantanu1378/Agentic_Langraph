import streamlit as st
from basic_chatbot import llmwithtools


st.title("LangGraph AI Agent")
chat_history = st.session_state.get("history", [])

user_input = st.text_input("You:")
if user_input:
    response = your_agent_function(user_input, chat_history)
    chat_history.append((user_input, response))
    st.session_state["history"] = chat_history

for user, bot in chat_history:
    st.markdown(f"**You:** {user}")
    st.markdown(f"**Bot:** {bot}")
