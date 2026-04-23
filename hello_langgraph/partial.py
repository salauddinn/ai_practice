from typing import TypedDict

from langgraph.graph import StateGraph,START,END
# typeDict example in python
class State(TypedDict):
    """this class represents the state of class
    """
    fin_dept: bool = False
    lib_dept: bool = False
    sports_dept: bool = False
    student_id: str

def financial_department_check(state: State) -> State:
   return {"fin_dept": True}
def library_department_check(state: State) -> State:
   return {"lib_dept": True}
def sports_department_check(state: State) -> State:
    return {"sports_dept": True}
    
     # graph which takes state as input and outputs the next state  

graph= StateGraph(State);
graph.add_node("fin", financial_department_check)
graph.add_node("lib", library_department_check)
graph.add_node("sports", sports_department_check)

# sequtienal graph
graph.add_edge(START, "fin")
graph.add_edge("fin", "lib")  
graph.add_edge("lib", "sports")
graph.add_edge("sports", END)

if __name__ == "__main__":
    compile_graph= graph.compile()
    response = compile_graph.invoke(
        {"student_id": "12345", 
         })
    print(response)