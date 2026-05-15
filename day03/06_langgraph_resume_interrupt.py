from typing import TypedDict, Optional, Literal
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt


class ApprovalState(TypedDict):
    action_details:str
    status:Optional[Literal["pending","approved","rejected"]]

# 审批节点
def approval_node(state:ApprovalState) -> Command[Literal["proceed","cancel"]]:
    print(f"执行节点: approval_node")
    print(f"操作详情: {state['action_details']}")
    print("工作流暂停，等待用户审批...")

    decision = interrupt(
        {
            "question":"批准此操作吗",
            "details":state["action_details"]
        }
    )
    next_node = "proceed" if decision else "cancel"
    print(f"审批决定：{'批准' if decision else '拒绝'}，路由到节点{next_node}")

    return(Command(goto = next_node))

def proceed_node(state:ApprovalState):
    print("执行节点: proceed_node")
    print("操作已被批准，正在执行...")
    return {"status":"approved"}

def cancel_node(state:ApprovalState):
    print("执行节点: cancel_node")
    print("操作不被批准，不许执行...")
    return {"status":"rejecter"}

builder = StateGraph(ApprovalState)
builder.add_node("approval",approval_node)
builder.add_node("proceed",proceed_node)
builder.add_node("cancel",cancel_node)

# 添加边
builder.add_edge(START,"approval")
builder.add_edge("proceed",END)
builder.add_edge("cancel",END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "approval-123"}}

print("首次启动工作流")

# input ={"action_details": "转账 $500", "status": "pending"}
initial = graph.invoke(
        {"action_details": "转账 $500", "status": "pending"},
        config=config,
    )


# 显示中断信息
print(f"工作流中断信息: {initial['__interrupt__']}\n")

# 获取用户输入
while True:
    user_input = input("\n请输入审批决定 (y/n): ").strip().lower()
    if user_input in ['y', 'yes', '是']:
        decision = True
        break
    elif user_input in ['n', 'no', '否']:
        decision = False
        break
    else:
        print("无效输入，请输入 y/yes/是 或 n/no/否")

# 获取用户输入
resumed = graph.invoke(Command(resume=decision),config=config)

# 显示最终结果
print(f"最终状态: {resumed}")
print(f"操作状态: {resumed['status']}")
print("\n=== 演示完成 ===")
