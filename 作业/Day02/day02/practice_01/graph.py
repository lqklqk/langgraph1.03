from langgraph.graph import StateGraph, START, END
from node import *

builder = StateGraph(OverAllState)
builder.add_node("calc_node",calc_node)
builder.add_node("odd_node",odd_node)
builder.add_node("even_node",even_node)
builder.add_node("add_calc",add_calc)
builder.add_node("mul_calc",mul_calc)
builder.add_node("div_calc",div_calc)
builder.add_node("sub_calc",sub_calc)

builder.add_edge(START,"calc_node")
# command中完成了后续边的连接
builder.add_edge("odd_node","add_calc")
builder.add_edge("odd_node","mul_calc")
builder.add_edge("even_node","sub_calc")
builder.add_edge("even_node","div_calc")
builder.add_edge("add_calc",END)
builder.add_edge("mul_calc",END)
builder.add_edge("sub_calc",END)
builder.add_edge("div_calc",END)

graph = builder.compile()
graph.invoke({"original_input":2})




