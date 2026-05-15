from langgraph.constants import START, END
from langgraph.graph import StateGraph

from homework.state import OverallState
from nodes import *
builder = StateGraph(OverallState)
builder.add_node("node",node_1)

# 添加边
builder.add_edge(START,"node")
builder.add_edge("node",END)

#编译
graph = builder.compile()
graph.invoke({"a":"hola"})
