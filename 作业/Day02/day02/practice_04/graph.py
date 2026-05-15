from typing import Sequence

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send

from state import OverAllState
from node import *

builder = StateGraph(OverAllState)
builder.add_node("generate_scores",generate_scores)
builder.add_node("generate_level",generate_level)

# 条件边函数
def map_process(state:OverAllState) -> Sequence[Send]:
    scores = state["scores"]
    print("在处理中检测到成绩："+ str(scores))
    send_list = [Send("generate_level", {"score": score}) for score in scores]
    return send_list

builder.add_edge(START,"generate_scores")
builder.add_conditional_edges(
    "generate_scores", # 源节点
    map_process # 路由函数
)
builder.add_edge("generate_level",END)

graph = builder.compile()
graph.invoke({})