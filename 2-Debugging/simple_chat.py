from langgraph.graph import START, END, StateGraph
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

# Environment setup
os.environ["GROQ_API_key"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"

# Initialize LLM
llm = init_chat_model("groq:llama3-8b-8192")

# State definition
class State(TypedDict):
    messages: Annotated[list, add_messages]

def call_llm_model(state: State):
    return {"messages": [llm.invoke(state['messages'])]}

# Build the graph
builder = StateGraph(State)
builder.add_node("llm", call_llm_model)
builder.add_edge(START, "llm")
builder.add_edge("llm", END)

graph = builder.compile()

# Test the graph
if __name__ == "__main__":
    try:
        response = graph.invoke({"messages": ["what is machine learning?"]})
        print("Response:", response)
    except Exception as e:
        print(f"Error: {e}") 