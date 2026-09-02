# -*- coding: utf-8 -*-
"""打包生成标准的静态网站发布包并同步到 GitHub P·L·A·N·A 分支与 docs 目录"""
import os
import json
import re
import shutil
import stat
import zipfile
import subprocess
from html import unescape as html_unescape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from stahl_document_ai.processors.graph_builder import StahlKnowledgeGraphBuilder
from stahl_document_ai.processors.interactive_graph_generator import InteractiveGraphGenerator
from stahl_document_ai.processors.obsidian_exporter import ObsidianVaultExporter


_CSS_URL_RE = re.compile(
    r"""url\(\s*(?:"([^"]*)"|'([^']*)'|([^'"\)]*))\s*\)""",
    re.IGNORECASE,
)
_ASSET_LITERAL_RE = re.compile(
    r"""(?i)(?<![\w])(?:\.?/|/)?assets(?:/|\\|%2f|%5c)[^"'`<>\s\),;\]}]+"""
)


def _remove_readonly_and_retry(function, path, error_info):
    error = error_info[1] if isinstance(error_info, tuple) else error_info
    if isinstance(error, PermissionError):
        os.chmod(path, stat.S_IWRITE)
        function(path)
        return
    raise error


def _remove_generated_tree(path):
    if path.exists():
        if not path.is_dir() or path.is_symlink():
            raise RuntimeError(f"拒绝清理非普通目录: {path}")
        shutil.rmtree(path, onerror=_remove_readonly_and_retry)


def _extract_css_urls(text):
    return {
        next(value for value in match.groups() if value is not None).strip()
        for match in _CSS_URL_RE.finditer(text)
    }


class _AssetReferenceParser(HTMLParser):
    _URL_ATTRIBUTES = {
        "action",
        "background",
        "cite",
        "data",
        "formaction",
        "href",
        "longdesc",
        "manifest",
        "poster",
        "profile",
        "src",
        "usemap",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = set()

    def handle_starttag(self, _tag, attrs):
        for name, value in attrs:
            if not value:
                continue
            name = name.lower()
            if name in self._URL_ATTRIBUTES:
                self.references.add(value)
            elif name == "srcset":
                self.references.update(
                    candidate.strip().split(maxsplit=1)[0]
                    for candidate in value.split(",")
                    if candidate.strip()
                )

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def _fully_unquote(value):
    for _ in range(4):
        decoded = unquote(value)
        if decoded == value:
            return decoded
        value = decoded
    raise RuntimeError(f"资源 URL 编码层级过深: {value}")


def _normalize_asset_reference(reference):
    reference = html_unescape(reference.strip()).replace("\\/", "/")
    if not reference:
        return None

    try:
        parsed = urlsplit(reference)
    except ValueError as exc:
        raise RuntimeError(f"无法解析资源 URL: {reference}") from exc
    if parsed.scheme or parsed.netloc:
        return None

    decoded_path = _fully_unquote(parsed.path).replace("\\", "/")
    while decoded_path.startswith("./"):
        decoded_path = decoded_path[2:]
    decoded_path = decoded_path.lstrip("/")
    parts = decoded_path.split("/")

    if not any(part.lower() == "assets" for part in parts):
        return None
    if any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"拒绝包含路径穿越或空路径段的资源引用: {reference}")
    if parts[0] != "assets":
        return None
    if len(parts) == 1:
        raise RuntimeError(f"资源引用未指向文件: {reference}")
    if any(part.lower() == ".git" or ":" in part for part in parts):
        raise RuntimeError(f"拒绝不安全的资源引用: {reference}")

    return PurePosixPath(*parts[1:])


def _collect_referenced_assets(index_path, assets_dir):
    html = index_path.read_text(encoding="utf-8")
    parser = _AssetReferenceParser()
    parser.feed(html)

    references = parser.references
    references.update(_extract_css_urls(html))
    references.update(match.group(0) for match in _ASSET_LITERAL_RE.finditer(html))

    assets_root = assets_dir.resolve()
    referenced_assets = {}
    for reference in references:
        relative_path = _normalize_asset_reference(reference)
        if relative_path is None:
            continue

        source = (assets_root / Path(*relative_path.parts)).resolve()
        try:
            source.relative_to(assets_root)
        except ValueError as exc:
            raise RuntimeError(f"资源引用越出 assets 目录: {reference}") from exc
        if not source.is_file():
            raise FileNotFoundError(f"index.html 引用的资源不存在: {reference}")

        archive_name = PurePosixPath("assets", *relative_path.parts)
        referenced_assets[archive_name.as_posix()] = (source, archive_name)

    return [referenced_assets[key] for key in sorted(referenced_assets)]


def _replace_referenced_assets(index_path, source_assets, target_assets):
    if target_assets.resolve().parent != target_assets.parent.resolve():
        raise RuntimeError(f"拒绝清理非预期资源目录: {target_assets}")
    if target_assets.exists():
        _remove_generated_tree(target_assets)

    copied_assets = []
    for source, archive_name in _collect_referenced_assets(index_path, source_assets):
        destination = target_assets.joinpath(*archive_name.parts[1:])
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied_assets.append(destination)

    return copied_assets


def _asset_inventory(assets_dir):
    if not assets_dir.exists():
        return set()
    inventory = {
        file.relative_to(assets_dir).as_posix()
        for file in assets_dir.rglob("*")
        if file.is_file()
    }
    if any(".git" in {part.lower() for part in PurePosixPath(name).parts} for name in inventory):
        raise RuntimeError(f"资源目录包含 Git 元数据: {assets_dir}")
    return inventory


