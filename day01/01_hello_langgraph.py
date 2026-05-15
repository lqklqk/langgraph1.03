from typing import TypedDict

from langgraph.constants import START,END
from langgraph.graph import StateGraph


# 状态的定义
class OverallState(TypedDict):
    user_input: str
    user_output: str

# 节点的定义
def node_1(state:OverallState) -> OverallState:
    user_input = state["user_input"]
    print(f'node_1的输出是：{user_input}')
    # 赋值给 user_output
    result = {"user_output":user_input}
    return result

def node_2(state:OverallState) -> OverallState:
    output = state["user_output"]
    print(f'node_2的输出是：{output}')


# 注册图

builder = StateGraph(OverallState)
# 注册节点
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
# 注册边
builder.add_edge(START,"node_1")
builder.add_edge("node_1","node_2")
builder.add_edge("node_2",END)

# 编译图
graph = builder.compile()
# 调用图
graph.invoke({"user_input":"hello"})