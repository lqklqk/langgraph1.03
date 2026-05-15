from state import OverallState


def process_1_node(state:OverallState) -> OverallState:
    original_input = state["origin_input"]
    process_1 = original_input +1
    return {"process_1":process_1}

def process_2_node(state:OverallState) -> OverallState:
    process_2 = state["process_1"] +1
    return {"process_2":process_2}

def process_3_node(state:OverallState) -> OverallState:
    process_3 = state["process_2"] +1
    return {"process_3":process_3}

def process_4_node(state:OverallState) -> OverallState:
    process_4 = state["process_3"] +1
    return {"process_4":process_4}
