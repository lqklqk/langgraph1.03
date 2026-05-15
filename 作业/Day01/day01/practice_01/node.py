from state import InputState, OutputState
from state import OverAllState

def calc_node(state:OverAllState) -> InputState:
    original_input = state['original_input']
    calc_output = pow(original_input, 2)
    return {"calc_output": calc_output}

def output_node(state:OutputState) :
    print(state['calc_output'])
    return