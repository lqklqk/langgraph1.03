from langgraph.graph import StateGraph, START, END

from node import *

builder = StateGraph(OverAllState)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)
builder.add_node("node_4",node_4)
builder.add_node("node_5",node_5,defer = True)
builder.add_node("node_6",node_6,defer = True)
builder.add_edge(START,"node_1")
builder.add_edge(START,"node_3")
builder.add_edge(START,"node_4")
builder.add_edge("node_1","node_2")
builder.add_edge("node_2","node_5")
builder.add_edge("node_3","node_5")
builder.add_edge("node_4","node_6")
builder.add_edge("node_5","node_6")
builder.add_edge("node_6",END)

graph = builder.compile()
print("=== 开始执行工作流 ===")
result = graph.invoke({})
print("=== 执行结果 ===")
print(result)