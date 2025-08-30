# Fix for Cell 4 - Add the missing retrieve_definition tool
from langchain_core.tools import tool

@tool
def add(a: float, b: float):
    """add number"""
    return a + b

@tool
def retrieve_definition(search_term: str):
    """Retrieve definition for a given search term"""
    return f"Definition for {search_term}: This is a placeholder definition. In a real implementation, you would search a knowledge base or database for the actual definition."

tools = [add, retrieve_definition]
tool_node = ToolNode([add, retrieve_definition])
llm_with_tools = llm.bind_tools(tools)

def call_llm_model(state: State):
    return {"messages": [llm_with_tools.invoke(state['messages'])]} 