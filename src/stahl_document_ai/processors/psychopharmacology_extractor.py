"""精神药理学专业知识抽取与结构化器"""
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from stahl_document_ai.processors.response_parser import ParsedDocument, ParsedPage


class PharmacologicalMechanism(BaseModel):
    target: str = Field(description="靶点受体/转运体/酶，例如 5-HT2A, D2, SERT, NET")
    action_type: str = Field(description="作用模式：激动剂、拮抗剂、部分激动剂、反向激动剂、再摄取抑制剂、别构调节剂")
    description: str = Field(description="机制描述或生理/药理效应")


class FigureAnnotation(BaseModel):
    figure_id: str = Field(description="图编号，如 图 1-24")
    caption: str = Field(description="图注标题与说明")
    page_number: int
    related_mechanisms: List[str] = Field(default_factory=list)


class ChapterSection(BaseModel):
    title: str
    level: int = 1
    page_start: int
    page_end: Optional[int] = None
    content: str
    figures: List[FigureAnnotation] = Field(default_factory=list)
    key_drugs: List[str] = Field(default_factory=list)
    key_receptors: List[str] = Field(default_factory=list)


class PsychopharmacologyKnowledgeBase(BaseModel):
    book_title: str = "Stahl精神药理学精要：神经科学基础与实践应用 第5版"
    sections: List[ChapterSection] = Field(default_factory=list)
    all_figures: List[FigureAnnotation] = Field(default_factory=list)
    extracted_receptors_summary: Dict[str, List[str]] = Field(default_factory=dict)


class PsychopharmacologyExtractor:
    """从 Document AI 解析文本中抽取精神药理学知识模型"""

    RECEPTORS_KEYWORDS = [
        "5-HT1A", "5-HT2A", "5-HT2C", "5-HT3", "5-HT6", "5-HT7",
        "D1", "D2", "D3", "D4", "D5",
        "alpha-1", "alpha-2", "alpha-2A", "beta-1", "beta-2", "α1", "α2", "β1",
        "GABA-A", "GABA-B", "NMDA", "AMPA", "kainate", "红藻氨酸",
        "SERT", "NET", "DAT", "VMAT2", "MAO-A", "MAO-B", "COMT", "FAAH"
    ]

    DRUG_CLASSES_KEYWORDS = [
        "SSRI", "SNRI", "NDRI", "NaSSA", "SARI", "SPARI", "SMS", "TCA", "MAOI",
        "第一代抗精神病药", "第二代抗精神病药", "非典型抗精神病药", "情绪稳定剂",
        "抗抑郁药", "抗精神病药", "抗焦虑药", "促认知药", "NMDA受体拮抗剂"
    ]

    DRUGS_KEYWORDS = [
        "氯氮平", "奥氮平", "利培酮", "喹硫平", "阿立哌唑", "齐拉西酮", "鲁拉西酮", "氨磺必利", "布南色林",
        "氟西汀", "帕罗西汀", "舍曲林", "西酞普兰", "艾司西酞普兰", "氟伏沙明", "文拉法辛", "度洛西汀",
        "米氮平", "安非他酮", "曲唑酮", "沃替西汀", "维拉佐酮", "阿戈美拉汀", "艾司氯胺酮", "氯胺酮",
        "锂盐", "碳酸锂", "丙戊酸钠", "卡马西平", "拉莫三嗪", "托吡酯",
        "地西泮", "劳拉西泮", "阿普唑仑", "唑吡坦", "右佐匹克隆", "褪黑素", "食欲素受体拮抗剂", "苏沃雷生"
    ]

    @classmethod
    def extract_figures_from_text(cls, text: str, page_num: int) -> List[FigureAnnotation]:
        """识别类似 '图 1-24 xxx' 或 '图1-24 xxx' 的图表说明"""
        figures = []
        pattern = re.compile(r'(图\s*\d+[-–—]\d+[^。\n\r]*[。\n\r]?(?:[^\n\r]+[\n\r]?){0,4})')
        for match in pattern.finditer(text):
            caption = match.group(1).strip()
            fig_id_match = re.match(r'(图\s*\d+[-–—]\d+)', caption)
            fig_id = fig_id_match.group(1) if fig_id_match else "图"
            
            # 分析图注涉及的机制词汇
            related = []
            for r in cls.RECEPTORS_KEYWORDS:
                if r.lower() in caption.lower():
                    related.append(r)

            figures.append(
                FigureAnnotation(
                    figure_id=fig_id,
                    caption=caption,
                    page_number=page_num,
                    related_mechanisms=list(set(related)),
                )
            )
        return figures

    @classmethod
    def analyze_page(cls, page: ParsedPage) -> Dict[str, Any]:
        """分析单个页面的药理要素"""
        text = page.raw_text
        found_receptors = [r for r in cls.RECEPTORS_KEYWORDS if r.lower() in text.lower()]
        found_drugs = [d for d in cls.DRUGS_KEYWORDS if d in text]
        found_classes = [c for c in cls.DRUG_CLASSES_KEYWORDS if c in text]
        figures = cls.extract_figures_from_text(text, page.page_number)

        return {
            "page_number": page.page_number,
            "receptors": list(set(found_receptors)),
            "drugs": list(set(found_drugs)),
            "drug_classes": list(set(found_classes)),
            "figures": figures,
        }

    @classmethod
    def build_structured_knowledge_base(
        cls, parsed_doc: ParsedDocument
    ) -> PsychopharmacologyKnowledgeBase:
        """从解析后的整本文档构建完整的精神药理学知识库"""
        all_figures: List[FigureAnnotation] = []
        sections: List[ChapterSection] = []
        receptor_mentions: Dict[str, List[str]] = {}

        current_section_title = "前言/概述"
        current_section_paragraphs = []
        current_section_start = 1

        for page in parsed_doc.pages:
            page_analysis = cls.analyze_page(page)
            all_figures.extend(page_analysis["figures"])

            # 汇总受体出现的页码与上下文
            for rec in page_analysis["receptors"]:
                if rec not in receptor_mentions:
                    receptor_mentions[rec] = []
                receptor_mentions[rec].append(f"P.{page.page_number}")

            # 检查章节标题（例如：第1章 化学神经传递、第2章 神经递质受体等）
            for p in page.paragraphs:
                p_clean = p.strip()
                if re.match(r'^第\s*[一二三四五六七八九十\d]+\s*章', p_clean) or re.match(r'^Chapter\s*\d+', p_clean, re.IGNORECASE):
                    if current_section_paragraphs:
                        sections.append(
                            ChapterSection(
                                title=current_section_title,
                                page_start=current_section_start,
                                page_end=page.page_number - 1,
                                content="\n\n".join(current_section_paragraphs),
                            )
                        )
                        current_section_paragraphs = []
                    current_section_title = p_clean
                    current_section_start = page.page_number

            current_section_paragraphs.append(page.raw_text)

        # 添加最后一个章节
        if current_section_paragraphs:
            sections.append(
                ChapterSection(
                    title=current_section_title,
                    page_start=current_section_start,
                    page_end=parsed_doc.pages[-1].page_number if parsed_doc.pages else current_section_start,
                    content="\n\n".join(current_section_paragraphs),
                )
            )

        return PsychopharmacologyKnowledgeBase(
            sections=sections,
            all_figures=all_figures,
            extracted_receptors_summary=receptor_mentions,
        )
