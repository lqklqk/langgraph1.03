from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt


class MyState(TypedDict):
    state_1:str
    state_2:Annotated[list,lambda x,y :x+y]

def node_1(state:MyState):
    print("进入了节点一")
    res = interrupt(
        {
            "key_1":"value_1",
            "key_2":"value_2"
        }
    )
    return res

builder=StateGraph(MyState)
builder.add_node("node",node_1)
builder.add_edge(START,"node")
builder.add_edge("node",END)

checkpoint = MemorySaver()
graph = builder.compile(checkpointer=checkpoint)
config = {"configurable":{"thread_id":1}}

result = graph.invoke(
    {
        "state_1":"test",
        "state_2":["1"]
    },
    config = config
)
print(result['__interrupt__'])