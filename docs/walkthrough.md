# 《Stahl精神药理学精要》以相互关系为证据连接交付报告

已为您完成**实体类别以相互关系为证据紧密连接（Evidence-Linked Subgraph Generator）**的全面升级！

彻底消除了以往单纯类别过滤时造成的“零连线孤立点”问题。现在点击任何实体类别，系统都会自动以该类别为核心，**将与它们直接发生药理作用的所有靶点、环路、疾病及机制连线全部作为证据网络紧密连接在一起呈现**！

最新产物已推送到 GitHub 远程仓库 **`P·L·A·N·A`** 分支！

---

## 1. 🧬 核心机制升级：以相互关系为证据闭环连接

```mermaid
graph LR
  subgraph 实体类别证据网络 (以受体为例)
    REC(("🎯 核心受体<br/>(如 5-HT1A, D2, NMDA)"))
    DRUG["💊 作用药物<br/>(如 艾司氯胺酮, 地达西尼)"]
    PATH["⚡ 级联通路<br/>(如 海马突触可塑性)"]
    DIS["🩺 适应症表型<br/>(如 难治抑郁 TRD)"]
    
    DRUG -->|激动/拮抗/PAM/抑制| REC
    REC -->|级联驱动| PATH
    PATH -->|改善/逆转| DIS
    DRUG -->|临床治疗| DIS
  end
```

| 点击类别 | 呈现的证据连接网络 (无孤立节点) |
|---|---|
| **精神药物 (Drug)** | 呈现所有精神药物，**并自动连带拉出它们作用的受体靶点、调控回路与治疗疾病**，完整展示药物机制证据链！ |
| **受体与信号靶点 (Receptor)** | 呈现全书所有受体靶点，**并自动连带拉出作用于它们的全部药物、下游级联分子 (mTOR/BDNF) 与神经通路**！ |
| **神经通路与环路 (Pathway)** | 呈现全书主要神经环路（CSTC、中脑边缘、视交叉上核等），**并连带展示汇聚其上的受体与调控药物**！ |
| **疾病与表型 (Disease)** | 呈现难治性抑郁、自杀干预、失眠、ADHD、精神分裂症等，**并连带拉出针对该疾病的全部一线/突破性药物与靶点**！ |
| **不良反应 (SideEffect)** | 呈现锥体外系、高催乳素、镇静、成瘾耐受等，**并连带展示诱发它们的受体阻断证据**！ |

---

## 2. 🚀 远程 GitHub P·L·A·N·A 分支已同步

* 🌐 **GitHub 仓库链接（P·L·A·N·A 分支）**：
  👉 **`https://github.com/Mirai0331/stahl-psychopharmacology-graph/tree/P%C2%B7L%C2%B7A%C2%B7N%C2%B7A`**
* 🖥️ **本地交互图谱**：
  👉 [`output/interactive_graph.html`](file:///C:/Users/Kuriy/.gemini/antigravity/scratch/stahl_document_ai/output/interactive_graph.html)
