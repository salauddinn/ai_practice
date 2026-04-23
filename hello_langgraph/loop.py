from typing import TypedDict
from typing import Literal
from langgraph.graph import StateGraph,START,END
# typeDict example in python
class State(TypedDict):
    """this class represents the state of class
    """
    application: str
    comments:list[str]=[]
    retry_count: int = 0
    approved: bool


def conditional_check(state: State) -> Literal["reapply", "next"]:
    if state["retry_count"] >= 3:
        return "next"
    else:
        return "reapply"

def apply(state: State) -> State:
    state["retry_count"] =  state["retry_count"] +1
    state["comments"] = state["comments"] + [f"Application attempt {state['retry_count']}: {state['application']}"]
    return state

def process(state: State) -> State:
    state["comments"]= state["comments"] + [f"Processing application: {state['application']}"]
    return state

def approved(state: State) -> State:
    state["comments"] = state["comments"] + ["C:Your application is approved"]
    state["approved"] = True    
    return state


graph= StateGraph(State);


graph.add_node("A", apply)
graph.add_node("B",  process)
graph.add_node("C", approved)



graph.add_edge(START, "A")
graph.add_edge("A", "B")
graph.add_conditional_edges(
    "B",
    conditional_check,
    {
        "reapply": "A",
        "next": "C"
    }
    )
graph.add_edge("C", END)

if __name__ == "__main__":
    compile_graph= graph.compile()
    application=input("Enter your application: ")
    response = compile_graph.invoke({
        "application": application,
        "comments": [],
        "retry_count": 0,
        "approved": False,
    }
         )
    print(response)