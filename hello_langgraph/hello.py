from typing import TypedDict

from langgraph.graph import StateGraph,START,END
# typeDict example in python
class MyState(TypedDict):
    """this class represents the state of class
    """
    name: str
    friends: list[str]
    family: list[str]

def find_friends(state: MyState) -> list[str]:
    """this function takes the state as input and returns the list of friends
    """
    state['friends']= ['Alice', 'Bob', 'Charlie'] 
    return state

def find_family(state: MyState) -> list[str]:
    """this function takes the state as input and returns the list of family members
    """
    state['family']= ['Mom', 'Dad', 'Sister'] 
    return state



 # graph which takes state as input and outputs the next state   
graph= StateGraph(MyState);
graph.add_node("friends", find_friends)
graph.add_node("family", find_family)
graph.add_edge(START, "friends")
graph.add_edge("friends", "family")
graph.add_edge("family", END)

#compile the graph
graph= graph.compile()

if __name__ == "__main__":
    response = graph.invoke(
        {"name": "John", 
         "friends": [], 
         "family": [], 
         })
    print(response)
    
