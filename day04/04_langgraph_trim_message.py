"""
LangGraph 消息修剪演示

展示了如何使用 trim_messages 函数来管理消息历史，
确保消息历史不会超过模型的最大上下文窗口限制。
如果环境中配置了API密钥，将使用百炼平台的通义大模型；否则使用模拟响应。
"""

import os
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately
)
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, MessagesState,END
from langgraph.checkpoint.memory import InMemorySaver

model = init_chat_model(
    "qwen-plus",
    model_provider="openai",
    api_key="sk-e75fee6662a34fac9b21cd2c62806bc2",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
)

def call_llm_node(state:MessagesState):
    print(f"原始消息总数量：{len(state["messages"])}")
    messages = trim_messages(
        state["messages"],
        strategy= "last",
        token_counter = count_tokens_approximately,
        max_tokens = 128,
        start_on = "human",
        end_on = ("human","tool")
    )
    # 显示修剪后的消息数量
    print(f"修剪后消息数量: {len(messages)}")
    response = model.invoke(messages)
    print(f"生成的恢复{response}")
    return{"messages": response}

builder = StateGraph(MessagesState)

checkpointer = InMemorySaver()

builder.add_node("call_llm",call_llm_node)
builder.add_edge(START,"call_llm")
builder.add_edge("call_llm",END)

graph = builder.compile(checkpointer = checkpointer)
# 配置线程ID
config = {"configurable": {"thread_id": "1"}}

# 第一次调用 - 问候
print("1. 第一次调用 - 问候:")
result1 = graph.invoke({
    "messages": [HumanMessage(content="hi, my name is bob")]
}, config)
print(f"回复: {result1['messages'][-1].content}")

# 第二次调用 - 请求写诗（关于猫）
print("\\n2. 第二次调用 - 请求写诗（关于猫）:")
result2 = graph.invoke({
    "messages": [HumanMessage(content="写一首关于猫的诗歌")]
}, config)
print(f"回复: {result2['messages'][-1].content}")

# 第三次调用 - 请求写诗（关于狗）
print("\\n3. 第三次调用 - 请求写诗（关于狗）:")
result3 = graph.invoke({
    "messages": [HumanMessage(content="再给我写一首关于狗的")]
}, config)
print(f"回复: {result3['messages'][-1].content}")

# 第四次调用 - 询问名字
print("\\n4. 第四次调用 - 询问名字:")
final_response = graph.invoke({
    "messages": [HumanMessage(content="我是什么名字?")]
}, config)
print(f"回复: {final_response['messages'][-1].content}")

# 模拟大量消息以展示修剪效果
print("\\n5. 模拟大量消息以展示修剪效果:")
# 添加大量消息
many_messages: List[HumanMessage] = []
for i in range(20):
    many_messages.append(HumanMessage(
        content=f"这是第{i + 1}条测试消息，内容很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长"))

result5 = graph.invoke({
    "messages": many_messages + [HumanMessage(content="what's my name?")]
}, config)
print(f"回复: {result5['messages'][-1].content}")

print("\\n=== 演示完成 ===")
