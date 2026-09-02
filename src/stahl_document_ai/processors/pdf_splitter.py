"""PDF 切片与图像渲染处理器"""
import io
from dataclasses import dataclass
from pathlib import Path
from typing import List, Generator, Tuple
import pymupdf


@dataclass
class PageImageChunk:
    page_number: int  # 1-indexed 全局页码
    image_bytes: bytes
    mime_type: str = "image/png"


class PDFSplitter:
    def __init__(self, pdf_path: str | Path):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF 文件未找到: {self.pdf_path}")
        
        self.doc = pymupdf.open(str(self.pdf_path))
        self.total_pages = len(self.doc)

    def get_total_pages(self) -> int:
        return self.total_pages

    def render_page_to_image(self, page_number: int, dpi: int = 200) -> PageImageChunk:
        """将单页 PDF 渲染为高清 PNG 图像（避开损坏的字体编码）"""
        page_idx = max(0, min(page_number - 1, self.total_pages - 1))
        page = self.doc[page_idx]
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        return PageImageChunk(
            page_number=page_number,
            image_bytes=img_bytes,
            mime_type="image/png",
        )

    def render_page_range(self, start_page: int, end_page: int, dpi: int = 200) -> List[PageImageChunk]:
        """批量渲染指定页码范围的图像"""
        start = max(1, start_page)
        end = min(self.total_pages, end_page)
        return [self.render_page_to_image(p, dpi=dpi) for p in range(start, end + 1)]