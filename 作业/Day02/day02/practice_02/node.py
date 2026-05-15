from state import OverAllState
from langgraph.types import Command
def calc_node(state:OverAllState) :
    original_input = state["original_input"]
    calc_reuslt = original_input * 2
    return {"calc_result": calc_reuslt}

def output_node(state:OverAllState) :
    original_input = state["original_input"]
    calc_reuslt = state["calc_result"]
    print("原始输入是： "+ str(original_input) + " 乘2计算结果是 " + str(calc_reuslt))