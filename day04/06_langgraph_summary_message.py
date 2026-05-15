"""
LangGraph 对话总结演示

该演示展示了如何使用聊天模型来总结消息历史，而不是简单地修剪或删除消息。
这种方法可以避免在清理消息队列时丢失信息。
"""

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, add_messages,END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict

class SummaryState(TypedDict):
    messages:Annotated[list,add_messages]
    summary:str

model = init_chat_model(
    "qwen-plus",
    model_provider="openai",
    api_key="sk-e75fee6662a34fac9b21cd2c62806bc2",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
)

summarization_model = model.bind(max_tokens=128)


def summarize_conversation(messages: Sequence[BaseMessage], current_summary: str = "") -> str:
    """
    使用模型总结对话历史

    Args:
        messages: 消息列表
        current_summary: 当前摘要

    Returns:
        str: 更新后的摘要
    """
    if not messages:
        return current_summary

    # 如果有模型则调用，否则使用模拟摘要
    if summarization_model:
        try:
            # 构造总结提示
            summary_prompt = f"当前摘要: {current_summary}\\n\\n新对话:\\n"
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    summary_prompt += f"人类: {msg.content}\\n"
                elif isinstance(msg, AIMessage):
                    summary_prompt += f"AI: {msg.content}\\n"

            summary_prompt += "\\n请提供一个简洁的摘要，包含重要的信息和上下文:"

            response = summarization_model.invoke([SystemMessage(content=summary_prompt)])
            return response.content
        except Exception as e:
            print(f"调用总结模型出错: {e}")
            # 出错时使用模拟摘要
            pass

    # 模拟摘要生成
    summary_content = " ".join([msg.content for msg in messages[-3:]])  # 取最后3条消息
    return f"对话摘要: {summary_content[:100]}..."  # 简单截取前100个字符


def summarize_node(state: SummaryState):
    """
    总结节点函数

    Args:
        state: 当前状态

    Returns:
        dict: 更新后的状态
    """
    print("\\n执行节点: summarize_node")
    messages = state["messages"]
    current_summary = state.get("summary", "")

    print(f"当前消息数量: {len(messages)}")
    print(f"当前摘要: {current_summary}")

    # 如果消息数量超过阈值，进行总结
    if len(messages) > 2:  # 当消息数量超过4条时进行总结
        print("消息数量超过阈值，开始总结对话历史...")
        # 取最近的几条消息进行总结
        recent_messages = messages[-4:]  # 最近4条消息
        new_summary = summarize_conversation(recent_messages, current_summary)
        print(f"生成的新摘要: {new_summary}")

        # 返回更新后的摘要和保留最近的几条消息
        return {
            "summary": new_summary,
            "messages": messages[-2:]  # 保留最近2条消息
        }
    else:
        print("消息数量未超过阈值，无需总结")
        return {"summary": current_summary}


def call_model(state: SummaryState):
    """
    调用模型的节点函数

    Args:
        state: 当前状态，包含消息历史和摘要

    Returns:
        dict: 更新后的状态
    """
    print("\\n执行节点: call_model")
    messages = state["messages"]
    summary = state.get("summary", "")

    print(f"当前消息数量: {len(messages)}")
    print(f"当前摘要: {summary}")

    # 构造包含摘要的完整上下文
    context_messages = []
    if summary:
        context_messages.append(SystemMessage(content=f"之前的对话摘要: {summary}"))

    context_messages.extend(messages)

    # 显示所有消息
    for i, msg in enumerate(context_messages):
        print(f"  消息 {i + 1}: {type(msg).__name__} - {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")

    # 如果有模型则调用，否则使用模拟响应
    if model:
        try:
            response = model.invoke(context_messages)
            print(f"生成的回复: {response.content}")
            return {"messages": [response]}
        except Exception as e:
            print(f"调用模型出错: {e}")
            # 出错时使用模拟响应
            pass
    return {"messages": [AIMessage(content=response)]}

builder = StateGraph(SummaryState)
builder.add_node("summary",summarize_node)
builder.add_node("llm",call_model)

builder.add_edge(START,"summary")
builder.add_edge("summary",END)

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)
# 配置线程ID
config = {"configurable": {"thread_id": "1"}}

# 第一次调用 - 问候
print("1. 第一次调用 - 问候:")
result1 = graph.invoke({
    "messages": [HumanMessage(content="我的名字是 bob")],
    "summary": ""
}, config)
print(f"回复: {result1['messages'][-1].content}")
print(f"当前摘要: {result1.get('summary', '')}")

print("\\n" + "=" * 50 + "\\n")

# 第二次调用 - 请求写诗（关于猫）
print("2. 第二次调用 - 请求写诗（关于猫）:")
result2 = graph.invoke({
    "messages": [HumanMessage(content="写一首关于猫的诗歌")],
    "summary": result1.get("summary", "")
}, config)
print(f"回复: {result2['messages'][-1].content}")
print(f"当前摘要: {result2.get('summary', '')}")

print("\\n" + "=" * 50 + "\\n")

# 第三次调用 - 请求写诗（关于狗）
print("3. 第三次调用 - 请求写诗（关于狗）:")
result3 = graph.invoke({
    "messages": [HumanMessage(content="现在再写一个关于狗的")],
    "summary": result2.get("summary", "")
}, config)
print(f"回复: {result3['messages'][-1].content}")
print(f"当前摘要: {result3.get('summary', '')}")

print("\\n" + "=" * 50 + "\\n")

# 第四次调用 - 询问名字
print("4. 第四次调用 - 询问名字:")
result4 = graph.invoke({
    "messages": [HumanMessage(content="我的名字是什么？")],
    "summary": result3.get("summary", "")
}, config)
print(f"回复: {result4['messages'][-1].content}")
print(f"当前摘要: {result4.get('summary', '')}")

print("\\n" + "=" * 50 + "\\n")

# 第五次调用 - 添加更多对话以触发总结
print("5. 第五次调用 - 添加更多对话以触发总结:")
conversation_history = [
    HumanMessage(content="让我们聊聊天气"),
    AIMessage(content="好的，你想聊什么地区的天气？"),
    HumanMessage(content="北京的天气怎么样？"),
    AIMessage(content="我无法获取实时天气信息，但北京属于温带大陆性季风气候。"),
    HumanMessage(content="what's my name?")  # 再次询问名字
]

result5 = graph.invoke({
    "messages": conversation_history,
    "summary": result4.get("summary", "")
}, config)
print(f"回复: {result5['messages'][-1].content}")
print(f"当前摘要: {result5.get('summary', '')}")

print("\\n=== 演示完成 ===")
