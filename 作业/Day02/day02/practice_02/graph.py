from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from node import *

builder = StateGraph(OverAllState)
builder.add_node("calc_node",calc_node)
builder.add_node("output_node",output_node)

builder.add_edge(START,"calc_node")
builder.add_edge("calc_node","output_node")
builder.add_edge("output_node",END)

memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)
config = {"configurable":{"thread_id":"test_thread"}}

graph.invoke({"original_input":2},config)
result = graph.invoke(None,config)
print(result)



