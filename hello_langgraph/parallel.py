from typing import TypedDict

from langgraph.graph import StateGraph,START,END
# typeDict example in python
class State(TypedDict):
    """this class represents the state of class
    """
    message: str
    student: str

def message_from_friend(state: State) -> State:
    return {"message": "You will win!"}

def message_from_enemy(state: State) -> State:
    return {"message": "You will  die trying but not win!"}

# Intentional: both nodes write to the same "message" key to demonstrate
# that in parallel execution, one result will overwrite the other (last write wins).
graph = StateGraph(State);
graph.add_node("friend", message_from_friend)
graph.add_node("enemy", message_from_enemy)

graph.add_edge(START, "friend")
graph.add_edge(START, "enemy")
graph.add_edge("friend", END)
graph.add_edge("enemy", END)

if __name__ == "__main__":
    compile_graph= graph.compile()
    response = compile_graph.invoke( State(student="Shyam") )
    print(response)
    
     # graph which takes state as input and outputs the next state