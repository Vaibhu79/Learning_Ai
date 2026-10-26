from langgraph.graph import END,StateGraph
from typing import TypedDict

# state banayenge kind of a whiteboard jisme har chiz subko dikhegi and update hoti rhegi

class State(TypedDict):
    number:int

# ab hum node banayenge different different kaam ke hisab se(accordingly)
def double(state:State) -> dict:

    boardnum = state["number"]
    
    newnum = boardnum * 2
    print("in double")
    print(newnum)

    # curly braces ka use key value pair ke wajah se kiya hai
    return{"number":newnum}


# ab hum ek or node banayenge jo ki finnish hone par call hoga

def finnish(state:State) -> dict:
    boardnum = state["number"]

    print("in finnish")
    print(boardnum)

    return{"number": boardnum}

# ab hum banayenge ek normal function jo ki condition check karega

def decision(state:State) ->str:
    if state["number"] < 100:
        return "double"
    else:
        return "finnish"

# kind of flow bana rhe hai hum log yha se
builder = StateGraph(State)

# humne uppar jo bhi nodes banaye hai unko yha par add kar rhe hai by the process below ("double",double) isme "" me jo hai wo node ka name hai and uske baad jo hai wo python function ka name hai
builder.add_node("double",double)
builder.add_node("finnish",finnish)

# entry ka point

builder.set_entry_point("double")

builder.add_conditional_edges(
    "double", decision,{
        "double":"double",
        "finnish":"finnish"},)
    
builder.add_edge("finnish",END)

graph=builder.compile()


if __name__ == "__main__":
    result=graph.invoke({"number":5})