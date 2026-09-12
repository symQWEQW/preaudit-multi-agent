# 🕸️ 某地 AI 预审 · LangGraph 多智能体协作

> 对齐楚天云 JD（LangChain / LangGraph / Spring AI，Dify 优先）——把单链 AI 预审拆为 Planner / Retriever / Auditor 三智能体协作，无依赖时自动回退顺序模式。

![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

> **对齐目标 JD**：楚天云「大模型算法研发工程师」明确要求 *LangChain/LangGraph/Spring AI，有 Dify 源码研究经验者优先*。
> 本仓库把某地「AI 预审」从 Dify 单工作流升级为 **LangGraph 多 Agent 协作**，直接命中该 JD。

## 三个 Agent 协作

1. **Planner（规划 Agent）**：从患者问题中识别病种，拆解需核对材料清单
2. **Retriever（检索 Agent）**：按病种检索对应政策标准
3. **Auditor（审核 Agent）**：综合材料与政策，输出结构化预审结论

## 为什么是「多 Agent」而非「单链」

- 职责解耦：病种识别 / 政策检索 / 合规审核独立优化、可替换
- 可观测：每步输入输出可记录、评估、重试
- 可扩展：后续加申诉 Agent、人工复核 Agent，复用同一图
- 工程化：比 Dify 拖拽更可控，适合复杂政务合规场景

## 目录结构

```
jiangling-multi-agent/
├── README.md
├── requirements.txt
├── multi_agent.py      # LangGraph 编排 + 三个 Agent（含无依赖回退模式）
└── docs/
    └── flow.md         # 流程图 + 各 Agent 职责
```

## 快速运行

```bash
pip install -r requirements.txt
python multi_agent.py
```

> 未安装 `langgraph` 时会自动回退到顺序执行模式（多 Agent 协作逻辑完全一致），
> 可直接 `python multi_agent.py` 看效果，无需任何外部依赖。

## 与某地主项目的关系

| 仓库 | 角色 | 技术 |
|---|---|---|
| jiangling-ai-preaudit | RAG 核心 + 评估（AI 工程作品） | TF-IDF/Milvus + Ollama |
| **jiangling-multi-agent** | 多 Agent 编排（命中楚天云 JD） | **LangGraph** |
| medical-lora-finetune | 原理级微调（差异化证据） | LoRA/PEFT |

三者共同构成「AI 应用落地工程师」作品集：会做应用、会编排 Agent、也懂模型原理。

## License

MIT（演示用途，逻辑为 mock，可接真实 LLM / 政策库）。
