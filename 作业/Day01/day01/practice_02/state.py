from typing import TypedDict
from typing import Annotated, List
import operator

class OverAllState(TypedDict):
   node_process_list: Annotated[List, operator.add]
