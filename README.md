# 基于 Google Cloud Document AI 的《Stahl精神药理学精要》结构化解析工具

本项目参考 [Google Cloud Document AI REST API 规范](https://docs.cloud.google.com/document-ai/docs/reference/rest?apix=true&rep_location=global)，专门解决大型医学专著（《Stahl精神药理学精要 第5版》537页）在本地 PDF 抽取时因内嵌字形编码损坏导致的严重乱码问题，利用 Document AI 视觉 OCR 与布局解析实现高精度文本恢复、图表提取以及精神药理学专业知识结构化抽取。

---

## 核心特性

1. **REST API 原生支持**：封装 Document AI v1 REST API（`:process` 同步在线处理与 `:batchProcess` 异步批量处理）。
2. **大文件智能切片与断点续传**：自动将 537 页 PDF 按 15 页单批次安全切片，支持局部页码处理与 JSON 响应本地缓存，避免重复消费 API。
3. **乱码彻底修复**：绕过损坏的 ToUnicode 映射，通过高精度 OCR 视觉模型提取完整中文与生化符号。
4. **精神药理学领域结构化**：
   - 提取 **受体/递质/转运体/酶**（5-HT1A, 5-HT2A, D2, GABA-A, NMDA, SERT, NET, DAT 等）。
   - 提取 **药物类别与具体药物**（SSRI, SNRI, 非典型抗精神病药, 氯氮平, 奥氮平等）。
   - 提取 **机制图解与图注**（自动识别 `图 X-Y` 机制图解并建立关联）。
5. **多格式导出**：
   - `stahl_full.md` / 章节 Markdown：排版清晰，适配 Obsidian / Notion。
   - `psychopharmacology_kb.json`：结构化知识库 JSON。
   - `rag_chunks.jsonl`：面向大模型 RAG 检索的 Chunk 数据集（含页码与受体/药物元数据）。

---

## 快速使用指南

### 1. 安装与环境准备

项目使用 `uv` 进行高效依赖管理：

```bash
cd C:\Users\Kuriy\.gemini\antigravity\scratch\stahl_document_ai
uv sync
```

### 2. 配置 Google Cloud 凭据

复制配置文件模板：
```bash
cp .env.example .env
```
在 `.env` 中填写您的 GCP 信息：
```ini
GCP_PROJECT_ID=your-gcp-project-id
GCP_LOCATION=us
GCP_PROCESSOR_ID=your-docai-processor-id
# 可选：GOOGLE_APPLICATION_CREDENTIALS="C:/path/to/key.json"
```

### 3. 命令行操作

#### (1) 查看 PDF 结构与批处理规划
```bash
uv run python src/stahl_document_ai/main.py info
```

#### (2) 试运行前 5 页（快速验证 OCR 效果）
```bash
uv run python src/stahl_document_ai/main.py process-range --start-page 1 --end-page 5
```

#### (3) 运行完整 537 页批处理
```bash
uv run python src/stahl_document_ai/main.py process-range --start-page 1 --end-page 537
```

#### (4) 从本地 JSON 缓存中重新生成导出文件（无 API 消耗）
```bash
uv run python src/stahl_document_ai/main.py parse-local-cached --cache-dir cache --output-dir output
```

### 4. 运行自动化测试
```bash
uv run pytest -v
```