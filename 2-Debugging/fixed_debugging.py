from langgraph.graph import START, END, StateGraph
from typing import Annotated
from typing_extensions import TypedDict
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages, BaseMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langgraph.types import Command, interrupt

# Load environment variables
load_dotenv()

# Fix the environment variable name (it was lowercase 'key' instead of uppercase 'KEY')
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")  # Fixed: was "GROQ_API_key"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"

# Initialize LLM
from langchain.chat_models import init_chat_model
llm = init_chat_model("groq:llama3-8b-8192")

# State definition
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define tools - add the missing tool that the LLM is trying to call
@tool
def add(a: float, b: float):
    """add number"""
    return a + b

@tool
def define_machine_learning(definition: str = ""):
    """Define or explain machine learning concepts"""
    if definition:
        return f"Machine Learning Definition: {definition}"
    else:
        return "Machine learning is a subfield of artificial intelligence that involves training algorithms to learn from data and make predictions or decisions without being explicitly programmed."

# Create tools list with both tools
tools = [add, define_machine_learning]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

def call_llm_model(state: State):
    return {"messages": [llm_with_tools.invoke(state['messages'])]}

# Build the graph
builder = StateGraph(State)
builder.add_node("tool_calling_llm", call_llm_model)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)

builder.add_edge("tools", END)

graph = builder.compile()

# Test the graph
if __name__ == "__main__":
    try:
        response = graph.invoke({"messages": ["what is machine learning?"]})
        print("Success!")
        print(response)
    except Exception as e:
        print(f"Error: {e}") 