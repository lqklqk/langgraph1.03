from typing import TypedDict

class InputState(TypedDict):
    calc_output: int

class OutputState(TypedDict):
    calc_output: int

class OverAllState(TypedDict):
    original_input: int
