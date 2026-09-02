"""命令行入口"""
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import os
import json
import time
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from stahl_document_ai.config import settings
from stahl_document_ai.client.docai_rest import DocumentAIRestClient
from stahl_document_ai.processors.pdf_splitter import PDFSplitter
from stahl_document_ai.processors.response_parser import DocumentAIResponseParser, ParsedDocument
from stahl_document_ai.processors.psychopharmacology_extractor import PsychopharmacologyExtractor
from stahl_document_ai.processors.graph_builder import StahlKnowledgeGraphBuilder
from stahl_document_ai.processors.interactive_graph_generator import InteractiveGraphGenerator
from stahl_document_ai.processors.obsidian_exporter import ObsidianVaultExporter
from stahl_document_ai.exporter import DocumentExporter

console = Console(safe_box=True)
app = typer.Typer(help="基于 Google Cloud Document AI 的 Stahl 精神药理学精要结构化解析系统")

DEFAULT_PDF_PATH = r"G:\4.文档\医学相关\Stahl精神药理学精要：神经科学基础与实践应用 第5版中译稿 (Stephen M. Stahl) (Z-Library).pdf"


@app.command()
def info(
    pdf_path: str = typer.Option(DEFAULT_PDF_PATH, help="PDF 文件路径"),
):
    """查看 PDF 基本信息与分块规划"""
    console.print(f"[bold cyan]正在分析 PDF 文件:[/bold cyan] {pdf_path}")
    splitter = PDFSplitter(pdf_path)
    total_pages = splitter.get_total_pages()

    table = Table(title="PDF 分析与批处理规划")
    table.add_column("属性", style="bold green")
    table.add_column("数值", style="yellow")

    table.add_row("总页数", str(total_pages))
    table.add_row("输出目录", str(settings.output_dir))
    table.add_row("缓存目录", str(settings.cache_dir))
    table.add_row("GCP Project ID", settings.gcp_project_id or "[未配置]")
    table.add_row("GCP Processor ID", settings.gcp_processor_id or "[未配置]")
    table.add_row("GCP Location", settings.gcp_location)

    console.print(table)


@app.command()
def process_range(
    start_page: int = typer.Option(1, help="起始页码 (从1开始)"),
    end_page: int = typer.Option(5, help="结束页码"),
    pdf_path: str = typer.Option(DEFAULT_PDF_PATH, help="PDF 文件路径"),
    output_dir: str = typer.Option("output", help="输出目录"),
    dpi: int = typer.Option(200, help="图像渲染 DPI"),
):
    """解析指定页码范围的 PDF 内容并通过 Document AI 纯图像 OCR 高清处理"""
    console.print(f"[bold green]开始处理页码范围: {start_page} - {end_page} (共 {end_page - start_page + 1} 页)[/bold green]")
    
    if not settings.gcp_project_id or not settings.gcp_processor_id:
        console.print("[bold red]错误: 请先在 .env 或环境变量中配置 GCP_PROJECT_ID 和 GCP_PROCESSOR_ID！[/bold red]")
        raise typer.Exit(code=1)

    splitter = PDFSplitter(pdf_path)
    client = DocumentAIRestClient(
        project_id=settings.gcp_project_id,
        location=settings.gcp_location,
        processor_id=settings.gcp_processor_id,
        credentials_path=settings.google_application_credentials,
        timeout=settings.request_timeout_seconds,
    )

    settings.cache_dir.mkdir(parents=True, exist_ok=True)
    all_pages = []
    full_text_list = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Document AI 正在逐页高精 OCR 解析...", total=(end_page - start_page + 1))

        for p_num in range(start_page, end_page + 1):
            cache_file = settings.cache_dir / f"page_{p_num:04d}.json"
            if cache_file.exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    response = json.load(f)
            else:
                chunk = splitter.render_page_to_image(p_num, dpi=dpi)
                response = client.process_document(chunk.image_bytes, mime_type=chunk.mime_type)
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(response, f, ensure_ascii=False)
                time.sleep(0.1)

            parsed = DocumentAIResponseParser.parse_process_response(response, global_page_offset=p_num - 1)
            all_pages.extend(parsed.pages)
            full_text_list.append(parsed.full_text)
            progress.advance(task)

    combined_doc = ParsedDocument(full_text="\n\n".join(full_text_list), pages=all_pages)
    kb = PsychopharmacologyExtractor.build_structured_knowledge_base(combined_doc)

    exporter = DocumentExporter(output_dir)
    md_file = exporter.export_full_markdown(combined_doc, f"stahl_pages_{start_page}_{end_page}.md")
    kb_file = exporter.export_knowledge_base_json(kb, f"kb_pages_{start_page}_{end_page}.json")
    rag_file = exporter.export_rag_chunks_jsonl(combined_doc, f"rag_pages_{start_page}_{end_page}.jsonl")

    console.print(f"[bold green][OK] 提取完成！生成的文件列表:[/bold green]")
    console.print(f" - Markdown: {md_file}")
    console.print(f" - 结构化知识库 JSON: {kb_file}")
    console.print(f" - RAG 检索数据集: {rag_file}")


@app.command()
def build_knowledge_graph(
    output_dir: str = typer.Option("output", help="知识图谱产物输出目录"),
):
    """构建精神药理学全景知识图谱与交互式可视化应用"""
    console.print("[bold cyan]正在构建 Stahl 精神药理学全景知识图谱...[/bold cyan]")
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. 构建图谱
    graph = StahlKnowledgeGraphBuilder.build_comprehensive_graph()
    graph_dict = graph.to_dict()

    # 2. 导出图谱 JSON
    json_path = out_path / "knowledge_graph.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(graph_dict, f, ensure_ascii=False, indent=2)

    # 3. 导出交互式 HTML
    html_path = out_path / "interactive_graph.html"
    InteractiveGraphGenerator.generate_html(graph, html_path)

    # 4. 导出 Obsidian 双链知识库
    vault_path = ObsidianVaultExporter.export_vault(graph, out_path)

    table = Table(title="Stahl 精神药理学知识图谱构建完成")
    table.add_column("指标/产物", style="bold green")
    table.add_column("详情与路径", style="yellow")

    table.add_row("图谱总节点数 (Nodes)", str(graph_dict["stats"]["total_nodes"]))
    table.add_row("药理关系边数 (Edges)", str(graph_dict["stats"]["total_edges"]))
    table.add_row("实体范畴覆盖", ", ".join(graph_dict["stats"]["categories"]))
    table.add_row("交互式图谱应用 (HTML)", str(html_path.resolve()))
    table.add_row("图谱数据文件 (JSON)", str(json_path.resolve()))
    table.add_row("Obsidian 双链知识库", str(vault_path.resolve()))

    console.print(table)
    console.print(f"\n[bold green][OK] 知识图谱已生成完毕！双击即可在浏览器中打开: {html_path}[/bold green]")


def main():
    app()


if __name__ == "__main__":
    main()