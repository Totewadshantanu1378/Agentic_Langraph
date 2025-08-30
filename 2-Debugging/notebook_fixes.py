# FIX FOR CELL 1 - Environment Variables
# Replace the content of Cell 1 with this:

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")  # Fixed: was "GROQ_API_key" (lowercase)
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"

# FIX FOR CELL 4 - Tools
# Replace the content of Cell 4 with this:

from langchain_core.tools import tool

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

tools = [add, define_machine_learning]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

def call_llm_model(state: State):
    return {"messages": [llm_with_tools.invoke(state['messages'])]} 