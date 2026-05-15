from state import OverAllState
from langgraph.types import Command
def calc_node(state:OverAllState) :
    original_input = state['original_input']
    odd_judge = original_input % 2 != 0

    if odd_judge:
        return Command(
            update ={
                "odd": True,
                "even": False
            },
            goto="odd_node"
        )
    else:
        return Command(
            update ={
                "odd": False,
                "even": True
            },
            goto="even_node"
        )

def odd_node(state:OverAllState) :
    print("奇数状态是： " + str(state['odd']) + ", 偶数状态是： " + str(state['even']))
    return

def even_node(state:OverAllState) :
    print("奇数状态是： " + str(state['odd']) + ", 偶数状态是： " + str(state['even']))
    return

def add_calc(state:OverAllState) :
    add_result = state['original_input'] + 2
    print("加2结果是： "+ str(add_result))
    return {"add_result": add_result}

def mul_calc(state:OverAllState) :
    mul_result = state['original_input'] * 2
    print("乘2结果是： "+ str(mul_result))
    return {"mul_result": mul_result}

def sub_calc(state:OverAllState) :
    sub_result = state['original_input'] - 2
    print("减2结果是： "+ str(sub_result))
    return {"sub_result": sub_result}

def div_calc(state:OverAllState) :
    div_result = state['original_input'] / 2
    print("除以2结果是： "+ str(div_result))
    return {"div_result": div_result}