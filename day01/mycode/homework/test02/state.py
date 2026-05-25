

from typing import TypedDict


class OverallState(TypedDict):
    calc_result: int
    
class InputState(TypedDict):
    input: int 
    
class OutputState(TypedDict):
    output: int