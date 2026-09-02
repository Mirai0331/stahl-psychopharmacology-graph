# -*- coding: utf-8 -*-
"""端到端与各模块功能测试（全书 14 章全景知识图谱 + 前沿新药）"""
import json
import pytest
from pathlib import Path
from stahl_document_ai.processors.pdf_splitter import PDFSplitter
from stahl_document_ai.processors.graph_builder import StahlKnowledgeGraphBuilder
from stahl_document_ai.processors.interactive_graph_generator import InteractiveGraphGenerator
from stahl_document_ai.processors.obsidian_exporter import ObsidianVaultExporter

PDF_PATH = r"G:\4.文档\医学相关\Stahl精神药理学精要：神经科学基础与实践应用 第5版中译稿 (Stephen M. Stahl) (Z-Library).pdf"


def test_pdf_splitter():
    splitter = PDFSplitter(PDF_PATH)
    assert splitter.get_total_pages() == 537
    chunk = splitter.render_page_to_image(1, dpi=100)
    assert chunk.page_number == 1
    assert chunk.mime_type == "image/png"
    assert len(chunk.image_bytes) > 0


def test_knowledge_graph_builder(tmp_path):
    graph = StahlKnowledgeGraphBuilder.build_comprehensive_graph()
    assert len(graph.nodes) >= 185
    assert len(graph.edges) >= 380

    # 验证无任何孤立节点 (0 isolated nodes)
    degrees = {n.id: 0 for n in graph.nodes}
    for e in graph.edges:
        degrees[e.source] = degrees.get(e.source, 0) + 1
        degrees[e.target] = degrees.get(e.target, 0) + 1
    assert all(deg > 0 for deg in degrees.values()), "存在孤立节点！"

    # 验证前沿与新修正实体
    node_labels = [n.label for n in graph.nodes]
    assert any("替洛利生" in l for l in node_labels)
    assert any("利右苯丙胺" in l for l in node_labels)
    assert any("法赞雷生" in l for l in node_labels)
    assert any("沃诺雷生" in l for l in node_labels)
    assert any("地达西尼" in l for l in node_labels)
    assert any("乌洛他隆" in l for l in node_labels)
    assert any("佐拉诺酮" in l for l in node_labels)
    assert any("仑卡奈单抗" in l for l in node_labels)
    assert any("托鲁地文拉法辛" in l for l in node_labels)
    assert any("艾司氯胺酮" in l for l in node_labels)
    assert any("卢美哌隆" in l for l in node_labels)

    # 验证 3D HTML 图谱生成
    html_file = tmp_path / "interactive_graph.html"
    InteractiveGraphGenerator.generate_html(graph, html_file)
    assert html_file.exists()
    html_content = html_file.read_text(encoding="utf-8")
    assert "法赞雷生" in html_content
    assert "地达西尼" in html_content
    assert "替洛利生" in html_content
    assert "卢美哌隆" in html_content
    assert "3d-force-graph" in html_content
    assert "three-spritetext" in html_content

    # 验证 Obsidian 知识库生成
    vault_dir = ObsidianVaultExporter.export_vault(graph, tmp_path)
    assert vault_dir.exists()
    index_file = vault_dir / "00_Stahl精神药理学精要_总索引.md"
    assert index_file.exists()
    index_text = index_file.read_text(encoding="utf-8")
    assert "[[地达西尼]]" in index_text
    assert "[[法赞雷生]]" in index_text
    assert "[[卢美哌隆]]" in index_text
