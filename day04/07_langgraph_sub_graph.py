"""
LangGraph 子图功能演示

该演示展示了如何在 LangGraph 中使用子图，包括：
1. 从节点调用图（不同的状态模式）
2. 将图添加为节点（共享状态模式）
3. 查看子图状态
4. 流式输出子图结果
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START,END
from langgraph.checkpoint.memory import MemorySaver


# 定义父图状态（不同的状态模式）
class ParentState(TypedDict):
    foo: str

# 定义共享状态的子图
class SharedSubgraphState(TypedDict):
    foo: str  # 共享状态键
    bar: str  # 子图私有状态键

# 定义非共享状态的子图
class SubgraphState(TypedDict):
    bar: str
    baz: str

def demo_add_graph_as_node():
    print("\\n===演示将图添加为节点===")
    subgraph = create_shared_subgraph()
    parent_graph = create_parent_graph_with_node_subgraph(subgraph)

    print("开始执行图")
    for chunk in parent_graph.stream({"foo":"foo"}):
        print(f"流式输出：{chunk}")

def shared_subgraph_node_1(state: SharedSubgraphState):
    """共享状态子图节点1"""
    print("执行共享状态子图节点1")
    return {"bar": "bar"}

def shared_subgraph_node_2(state: SharedSubgraphState):
    """共享状态子图节点2"""
    print("执行共享状态子图节点2")
    return {"foo": state["foo"] + state["bar"]}

def subgraph_node_1(state: SubgraphState):
    """子图节点1"""
    print("执行子图节点1")
    return {"baz": "baz"}

def subgraph_node_2(state: SubgraphState):
    """子图节点2"""
    print("执行子图节点2")
    return {"bar": state["bar"] + state["baz"]}

def node_1(state:ParentState):
    print("执行父图节点1")
    return {"foo":"hi!" + state["foo"]}

def node_2(subgraph):
    """父图节点2 -  调用子图"""
    def _call_subgraph(state:ParentState):
        print("执行父图节点2（调用子图）")
        # 转换状态到子图格式
        subgraph_input = {"bar":state["foo"],"baz":""}
        response = subgraph.invoke(subgraph_input)
        return {"foo": response["bar"]}
    return _call_subgraph

def create_shared_subgraph():
    """创建具有共享状态的子图"""
    subgraph_builder = StateGraph(SharedSubgraphState)
    subgraph_builder.add_node("shared_subgraph_node_1",shared_subgraph_node_1)
    subgraph_builder.add_node("shared_subgraph_node_2",shared_subgraph_node_2)
    subgraph_builder.add_edge(START, "shared_subgraph_node_1")
    subgraph_builder.add_edge("shared_subgraph_node_1", "shared_subgraph_node_2")
    subgraph_builder.add_edge("shared_subgraph_node_2",END)
    return subgraph_builder.compile()

def create_parent_graph_with_node_subgraph(subgraph):
    """创建将子图作为节点添加的父图"""
    print("\n===创建将子图作为节点添加的父图===")
    builder = StateGraph(ParentState)
    builder.add_node("node_1",node_1)
    builder.add_node("node_2",subgraph)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2",END)
    return builder.compile()

# demo_add_graph_as_node()

def demo_subgraph_call():
    print("\\n===从节点调用图===")
    subgraph = create_subgraph_different_schema()
    parent_graph = create_parent_graph_with_subgraph_call(subgraph)

    print("开始执行图")
    for chunk in parent_graph.stream({"foo":"foo"},subgraph = True):
        print(f"流式输出：{chunk}")

def create_subgraph_different_schema():
    print("\\n=== 创建具有不同状态模式的子图 ===")
    subgraph_builder = StateGraph(SubgraphState)
    subgraph_builder.add_node("subgraph_node_1",subgraph_node_1)
    subgraph_builder.add_node("subgraph_node_2",subgraph_node_2)
    subgraph_builder.add_edge(START, "subgraph_node_1")
    subgraph_builder.add_edge("subgraph_node_1","subgraph_node_2")
    subgraph_builder.add_edge("subgraph_node_2",END)
    return subgraph_builder.compile()

def create_parent_graph_with_subgraph_call(subgraph):
    """创建通过节点调用子图的父图"""
    print("\\n创建通过节点调用子图的父图")
    builder = StateGraph(ParentState)
    builder.add_node("node_1",node_1)
    builder.add_node("node_2",node_2(subgraph))
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2",END)
    return builder.compile()

demo_subgraph_call()