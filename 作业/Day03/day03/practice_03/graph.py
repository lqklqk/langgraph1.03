import uuid

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START,END

from langgraph.graph import StateGraph

from state import OverallState
from node import *
builder = StateGraph(OverallState)
builder.add_node("process_1",process_1_node)
builder.add_node("process_2",process_2_node)
builder.add_node("process_3",process_3_node)
builder.add_node("process_4",process_4_node)
builder.add_edge(START,"process_1")
builder.add_edge("process_1","process_2")
builder.add_edge("process_2","process_3")
builder.add_edge("process_3","process_4")
builder.add_edge("process_4",END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)


config = {
    "configurable": {
        "thread_id": str(uuid.uuid4()),
    }
}

graph.invoke({"origin_input":1},config = config)

states = list(graph.get_state_history(config))

for i ,state in enumerate(states):
    print(f" {i}. 下一步节点: {state.next}")
    print(f"    检查点ID: {state.config['configurable']['checkpoint_id']}")
    if state.values:
        print(f"    状态值: {state.values}")
    print()

midway_state = states[2]
print(f"midway state: {midway_state}")
print(f"选中的状态: {midway_state.next}")
print(f"选中的状态值: {midway_state.values}")

new_config = graph.update_state(
    midway_state.config,
    values={"process_2": 5}
)
print(f"新配置: {new_config}")

output2 = graph.invoke(None,new_config)
print(output2)