def _prepare_lite_dist(root_dir, dist_dir):
    lite_dir = root_dir / "dist_lite"
    if lite_dir.resolve().parent != root_dir.resolve():
        raise RuntimeError(f"拒绝清理非预期目录: {lite_dir}")
    if lite_dir.exists() and (not lite_dir.is_dir() or lite_dir.is_symlink()):
        raise RuntimeError(f"拒绝清理非普通目录: {lite_dir}")

    readme_path = lite_dir / "README_FOR_KIMI.txt"
    if not readme_path.is_file() or readme_path.is_symlink():
        raise FileNotFoundError(f"缺少可信的精简包说明文件: {readme_path}")
    readme_content = readme_path.read_bytes()

    if lite_dir.exists():
        _remove_generated_tree(lite_dir)
    lite_dir.mkdir(parents=False, exist_ok=False)

    shutil.copy2(dist_dir / "index.html", lite_dir / "index.html")
    shutil.copy2(dist_dir / "knowledge_graph.json", lite_dir / "knowledge_graph.json")
    shutil.copy2(dist_dir / "vercel.json", lite_dir / "vercel.json")
    (lite_dir / ".nojekyll").touch()
    (lite_dir / "README_FOR_KIMI.txt").write_bytes(readme_content)

    copied_assets = []
    for source, archive_name in _collect_referenced_assets(
        dist_dir / "index.html", dist_dir / "assets"
    ):
        destination = lite_dir.joinpath(*archive_name.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied_assets.append(destination)

    return lite_dir, copied_assets


def _write_lite_zip(lite_dir, copied_assets, zip_path):
    release_files = [
        lite_dir / "index.html",
        lite_dir / "knowledge_graph.json",
        lite_dir / ".nojekyll",
        lite_dir / "vercel.json",
        lite_dir / "README_FOR_KIMI.txt",
        *copied_assets,
    ]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in release_files:
            archive_name = file.relative_to(lite_dir)
            if ".git" in {part.lower() for part in archive_name.parts}:
                raise RuntimeError(f"拒绝打包 Git 元数据: {archive_name}")
            zipf.write(file, archive_name)


project_root = Path(__file__).resolve().parent.parent
root = project_root / "output"
root.mkdir(parents=True, exist_ok=True)

# 0. 重新构建图谱数据、3D 页面与 Obsidian Vault
graph = StahlKnowledgeGraphBuilder.build_comprehensive_graph()
kg_json_path = root / "knowledge_graph.json"
kg_json_path.write_text(json.dumps(graph.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

html_path = root / "interactive_graph.html"
InteractiveGraphGenerator.generate_html(graph, html_path)
ObsidianVaultExporter.export_vault(graph, root)

dist = root / "dist"
if dist.resolve().parent != root.resolve():
    raise RuntimeError(f"拒绝清理非预期目录: {dist}")
if dist.exists():
    _remove_generated_tree(dist)
dist.mkdir(parents=False, exist_ok=False)

# 1. 复制 index.html
shutil.copy2(root / "interactive_graph.html", dist / "index.html")

# 2. 复制 assets 目录 (如果存在)
dist_assets = dist / "assets"
dist_release_assets = _replace_referenced_assets(
    dist / "index.html", root / "assets", dist_assets
)

# 3. 复制知识图谱数据
shutil.copy2(root / "knowledge_graph.json", dist / "knowledge_graph.json")

# 4. 创建 .nojekyll 与 Vercel 静态配置
(dist / ".nojekyll").touch()
vercel_cfg = {
    "version": 2,
    "headers": [
        {
            "source": "/assets/(.*)",
            "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
            ]
        }
    ]
}
(dist / "vercel.json").write_text(json.dumps(vercel_cfg, indent=2), encoding="utf-8")

# 5. 复制到 dist_lite
lite_dir, lite_release_assets = _prepare_lite_dist(root, dist)

# 6. 复制到 docs 目录与仓库根目录以支持所有模式的 GitHub Pages
project_root = Path(__file__).resolve().parent.parent
docs_dir = project_root / "docs"
docs_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(dist / "index.html", docs_dir / "index.html")
shutil.copy2(dist / "knowledge_graph.json", docs_dir / "knowledge_graph.json")
(docs_dir / ".nojekyll").touch()

# 兼容根目录直接托管模式
shutil.copy2(dist / "index.html", project_root / "index.html")
shutil.copy2(dist / "knowledge_graph.json", project_root / "knowledge_graph.json")
(project_root / ".nojekyll").touch()

docs_assets = docs_dir / "assets"
if docs_assets.exists():
    _remove_generated_tree(docs_assets)
if dist_assets.exists():
    shutil.copytree(dist_assets, docs_assets)

root_assets = project_root / "assets"
if root_assets.exists():
    _remove_generated_tree(root_assets)
if dist_assets.exists():
    shutil.copytree(dist_assets, root_assets)

expected_asset_inventory = _asset_inventory(dist_assets)
if expected_asset_inventory != {
    file.relative_to(dist_assets).as_posix() for file in dist_release_assets
}:
    raise RuntimeError("dist/assets 含有 HTML 未引用的资源")
for label, assets_dir in {
    "docs": docs_assets,
    "root": root_assets,
    "dist_lite": lite_dir / "assets",
}.items():
    if _asset_inventory(assets_dir) != expected_asset_inventory:
        raise RuntimeError(f"{label} 资源集合与 dist/assets 不一致")

# 7. 生成精简 ZIP 发布包
zip_path = root / "stahl_web_deploy.zip"
_write_lite_zip(lite_dir, lite_release_assets, zip_path)

print(f"[OK] 静态发布包已就绪: {dist}")
print(f"[OK] GitHub Pages /docs 部署包已就绪: {docs_dir}")
print(f"[OK] 精简部署包已就绪: {zip_path}")
