from langgraph.graph import START, END, StateGraph
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
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

# Define comprehensive tools
@tool
def add(a: float, b: float):
    """Add two numbers together"""
    return a + b

@tool
def define_machine_learning():
    """Define what machine learning is"""
    return "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. It involves algorithms that can identify patterns in data and make predictions or decisions based on those patterns."

@tool
def retrieve_definition(search_term: str):
    """Retrieve definition for a given search term"""
    definitions = {
        "machine learning": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.",
        "artificial intelligence": "Artificial intelligence is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
        "deep learning": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data."
    }
    return definitions.get(search_term.lower(), f"Definition for {search_term}: This is a placeholder definition.")

@tool
def search_web(query: str):
    """Search the web for information"""
    return f"Search results for '{query}': This is a placeholder for web search functionality. In a real implementation, you would integrate with a search API."

# Create tools list and bind to LLM
tools = [add, define_machine_learning, retrieve_definition, search_web]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

def call_llm_model(state: State):
    return {"messages": [llm_with_tools.invoke(state['messages'])]}

# Build the graph
memory = MemorySaver()

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
        print("Response:", response)
    except Exception as e:
        print(f"Error: {e}")
        print("Trying simple approach...")
        
        # Fallback to simple approach
        simple_response = llm.invoke("what is machine learning?")
        print("Simple response:", simple_response) 