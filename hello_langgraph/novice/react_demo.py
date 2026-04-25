from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from typing import TypedDict, Literal
from typing_extensions import Annotated
# reducer
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os

load_dotenv()
project = os.getenv('GOOGLE_CLOUD_PROJECT')


# model
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    vertexai = True,
    project = project
)

llm.invoke("what is the capital of France?").pretty_print()
 #let's create basic tools

@tool("multiply")
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

@tool("add")
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@tool("subtract")
def subtract(a: int, b: int) -> int:
    """Subtracts two numbers."""
    return a - b

@tool("get_weather")
def get_weather(location: str) -> str:
    """Gets the weather for a location."""
    return f"The weather in {location} is sunny."

#all tools in an array  
tools = [multiply, add, subtract, get_weather]

# llm_with_tools = llm.bind_tools(tools)

# llm_with_tools.invoke("What is the weather in New York and what is 5 multiplied by 3?").pretty_print()

tool_node = ToolNode(tools=tools)

llm_with_tools = llm.bind_tools(tools=tools)

# llm_with_tools.invoke("What is the weather in New York").pretty_print()



class AgentState(TypedDict):
    """State of the agent."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[str]


def llm_node(state: AgentState) -> str:
    """Node that calls the LLM."""
    response = llm_with_tools.invoke(state['messages'])
    return {"messages":[response]}

def route_tools(state: AgentState) -> Literal["tools", "END"]:
    last_message = state['messages'][-1]
    if getattr(last_message, "tool_calls", []):
        return "tools"
    return END
    
graph = StateGraph(AgentState)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    route_tools,
    { "tools": "tools",
      END: END })
graph.add_edge("tools", "llm")

compile_graph = graph.compile()

if __name__ == "__main__":
    result =compile_graph.invoke({
        "messages":[
            HumanMessage(content="What is 10 times 5 plus 100")
            
        ]
    })
    for message in result['messages']:
        print(f"{message.type}: {message.content}")