from state import *
def odd_even_judgment(state:OverallState) -> OverallState:
    user_input = state['user_input']
    if(user_input % 2 == 0):
        even = True
        odd = False
    else:
        even = False
        odd = True
    return {"even":even, "odd":odd}

def odd_judgment(state:OverallState) -> OverallState:
    print("奇数")

def even_judgment(state:OverallState) -> OverallState:
    print("偶数")

def double_process(state:OverallState) -> OverallState:
    user_input = state['user_input']
    user_input = user_input + user_input
    print(f'翻倍后是{user_input}')
    return {"user_input":user_input}

def one_plus_process(state:OverallState) -> OverallState:
    user_input = state['user_input']
    user_input = user_input + 1
    print(f'加1后是{user_input}')
    return {"user_input":user_input}