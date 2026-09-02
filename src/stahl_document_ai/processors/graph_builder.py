"""精神药理学知识图谱构建引擎（从 graph_data.json 加载 100% 全连通数据）"""
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class GraphNode:
    id: str
    label: str
    category: str
    description: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    target: str
    relationship: str
    label: str
    description: str = ""
    weight: float = 1.0


@dataclass
class PsychopharmacologyKnowledgeGraph:
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "categories": list(set(n.category for n in self.nodes)),
                "relationships": list(set(e.relationship for e in self.edges)),
            }
        }


class StahlKnowledgeGraphBuilder:
    @classmethod
    def build_comprehensive_graph(cls) -> PsychopharmacologyKnowledgeGraph:
        data_path = Path(__file__).parent / "graph_data.json"
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        nodes = [
            GraphNode(
                id=n["id"],
                label=n["label"],
                category=n["category"],
                description=n.get("description", ""),
                properties=n.get("properties", {})
            )
            for n in data.get("nodes", [])
        ]

        edges = [
            GraphEdge(
                source=e["source"],
                target=e["target"],
                relationship=e["relationship"],
                label=e["label"],
                description=e.get("description", ""),
                weight=float(e.get("weight", 1.0))
            )
            for e in data.get("edges", [])
        ]

        return PsychopharmacologyKnowledgeGraph(nodes=nodes, edges=edges)