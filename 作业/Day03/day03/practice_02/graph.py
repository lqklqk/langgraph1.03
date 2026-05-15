from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt

from node import input_interrupt_node,output_node
from state import OverallState

builder=StateGraph(OverallState)
builder.add_node("input_interrupt_node",input_interrupt_node)
builder.add_node("output_node",output_node)
builder.add_edge(START,"input_interrupt_node")
builder.add_edge("input_interrupt_node","output_node")
builder.add_edge("output_node",END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer = checkpointer)

config = {"configurable": {"thread_id": "test"}}
initial = graph.invoke({"original_input": "初始输入内容"}, config=config)
print(f"工作流中断信息: {initial['__interrupt__']}\n")

# 获取用户编辑后的内容
edited_text = input("\n请输入编辑后的内容: ").strip()

result = graph.invoke(
    Command(resume = edited_text),
    config = config,
)
print(result)