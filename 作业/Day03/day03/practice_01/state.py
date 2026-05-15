from typing import TypedDict


class OverallState(TypedDict):
    original_input: str

class SubgraphState(TypedDict):
    original_input: str
    node_1_state:str
    node_2_state:str
    node_3_state:str