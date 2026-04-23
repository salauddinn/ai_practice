from typing import TypedDict

from langgraph.graph import StateGraph,START,END
from typing_extensions import Annotated
import operator

# Annotated is a Python typing feature that lets you attach metadata to a type.
# Syntax: Annotated[Type, metadata]
# In LangGraph, the metadata is a "reducer" function that tells LangGraph
# HOW to merge values when multiple nodes return the same key.
#   - operator.add on lists = concatenate the lists together
#   - Without Annotated, LangGraph just replaces the old value (last write wins)

def my_choice(exisitng,new):
    """this is a custom reducer function that takes the existing value and the new value and returns the new value
    """
    return new
class State(TypedDict):
    """this class represents the state of class
    """
    # Annotated[list[str], operator.add] means:
    #   Type = list[str], Reducer = operator.add (list concatenation)
    message: Annotated[list[str],operator.add]
    # message: Annotated[list[str],my_choice]

    student: str

def message_from_friend(state: State) -> State:
    return {"message": ["You will win!"]}

def message_from_enemy(state: State) -> State:
    return {"message": ["You will  die trying but not win!"]}

# Problem: When parallel nodes write to the same key (e.g., "message": str),
# one result overwrites the other (last write wins) — you lose data.
#
# Fix: Use Annotated[list[str], operator.add] as a reducer.
# This tells LangGraph to append (operator.add) both results into a single list
# instead of overwriting. Output: ["You will win!", "You will die trying..."]
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