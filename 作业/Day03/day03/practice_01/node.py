from state import OverallState,SubgraphState

def node_1(state: SubgraphState) -> SubgraphState:
    print("正在设置node_1状态信息")
    return {"node_1_state":"completed"}

def node_2(state: SubgraphState) -> SubgraphState:
    print("正在设置node_2状态信息")
    return {"node_2_state":"completed"}

def node_3(state: SubgraphState) -> SubgraphState:
    print("正在设置node_3状态信息")
    return {"node_3_state":"completed"}

def output_node(state: OverallState) -> OverallState:
    print("此为主流程的输出处理节点")
    return state