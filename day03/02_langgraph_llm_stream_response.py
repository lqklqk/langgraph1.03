from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

model = init_chat_model(model="qwen3-max",
                        model_provider="openai",
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                        api_key="sk-e75fee6662a34fac9b21cd2c62806bc2",)
class State(TypedDict):
    query: str
    answer: str

def node(state:State):
    print("开始调用node节点")
    llm_result = model.invoke([("user",state["query"])])
    print("llm invoke 结束")
    return {"answer": llm_result}

builder = StateGraph(State)
builder.add_node("node",node)

# 添加边
builder.add_edge(START,"node")
builder.add_edge("node",END)

graph = builder.compile()
# 构造输入
input = {"query":"给我写一篇小学生日记"}

for chunk,meta_data in graph.stream(input,stream_mode="messages"):
    print(chunk.content,end="")