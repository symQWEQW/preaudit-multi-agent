"""江陵 AI 预审 · 多 Agent 协作（LangGraph 实现）。

三个 Agent 协作完成慢特病预审：
  1) Planner（规划 Agent）：从患者问题中识别病种，拆解需要核对的材料清单
  2) Retriever（检索 Agent）：按病种检索对应政策标准
  3) Auditor（审核 Agent）：综合材料与政策，输出结构化预审结论

依赖：langgraph, langchain（pip install -r requirements.txt）
未安装 langgraph 时自动回退到顺序执行模式（逻辑完全一致），便于无依赖演示。

对应目标 JD：楚天云「大模型算法研发工程师」明确要求 LangChain/LangGraph/Spring AI，Dify 优先。
"""
from typing import TypedDict, Annotated

# ---- 在无 langgraph 环境下优雅回退 ----
try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    print("[提示] 未检测到 langgraph，已回退到顺序执行模式（多 Agent 协作逻辑一致）。")


class State(TypedDict):
    query: str
    disease: str
    materials: str
    policy: str
    conclusion: str
    messages: Annotated[list, "add_messages"] if HAS_LANGGRAPH else list


# ---- Agent 1：规划 ----
def planner(state: State) -> dict:
    q = state["query"]
    if "高血压" in q:
        disease = "高血压"
    elif "糖尿病" in q:
        disease = "糖尿病"
    elif "恶性肿瘤" in q or "癌症" in q:
        disease = "恶性肿瘤"
    else:
        disease = "未知"
    # 模拟从患者上传材料中提取的关键字段
    materials = (
        f"[{disease}] 已提取材料：诊断证明、病历、检验单、血压/血糖记录（mock）"
        if disease != "未知" else "无法识别病种，需人工介入"
    )
    return {"disease": disease, "materials": materials}


# ---- Agent 2：检索 ----
POLICY_DB = {
    "高血压": "认定标准：非药物状态下同日三次收缩压≥140mmHg 和/或舒张压≥90mmHg；"
              "材料：诊断证明、近半年病历、三次血压记录、医保凭证。",
    "糖尿病": "认定标准：空腹≥7.0 或 餐后≥11.1 或 糖化血红蛋白≥6.5%（两次不同日期）；"
              "材料：诊断证明、血糖与糖化报告、胰岛素记录。",
    "恶性肿瘤": "认定标准：病理/细胞学确诊，或影像+肿瘤标志物确诊；"
                "材料：三级医院病理报告、影像报告、治疗方案。",
}


def retriever(state: State) -> dict:
    return {"policy": POLICY_DB.get(state["disease"], "未找到对应病种政策")}


# ---- Agent 3：审核 ----
def auditor(state: State) -> dict:
    if state["disease"] == "未知":
        return {"conclusion": "⚠️ 病种识别失败，转人工窗口复核。"}
    conclusion = (
        f"【{state['disease']} 预审结论】\n"
        f"- 材料核对：{state['materials']}\n"
        f"- 政策依据：{state['policy']}\n"
        f"- 初步判定：材料齐备且符合认定标准，建议进入窗口 PC 端复核 → 短信通知患者。"
    )
    return {"conclusion": conclusion}


# ---- 图编排 ----
def build_graph():
    g = StateGraph(State)
    g.add_node("planner", planner)
    g.add_node("retriever", retriever)
    g.add_node("auditor", auditor)
    g.set_entry_point("planner")
    g.add_edge("planner", "retriever")
    g.add_edge("retriever", "auditor")
    g.add_edge("auditor", END)
    return g.compile()


def run_sequential(state: State) -> State:
    """无 langgraph 时的等价顺序实现。"""
    s = dict(state)
    s.update(planner(s))
    s.update(retriever(s))
    s.update(auditor(s))
    return s


def invoke(query: str) -> dict:
    init = {"query": query, "disease": "", "materials": "",
            "policy": "", "conclusion": "", "messages": []}
    if HAS_LANGGRAPH:
        app = build_graph()
        return app.invoke(init)
    return run_sequential(init)


if __name__ == "__main__":
    demo_query = "高血压患者申请慢特病认定需要准备哪些材料？"
    result = invoke(demo_query)
    print(f"问题：{demo_query}\n")
    print(result["conclusion"])
