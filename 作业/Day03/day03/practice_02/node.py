from langgraph.types import interrupt

from state import OverallState

def input_interrupt_node(state: OverallState) -> OverallState:
    print("进入中断输入节点")
    updated = interrupt({
        "instruction": "请审阅并编辑以下内容",
        "content": state["original_input"],
    })

    print(f"收到编辑后的内容: {updated}")
    return {"interrupt_input": updated}

def output_node(state:OverallState) -> OverallState:
    original_input = state["original_input"]
    interrupt_input = state["interrupt_input"]
    print("原始输入内容： "+ original_input)
    print("中断输入内容： "+ interrupt_input)
    return