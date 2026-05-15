from asyncio import sleep
from state import OverAllState

def node_1 (state:OverAllState) -> OverAllState:
    print(f'Adding "node_1" to {state["node_process_list"]}')
    return({"node_process_list":["node_1"]})

def node_2 (state:OverAllState) -> OverAllState:
    print(f'Adding "node_2" to {state["node_process_list"]}')
    return({"node_process_list":["node_2"]})

def node_3 (state:OverAllState) -> OverAllState:
    print(f'Adding "node_3" to {state["node_process_list"]}')
    return({"node_process_list":["node_3"]})

def node_4 (state:OverAllState) -> OverAllState:
    print(f'Adding "node_4" to {state["node_process_list"]}')
    return({"node_process_list":["node_4"]})

def node_5 (state:OverAllState) -> OverAllState:
    print(f'Adding "node_5" to {state["node_process_list"]}')
    return({"node_process_list":["node_5"]})

def node_6 (state:OverAllState) -> OverAllState:
    print(f'Adding "node_6" to {state["node_process_list"]}')
    return({"node_process_list":["node_6"]})