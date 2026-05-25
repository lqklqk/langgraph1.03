from state import InputState, OutputState, OverallState

def calc(state:InputState) -> OverallState:
    input = state.get("input")
    calc_result = input ** 2
    result = {"calc_result": calc_result}
    return result

def output(state: OverallState) -> OutputState:
    calc_result = state.get("calc_result")
    print(f"output 节点打印结果：{calc_result}")
    result = {"output": calc_result}
    return result
