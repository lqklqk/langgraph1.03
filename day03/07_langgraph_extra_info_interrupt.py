import sqlite3
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

class ReviewState(TypedDict):
    generated_text:str


def review_node(state: ReviewState):
    """
    审阅节点

    Args:
        state: 当前状态，包含生成的文本内容

    Returns:
        dict: 更新后的状态
    """
    print(f"执行节点: review_node")
    print(f"当前文本内容: {state['generated_text']}")
    print("工作流暂停，等待用户审阅和编辑...")

    updated = interrupt(
        {
            "instruction":"请审阅并编辑以下内容",
            "content":state["generated_text"]
        }
    )
    print(f"接收到的内容是：{updated}")
    return {"generated_text": updated}

builder =StateGraph(ReviewState)
builder.add_node("review",review_node)
# 添加边
builder.add_edge(START,"review")
builder.add_edge("review",END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 配置线程ID
config = {"configurable": {"thread_id": "review-42"}}

initial = graph.invoke({"generated_text":"这是初始草稿内容"},config = config)
# 显示中断信息
print(f"工作流中断信息: {initial['__interrupt__']}\n")

# 恢复工作流
# 模拟用户审阅和编辑过程
print("2. 模拟用户审阅和编辑过程...")
interrupt_value = initial["__interrupt__"][0].value
print("指导说明:", interrupt_value["instruction"])
print("原文内容:", interrupt_value["content"])

# 获取用户编辑后的内容
edited_text = input("\n请输入编辑后的内容: ").strip()

final_state = graph.invoke(Command(resume = edited_text),config = config)

# 显示最终结果
print(f"最终状态: {final_state}")
print(f"最终文本内容: {final_state['generated_text']}")
print("\n=== 演示完成 ===")
