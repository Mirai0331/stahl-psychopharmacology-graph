"""生成适配 Obsidian 的双向链接 Markdown 知识库（支持 Windows 安全文件名）"""
import re
from pathlib import Path
from typing import Dict, Any, List
from stahl_document_ai.processors.graph_builder import PsychopharmacologyKnowledgeGraph


def sanitize_filename(name: str) -> str:
    """清理 Windows 限制的文件名非法字符"""
    return re.sub(r'[\\/*?:"<>|]', '_', name.strip())


class ObsidianVaultExporter:
    """导出结构化、带 [[双向链接]] 的 Markdown 知识库"""

    @classmethod
    def export_vault(cls, graph: PsychopharmacologyKnowledgeGraph, output_dir: Path) -> Path:
        vault_dir = output_dir / "obsidian_vault"
        vault_dir.mkdir(parents=True, exist_ok=True)

        dir_receptors = vault_dir / "01_受体与靶点"
        dir_drugs = vault_dir / "02_药物机制与临床"
        dir_pathways = vault_dir / "03_神经通路与脑区"
        dir_diseases = vault_dir / "04_疾病与不良反应"

        for d in [dir_receptors, dir_drugs, dir_pathways, dir_diseases]:
            d.mkdir(exist_ok=True)

        # 构建邻接关系索引
        incoming: Dict[str, List[Dict[str, Any]]] = {}
        outgoing: Dict[str, List[Dict[str, Any]]] = {}
        for edge in graph.edges:
            outgoing.setdefault(edge.source, []).append(edge)
            incoming.setdefault(edge.target, []).append(edge)

        nodes_map = {n.id: n for n in graph.nodes}

        # 1. 导出受体与靶点卡片
        for node in graph.nodes:
            if node.category == "Receptor":
                clean_name = sanitize_filename(node.label.split()[0])
                file_path = dir_receptors / f"{clean_name}.md"
                content = [
                    "---",
                    f"id: {node.id}",
                    f"title: {node.label}",
                    f"category: {node.category}",
                    f"tags: [受体靶点, 精神药理学, {node.properties.get('type', 'GPCR')}]",
                    "---\n",
                    f"# {node.label}\n",
                    f"> **受体/靶点类型**：`{node.properties.get('type', 'GPCR')}`\n",
                    f"## 📌 神经生物学与生理功能\n{node.description}\n",
                    "## 🔗 靶向该受体的相关药物与作用模式",
                ]
                
                acting_drugs = incoming.get(node.id, [])
                if acting_drugs:
                    content.append("| 药物 | 作用模式 (Action) | 药理学效应与临床意义 |")
                    content.append("| --- | --- | --- |")
                    for edge in acting_drugs:
                        src_node = nodes_map.get(edge.source)
                        if src_node and src_node.category == "Drug":
                            clean_drug = sanitize_filename(src_node.label.split()[0])
                            content.append(f"| [[{clean_drug}]] | `{edge.label}` | {edge.description or '—'} |")
                else:
                    content.append("暂无直接靶向药物记录。")

                file_path.write_text("\n".join(content), encoding="utf-8")

        # 2. 导出药物机制卡片
        for node in graph.nodes:
            if node.category == "Drug":
                clean_name = sanitize_filename(node.label.split()[0])
                file_path = dir_drugs / f"{clean_name}.md"
                content = [
                    "---",
                    f"id: {node.id}",
                    f"title: {node.label}",
                    f"category: {node.category}",
                    "tags: [精神药物, 临床药理学]",
                    "---\n",
                    f"# {node.label}\n",
                    f"## 📋 药物机制概览与临床定位\n{node.description}\n",
                    "## 🎯 受体结合与药理机制谱 (Binding Profile)",
                ]

                out_edges = outgoing.get(node.id, [])
                receptor_edges = [e for e in out_edges if nodes_map.get(e.target, None) and nodes_map[e.target].category == "Receptor"]
                if receptor_edges:
                    content.append("| 靶点受体/转运体 | 作用方式 (Action) | 机制效应 |")
                    content.append("| --- | --- | --- |")
                    for e in receptor_edges:
                        rec_node = nodes_map[e.target]
                        rec_clean = sanitize_filename(rec_node.label.split()[0])
                        content.append(f"| [[{rec_clean}]] | `{e.label}` | {e.description} |")

                # 适应症
                treat_edges = [e for e in out_edges if e.relationship == "TREATS"]
                if treat_edges:
                    content.append("\n## 🏥 主要临床适应症")
                    for e in treat_edges:
                        dis_node = nodes_map[e.target]
                        dis_clean = sanitize_filename(dis_node.label.split()[0])
                        content.append(f"- [[{dis_clean}]]：{e.description}")

                # 副作用
                se_edges = [e for e in out_edges if e.relationship == "CAUSES"]
                if se_edges:
                    content.append("\n## ⚠️ 重点不良反应与安全监测")
                    for e in se_edges:
                        se_node = nodes_map[e.target]
                        se_clean = sanitize_filename(se_node.label.split()[0])
                        content.append(f"- **[[{se_clean}]]**：{e.description}")

                file_path.write_text("\n".join(content), encoding="utf-8")

        # 3. 导出神经通路卡片
        for node in graph.nodes:
            if node.category == "Pathway":
                clean_name = sanitize_filename(node.label.split()[0])
                file_path = dir_pathways / f"{clean_name}.md"
                content = [
                    "---",
                    f"id: {node.id}",
                    f"title: {node.label}",
                    f"category: {node.category}",
                    "tags: [神经环路, 脑区功能]",
                    "---\n",
                    f"# {node.label}\n",
                    f"## 🧠 环路解剖与生理功能\n{node.description}\n",
                    f"> **主要递质网络**：`{node.properties.get('neurotransmitter', 'Dopamine')}`\n",
                ]
                file_path.write_text("\n".join(content), encoding="utf-8")

        # 4. 导出疾病与不良反应卡片
        for node in graph.nodes:
            if node.category in ["Disease", "SideEffect"]:
                clean_name = sanitize_filename(node.label.split()[0])
                file_path = dir_diseases / f"{clean_name}.md"
                content = [
                    "---",
                    f"id: {node.id}",
                    f"title: {node.label}",
                    f"category: {node.category}",
                    "tags: [疾病与症状, 精神医学]",
                    "---\n",
                    f"# {node.label}\n",
                    f"## 🩺 临床表征与病理机制\n{node.description}\n",
                ]
                file_path.write_text("\n".join(content), encoding="utf-8")

        # 5. 生成全书主索引 Index.md
        index_file = vault_dir / "00_Stahl精神药理学精要_总索引.md"
        index_content = [
            "# 📚 Stahl 精神药理学精要 · 双向链接知识库总览\n",
            "> 基于《Stahl's Essential Psychopharmacology 5th Edition》构建\n",
            "## 💊 核心药物列表",
            ", ".join([f"[[{sanitize_filename(n.label.split()[0])}]]" for n in graph.nodes if n.category == "Drug"]),
            "\n## 🧬 核心受体与靶点列表",
            ", ".join([f"[[{sanitize_filename(n.label.split()[0])}]]" for n in graph.nodes if n.category == "Receptor"]),
            "\n## 🧠 神经通路与认知环路",
            ", ".join([f"[[{sanitize_filename(n.label.split()[0])}]]" for n in graph.nodes if n.category == "Pathway"]),
            "\n## 🏥 精神疾病与症状谱",
            ", ".join([f"[[{sanitize_filename(n.label.split()[0])}]]" for n in graph.nodes if n.category == "Disease"]),
        ]
        index_file.write_text("\n".join(index_content), encoding="utf-8")

        return vault_dir