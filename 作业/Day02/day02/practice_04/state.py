from typing import List, Annotated

from langgraph.graph import add_messages
from typing_extensions import TypedDict

class OverAllState (TypedDict):
    scores : List[int]
    level : Annotated[List[str], add_messages]
