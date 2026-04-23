from typing import TypedDict
from typing import Literal
from langgraph.graph import StateGraph,START,END
# typeDict example in python
class State(TypedDict):
    """this class represents the state of class
    """
    query: str
    response: str

def process_question(state: State) -> Literal["finance", "sports", "admin"]:
    if "fee" in state["query"]:
        return "finance"
    elif "sports" in state["query"] or "game" in state["query"]:
        return "sports"
    else:
        return "admin"

def fin_response(state: State) -> State:
    return {"response": "Pay your fee"};

def admin_dept(state: State) -> State:
    return {"response": "Meet me tomorrow"}

def sport_dept(state: State) -> State:
    return {"response": "Physical trainer is on leave"}

graph= StateGraph(State);

graph.add_node("fin", fin_response)
graph.add_node("adm", admin_dept)
graph.add_node("sport", sport_dept)

graph.add_conditional_edges(
    START,
    process_question,
    {
        "finance": "fin",
        "admin": "adm",
        "sports": "sport"
    }

)
graph.add_edge("fin", END)
graph.add_edge("adm", END)
graph.add_edge("sport", END)
  
if __name__ == "__main__":
    compile_graph= graph.compile()
    query=input("Ask your question: ")  
    response = compile_graph.invoke(
        {"query": query}
         )
    print(response)
