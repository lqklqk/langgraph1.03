from langgraph.config import get_stream_writer
from langgraph.constants import START,END
from langgraph.graph import StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    query:str
    answer:str
    progess:list

def node(state:State):
    # 获取流写入器以发送自定义数据
    writer = get_stream_writer()

    # 发送自定义数据
    writer({"customer_key":"开始处理查询"})
    writer({"progess":"步骤一：查询分析内容","status":"running"})

    query = state["query"]
    # 模拟处理流程
    result = f"处理结果：{query.upper()}"

    writer({"progress": "步骤2: 生成结果", "status": "running"})
    writer({"progress": "步骤3: 完成处理", "status": "completed"})
    writer({"custom_key": "查询处理完成"})

    return{
        "answer":result,
        "progress":state.get("progress",[]) + ["处理完成"]

    }

builder = StateGraph(State)
builder.add_node("node",node)

# 添加边
builder.add_edge(START,"node")
builder.add_edge("node",END)

# 编译
graph = builder.compile()

# 定义输入
input = {
    "query":"hello buddy",
    "answer":"",
    "progess":[]
}
"""for chunks in graph.stream(input,stream_mode="custom"):
    print(f"自定义数据块{chunks}")

for chunks in graph.stream(input,stream_mode="updates"):
    print(f"更新状态数据块 {chunks}")"""
for mode,chunks in graph.stream(input,stream_mode=["custom","updates"]):
    print(f"  [{mode}]: {chunks}")
