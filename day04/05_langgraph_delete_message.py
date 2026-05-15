"""
LangGraph 消息删除演示

该演示展示了如何使用 RemoveMessage 从图状态中删除消息。
当状态的 key 带有 add_messages 这个 reducer 时（例如 MessagesState），RemoveMessage 可以正常工作。
"""

from typing import Annotated, Sequence
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    RemoveMessage,
    BaseMessage
)
from langchain_core.messages.utils import count_tokens_approximately
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, MessagesState,END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict

from anggraph_funcapi_entrypoint import checkpointer


# 定义状态类型
class CustomMessagesState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "messages"]

model = init_chat_model(
    "qwen-plus",
    model_provider="openai",
    api_key="sk-e75fee6662a34fac9b21cd2c62806bc2",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
)

def call_llm(state: MessagesState):
    print("\\n执行节点: call_model")
    print(f"当前消息数量: {len(state['messages'])}")

    # 显示所有消息
    for i, msg in enumerate(state["messages"]):
        print(f"  消息 {i + 1}: {type(msg).__name__} - {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")
    response = model.invoke(state["messages"])
    print(f"生成的恢复：{response.content}")
    return {"messages": state["messages"]}

def delete_node(state: MessagesState):
    print("\\n执行节点: delete_messages")
    messages = state["messages"]
    print(f"删除前消息数量: {len(messages)}")

    if len(messages) > 2:
        # 删除最早的两条消息
        to_remove = [RemoveMessage(id=m.id) for m in messages[:2]]
        print(f"将删除 {len(to_remove)} 条消息")
        # 显示要删除的消息
        for i, msg in enumerate(messages[:2]):
            print(
                f"  删除消息 {i + 1}: {type(msg).__name__} - {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")
        return {"messages": to_remove}
    else:
        print("消息数量不足，无需删除")
        return {}

builder = StateGraph(MessagesState)

builder.add_node("call_llm",call_llm),
builder.add_node("delete",delete_node),
builder.add_edge(START,"call_llm")
builder.add_edge("call_llm","delete")
builder.add_edge("delete",END)
checkpointer = InMemorySaver()
# 编译图
app = builder.compile(checkpointer=checkpointer)

# 配置线程ID
config = {"configurable": {"thread_id": "1"}}

# 第一次调用 - 问候
print("1. 第一次调用 - 问候:")
for event in app.stream(
        {"messages": [HumanMessage(content="hi! I'm bob")]},
        config,
        stream_mode="values"
):
    print(f"当前状态中的消息数量: {len(event['messages'])}")
    if event["messages"]:
        last_message = event["messages"][-1]
        print(f"最新消息: {type(last_message).__name__} - {last_message.content}")

print("\\n" + "=" * 50 + "\\n")

# 第二次调用 - 询问名字
print("2. 第二次调用 - 询问名字:")
for event in app.stream(
        {"messages": [HumanMessage(content="what's my name?")]},
        config,
        stream_mode="values"
):
    print(f"当前状态中的消息数量: {len(event['messages'])}")
    if event["messages"]:
        last_message = event["messages"][-1]
        print(f"最新消息: {type(last_message).__name__} - {last_message.content}")

print("\\n" + "=" * 50 + "\\n")

# 第三次调用 - 请求写诗
print("3. 第三次调用 - 请求写诗:")
for event in app.stream(
        {"messages": [HumanMessage(content="write a short poem about cats")]},
        config,
        stream_mode="values"
):
    print(f"当前状态中的消息数量: {len(event['messages'])}")
    if event["messages"]:
        last_message = event["messages"][-1]
        print(f"最新消息: {type(last_message).__name__} - {last_message.content}")

print("\\n" + "=" * 50 + "\\n")

# 第四次调用 - 请求写诗（关于狗）
print("4. 第四次调用 - 请求写诗（关于狗）:")
for event in app.stream(
        {"messages": [HumanMessage(content="now do the same but for dogs")]},
        config,
        stream_mode="values"
):
    print(f"当前状态中的消息数量: {len(event['messages'])}")
    if event["messages"]:
        last_message = event["messages"][-1]
        print(f"最新消息: {type(last_message).__name__} - {last_message.content}")

print("\\n=== 演示完成 ===")
