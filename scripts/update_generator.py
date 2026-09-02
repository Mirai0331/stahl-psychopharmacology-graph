# -*- coding: utf-8 -*-
"""同步更新脚本与生成器模板"""
from stahl_document_ai.processors.interactive_graph_generator import InteractiveGraphGenerator
from stahl_document_ai.processors.graph_builder import PsychopharmacologyKnowledgeGraph
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data_path = root / "output" / "knowledge_graph.json"
out_html = root / "output" / "interactive_graph.html"

if data_path.exists():
    kg_dict = json.loads(data_path.read_text(encoding="utf-8"))
    kg = PsychopharmacologyKnowledgeGraph.parse_obj(kg_dict)
    InteractiveGraphGenerator.generate_html(kg, out_html)
    print(f"[OK] 成功使用最新立体化生成器更新: {out_html}")
else:
    print(f"[WARN] 数据文件不存在: {data_path}")
