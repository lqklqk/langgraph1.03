from tkinter import END

from node import calc, output
from state import InputState, OutputState, OverallState
from langgraph.graph import START, END, StateGraph


builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

# 注册节点
builder.add_node("calc_node", calc)
builder.add_node("output_node", output)

# 添加边
builder.add_edge(START, "calc_node")
builder.add_edge("calc_node", "output_node")
builder.add_edge("output_node", END)

# 编译图
graph = builder.compile()

r = graph.invoke({"input":3})

print(r)