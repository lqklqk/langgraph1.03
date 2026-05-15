from typing import Literal

from langgraph.graph import StateGraph
from langgraph.constants import START,END
from state import OverallState
from node import *
builder = StateGraph(OverallState)
def odd_even_judgment_edge(state:OverallState) -> Literal["odd","even"]:
    odd = state['odd']
    if(odd):
        return "odd"
    else:
        return "even"
def calc_edge(state:OverallState) -> Literal["double","one_plus"]:
    user_input = state['user_input']
    if(user_input > 5):
        return "double"
    else:
        return "one_plus"

builder.add_node("judgment",odd_even_judgment)
builder.add_node("odd",odd_judgment)
builder.add_node("even",even_judgment)
builder.add_node("double",double_process)
builder.add_node("one_plus",one_plus_process)

builder.add_edge(START,"judgment")
builder.add_conditional_edges(
    "judgment",
    odd_even_judgment_edge,
    {
        "odd":"odd",
        "even":"even"
    }
)
builder.add_conditional_edges(
    "odd",
    calc_edge,
    {
        "double":"double",
        "one_plus":"one_plus"
    }
)
builder.add_conditional_edges(
    "even",
    calc_edge,
    {
        "double":"double",
        "one_plus":"one_plus"
    }
)
builder.add_edge("double",END)
builder.add_edge("one_plus",END)

graph = builder.compile()
graph.invoke({"user_input":20,"odd":False ,"even":False})
