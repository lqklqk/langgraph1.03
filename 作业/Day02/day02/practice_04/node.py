from random import random

from state import OverAllState


# 生成成绩列表的节点
def generate_scores(state : OverAllState) -> dict:
    score_list = [50,70,40,100,59]
    return {"scores" : score_list}

# 为每个分数生成评级
def generate_level(state : OverAllState) -> dict:
    score = state.get("score",0)
    print("正在处理分析成绩： " + str(score))
    if score >= 60:
        level ="成绩为： "+ str(score) + "分，及格"
    else:
        level ="成绩为： "+ str(score) + "分，不及格"
    print(level)
    return {"level" : level}
