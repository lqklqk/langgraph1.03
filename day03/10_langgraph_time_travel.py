
import uuid
from typing_extensions import TypedDict, NotRequired

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class StoryState(TypedDict):
    """故事状态定义"""
    character: NotRequired[str]
    setting: NotRequired[str]
    plot: NotRequired[str]
    ending: NotRequired[str]


def create_character(state: StoryState):
    """
    创建故事角色

    Args:
        state: 当前状态

    Returns:
        dict: 更新后的状态
    """
    print("执行节点: create_character")

    # 模拟LLM调用
    mock_character = "一只会说话的猫"
    print(f"创建的角色: {mock_character}")
    return {"character": mock_character}


def set_setting(state: StoryState):
    """
    设置故事背景

    Args:
        state: 当前状态

    Returns:
        dict: 更新后的状态
    """
    print("执行节点: set_setting")

    # 模拟LLM调用
    mock_setting = "在一个神秘的图书馆里"
    print(f"设置的背景: {mock_setting}")
    return {"setting": mock_setting}


def develop_plot(state: StoryState):
    """
    发展故事情节

    Args:
        state: 当前状态

    Returns:
        dict: 更新后的状态
    """
    print("执行节点: develop_plot")

    # 模拟LLM调用
    character = state.get("character", "未知角色")
    setting = state.get("setting", "未知背景")
    mock_plot = f"{character}在{setting}发现了一本会发光的书"
    print(f"发展的剧情: {mock_plot}")
    return {"plot": mock_plot}


def write_ending(state: StoryState):
    """
    编写故事结局

    Args:
        state: 当前状态

    Returns:
        dict: 更新后的状态
    """
    print("执行节点: write_ending")

    # 模拟LLM调用
    plot = state.get("plot", "未知剧情")
    mock_ending = f"当{plot}时，整个图书馆都被魔法光芒照亮了"
    print(f"编写的结局: {mock_ending}")
    return {"ending": mock_ending}

    # 构建工作流


workflow = StateGraph(StoryState)

# 添加节点
workflow.add_node("create_character", create_character)
workflow.add_node("set_setting", set_setting)
workflow.add_node("develop_plot", develop_plot)
workflow.add_node("write_ending", write_ending)

# 添加边来连接节点
workflow.add_edge(START, "create_character")
workflow.add_edge("create_character", "set_setting")
workflow.add_edge("set_setting", "develop_plot")
workflow.add_edge("develop_plot", "write_ending")
workflow.add_edge("write_ending", END)

# 编译
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

# 1. 运行图表生成第一个故事
print("1. 生成第一个故事...")
config1 = {
    "configurable": {
        "thread_id": str(uuid.uuid4()),
    }
}

story1 = graph.invoke({}, config1)
print(f"角色: {story1['character']}")
print(f"背景: {story1['setting']}")
print(f"剧情: {story1['plot']}")
print(f"结局: {story1['ending']}")
print()

# 2. 查看历史状态
print("2. 查看第一个故事的历史状态...")
states1 = list(graph.get_state_history(config1))

print("历史状态:")
for i, state in enumerate(states1):
    print(f"  {i}. 下一步节点: {state.next}")
    print(f"     检查点ID: {state.config['configurable']['checkpoint_id']}")
    if state.values:
        print(f"     状态值: {state.values}")
    print()

# 3. 从中间状态恢复执行，创建第二个故事
print("3. 从中间状态恢复执行，创建第二个故事...")

character_state = states1[2]  # 索引2对应set_setting执行后的状态
print(f"选中的状态: {character_state.next}")
print(f"选中的状态值: {character_state.values}")

# 更新状态，改变角色
new_config = graph.update_state(
    character_state.config,
    values={"character": "一只会飞的龙"}
)
print(f"新配置: {new_config}")
print()

# 4. 从新检查点恢复执行
print("4. 从新检查点恢复执行，生成第二个故事...")
story2 = graph.invoke(None, new_config)
print(f"新角色: {story2['character']}")
print(f"背景: {story2['setting']}")
print(f"剧情: {story2['plot']}")
print(f"结局: {story2['ending']}")
print()

# 5. 比较两个故事
print("5. 比较两个故事:")
print("  故事1:")
print(f"    角色: {story1['character']}")
print(f"    背景: {story1['setting']}")
print(f"    剧情: {story1['plot']}")
print(f"    结局: {story1['ending']}")
print()

print("  故事2:")
print(f"    角色: {story2['character']}")
print(f"    背景: {story2['setting']}")
print(f"    剧情: {story2['plot']}")
print(f"    结局: {story2['ending']}")
print()

print("=== 演示完成 ===")
