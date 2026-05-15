from langgraph.graph import START, StateGraph, END
from node import *

from state import SubgraphState

# 构造子图
subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node("node_1",node_1)
subgraph_builder.add_node("node_2",node_2)
subgraph_builder.add_node("node_3",node_3)
subgraph_builder.add_edge(START,"node_1")
subgraph_builder.add_edge("node_1", "node_2")
subgraph_builder.add_edge("node_2", "node_3")
subgraph_builder.add_edge("node_3", END)
subgraph = subgraph_builder.compile()

# 创建父图
builder = StateGraph(OverallState)
builder.add_node("output_node",output_node)
builder.add_node("subgraph",subgraph)
builder.add_edge(START,"subgraph")
builder.add_edge("subgraph","output_node")
builder.add_edge("output_node",END)
graph = builder.compile()

# 包含子图的流式输出
for chunk in graph.stream(
    {"original_input":"original_input"},
    stream_mode ="updates",
    subgraphs=True
):
    print(f"  流式输出块: {chunk}")
