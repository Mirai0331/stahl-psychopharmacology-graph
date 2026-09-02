"""结果导出器：生成清晰 Markdown、JSON 知识库与 RAG Chunks"""
import json
from pathlib import Path
from typing import Dict, Any, List
from stahl_document_ai.processors.response_parser import ParsedDocument
from stahl_document_ai.processors.psychopharmacology_extractor import (
    PsychopharmacologyKnowledgeBase,
    PsychopharmacologyExtractor,
)


class DocumentExporter:
    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.md_dir = self.output_dir / "markdown_chapters"
        self.md_dir.mkdir(exist_ok=True)

    def export_full_markdown(self, parsed_doc: ParsedDocument, filename: str = "stahl_full.md") -> Path:
        """导出整合版 Markdown 文件"""
        target = self.output_dir / filename
        with open(target, "w", encoding="utf-8") as f:
            f.write("# Stahl 精神药理学精要：神经科学基础与实践应用（第5版）\n\n")
            for page in parsed_doc.pages:
                f.write(f"\n\n<!-- Page {page.page_number} Start -->\n\n")
                f.write(f"### [第 {page.page_number} 页]\n\n")
                
                # 写入页面主要文本与段落
                for p in page.paragraphs:
                    p_clean = p.strip()
                    if p_clean.startswith("图 ") or p_clean.startswith("图") or "Figure " in p_clean:
                        f.write(f"> 🖼️ **{p_clean}**\n\n")
                    else:
                        f.write(f"{p_clean}\n\n")
                
                # 写入表格
                for t in page.tables:
                    f.write("\n" + t.to_markdown() + "\n\n")
                    
                f.write(f"<!-- Page {page.page_number} End -->\n")
        return target

    def export_knowledge_base_json(
        self, kb: PsychopharmacologyKnowledgeBase, filename: str = "psychopharmacology_kb.json"
    ) -> Path:
        """导出结构化精神药理学知识库 JSON"""
        target = self.output_dir / filename
        with open(target, "w", encoding="utf-8") as f:
            json.dump(kb.model_dump(), f, ensure_ascii=False, indent=2)
        return target

    def export_rag_chunks_jsonl(
        self, parsed_doc: ParsedDocument, filename: str = "rag_chunks.jsonl"
    ) -> Path:
        """导出适合 RAG 检索的带元数据 Chunk 数据集"""
        target = self.output_dir / filename
        with open(target, "w", encoding="utf-8") as f:
            chunk_id = 0
            for page in parsed_doc.pages:
                analysis = PsychopharmacologyExtractor.analyze_page(page)
                
                # 按段落或每2个段落作为一个 Chunk
                for p in page.paragraphs:
                    if len(p.strip()) < 15:
                        continue
                    
                    chunk_item = {
                        "chunk_id": f"chunk_{chunk_id:05d}",
                        "page_number": page.page_number,
                        "text": p.strip(),
                        "metadata": {
                            "book": "Stahl精神药理学精要 第5版",
                            "receptors": [r for r in analysis["receptors"] if r.lower() in p.lower()],
                            "drugs": [d for d in analysis["drugs"] if d in p],
                            "is_figure_caption": p.strip().startswith("图 ") or p.strip().startswith("图"),
                        }
                    }
                    f.write(json.dumps(chunk_item, ensure_ascii=False) + "\n")
                    chunk_id += 1
        return target
