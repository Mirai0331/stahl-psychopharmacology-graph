# -*- coding: utf-8 -*-
"""同步更新脚本与 3D 生成器模板"""
import json
from pathlib import Path
from stahl_document_ai.processors.interactive_graph_generator import InteractiveGraphGenerator
from stahl_document_ai.processors.graph_builder import StahlKnowledgeGraphBuilder

root = Path(__file__).resolve().parent.parent
out_html = root / "output" / "interactive_graph.html"

graph = StahlKnowledgeGraphBuilder.build_comprehensive_graph()
InteractiveGraphGenerator.generate_html(graph, out_html)
print(f"[OK] 成功使用 3D 立体化生成器更新: {out_html}")

