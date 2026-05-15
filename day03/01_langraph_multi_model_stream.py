from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class State(TypedDict):
    question:str
    answer:str
    confidence:float
    steps:int

def question(state:State):
    question = state['question']
    # 模拟思考
    steps = [f"分析问题: {question}", "检索相关知识", "形成初步答案"]
    return {"steps": steps}


def respond(state: State) -> State:
    """回应节点"""
    question = state["question"]
    # 根据问题生成答案
    if "天气" in question:
        answer = "今天天气晴朗"
        confidence = 0.9
    elif "时间" in question:
        answer = "现在是上午10点"
        confidence = 0.8
    else:
        answer = "这是一个很好的问题"
        confidence = 0.7

    return {
        "answer": answer,
        "confidence": confidence
    }

def reflect(state: State) -> State:
    answer = state["answer"]
    confidence = state["confidence"]
    steps = state["steps"]

    steps.append(f"验证答案：{answer}")
    steps.append(f"置信度：{confidence}")

    if confidence > 0.8:
        conclusion ="高置信度答案"
    elif confidence > 0.5:
        conclusion = "中高置信度答案"
    else:
        conclusion = "低置信度答案"
    steps.append(f"结论{conclusion}")
    return {"steps": steps}


builder = StateGraph(State)
builder.add_node("question",question)
builder.add_node("respond",respond)
builder.add_node("reflect",reflect)

# 添加边
builder.add_edge(START,"question")
builder.add_edge("question","respond")
builder.add_edge("respond","reflect")
builder.add_edge("reflect",END)

graph = builder.compile()
input = {
    "question":"今天天气怎么样",
    "answer":"",
    "confidence":0.0,
    "steps":[]
}
# 使用 values 模式进行流式展示

"""for chunks in graph.stream(input,stream_mode ="values"):
    print(f"  {chunks}")"""

# 使用updates 模式流式展示
"""for chunks in graph.stream(input,stream_mode = "updates"):
    print(f"  {chunks}")"""

# 使用多种流模式输出
for mode, chunk in graph.stream(input, stream_mode=["values", "updates"]):
    print(f"  [{mode}]: {chunk}")

# 使用debug模式
for chunks in graph.stream(input, stream_mode="debug"):
    print(f"  {chunks}")
