"""Document AI 响应数据解析与 Markdown 重建"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class ParsedTable:
    headers: List[str]
    rows: List[List[str]]
    page_number: int

    def to_markdown(self) -> str:
        if not self.headers and not self.rows:
            return ""
        
        col_count = max(len(self.headers), max((len(r) for r in self.rows), default=0))
        headers = self.headers + [""] * (col_count - len(self.headers))
        
        md_lines = []
        md_lines.append("| " + " | ".join(h.replace("\n", " ") for h in headers) + " |")
        md_lines.append("| " + " | ".join(["---"] * col_count) + " |")
        
        for row in self.rows:
            padded_row = row + [""] * (col_count - len(row))
            md_lines.append("| " + " | ".join(c.replace("\n", " ") for c in padded_row) + " |")
            
        return "\n".join(md_lines)


@dataclass
class ParsedPage:
    page_number: int  # 原始文档全局页码
    raw_text: str
    paragraphs: List[str] = field(default_factory=list)
    tables: List[ParsedTable] = field(default_factory=list)
    figure_captions: List[str] = field(default_factory=list)


@dataclass
class ParsedDocument:
    full_text: str
    pages: List[ParsedPage] = field(default_factory=list)


class DocumentAIResponseParser:
    """解析 Google Cloud Document AI API 返回的 document 字典"""

    @staticmethod
    def _get_text_from_anchor(full_text: str, text_anchor: Optional[Dict[str, Any]]) -> str:
        if not text_anchor or "textSegments" not in text_anchor:
            return ""
        
        extracted = []
        for segment in text_anchor.get("textSegments", []):
            start = int(segment.get("startIndex", 0))
            end = int(segment.get("endIndex", len(full_text)))
            extracted.append(full_text[start:end])
        return "".join(extracted).strip()

    @classmethod
    def parse_process_response(
        cls,
        response_data: Dict[str, Any],
        global_page_offset: int = 0
    ) -> ParsedDocument:
        """
        解析 Document AI process 接口返回的字典
        global_page_offset: 全局页码偏移量（例如 chunk 起始页码 - 1）
        """
        doc = response_data.get("document", response_data)
        full_text = doc.get("text", "")
        pages_data = doc.get("pages", [])

        parsed_pages: List[ParsedPage] = []

        for page in pages_data:
            local_page_num = page.get("pageNumber", 1)
            actual_page_num = local_page_num + global_page_offset

            # 1. 提取段落
            paragraphs = []
            for p in page.get("paragraphs", []):
                p_text = cls._get_text_from_anchor(full_text, p.get("layout", {}).get("textAnchor"))
                if p_text:
                    paragraphs.append(p_text)

            # 如果没有段落层级，回退到 blocks 或 lines
            if not paragraphs:
                for b in page.get("blocks", []):
                    b_text = cls._get_text_from_anchor(full_text, b.get("layout", {}).get("textAnchor"))
                    if b_text:
                        paragraphs.append(b_text)

            # 2. 提取表格
            parsed_tables = []
            for table in page.get("tables", []):
                headers = []
                for h_row in table.get("headerRows", []):
                    for cell in h_row.get("cells", []):
                        cell_text = cls._get_text_from_anchor(full_text, cell.get("layout", {}).get("textAnchor"))
                        headers.append(cell_text)

                rows = []
                for b_row in table.get("bodyRows", []):
                    row_cells = []
                    for cell in b_row.get("cells", []):
                        cell_text = cls._get_text_from_anchor(full_text, cell.get("layout", {}).get("textAnchor"))
                        row_cells.append(cell_text)
                    if row_cells:
                        rows.append(row_cells)

                if headers or rows:
                    parsed_tables.append(
                        ParsedTable(headers=headers, rows=rows, page_number=actual_page_num)
                    )

            # 3. 提取图注（例如以 "图 1-" 或 "图 2-" 开头的段落）
            figure_captions = []
            for p_text in paragraphs:
                p_clean = p_text.strip()
                if p_clean.startswith("图 ") or p_clean.startswith("图") or "Figure " in p_clean:
                    figure_captions.append(p_clean)

            page_raw_text = "\n\n".join(paragraphs)

            parsed_pages.append(
                ParsedPage(
                    page_number=actual_page_num,
                    raw_text=page_raw_text,
                    paragraphs=paragraphs,
                    tables=parsed_tables,
                    figure_captions=figure_captions,
                )
            )

        return ParsedDocument(full_text=full_text, pages=parsed_pages)
