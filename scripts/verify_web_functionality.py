# -*- coding: utf-8 -*-
"""验证知识图谱页面、静态发布副本与 ZIP 发布包的一致性。"""

import html as html_module
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

HTML_PATHS = (
    OUTPUT_DIR / "interactive_graph.html",
    OUTPUT_DIR / "dist" / "index.html",
    PROJECT_ROOT / "docs" / "index.html",
    PROJECT_ROOT / "index.html",
    OUTPUT_DIR / "dist_lite" / "index.html",
)
JSON_PATHS = (
    OUTPUT_DIR / "knowledge_graph.json",
    OUTPUT_DIR / "dist" / "knowledge_graph.json",
    PROJECT_ROOT / "docs" / "knowledge_graph.json",
    PROJECT_ROOT / "knowledge_graph.json",
    OUTPUT_DIR / "dist_lite" / "knowledge_graph.json",
)
ZIP_PATH = OUTPUT_DIR / "stahl_web_deploy.zip"
EXPECTED_NODE_COUNT = 187
EXPECTED_EDGE_COUNT = 384
DIST_ROOT_FILES = frozenset(
    {
        "index.html",
        "knowledge_graph.json",
        ".nojekyll",
        "vercel.json",
    }
)
LITE_ROOT_FILES = frozenset(
    {
        *DIST_ROOT_FILES,
        "README_FOR_KIMI.txt",
    }
)

ASSET_STRING_PATTERN = re.compile(
    r"(?P<quote>[\"'`])(?P<path>(?:\./|/)?assets/.*?)(?P=quote)",
    flags=re.IGNORECASE,
)
ASSET_URL_PATTERN = re.compile(
    r"url\(\s*(?P<path>(?:\./|/)?assets/[^\s)'\"]+)\s*\)",
    flags=re.IGNORECASE,
)
GRAPH_RAW_DATA_PATTERN = re.compile(r"\bconst\s+graphRawData\s*=\s*")
SCRIPT_PATTERN = re.compile(
    r"<script(?P<attrs>\s[^>]*)?>(?P<body>.*?)</script\s*>",
    flags=re.IGNORECASE | re.DOTALL,
)


class VerificationError(RuntimeError):
    """表示发布产物未通过验证。"""


def display_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def read_required_bytes(path: Path) -> bytes:
    require(path.is_file(), f"缺少必要文件: {display_path(path)}")
    return path.read_bytes()


def verify_identical_files(paths: tuple[Path, ...], kind: str) -> bytes:
    canonical_path = paths[0]
    canonical_content = read_required_bytes(canonical_path)
    mismatches = [
        display_path(path)
        for path in paths[1:]
        if read_required_bytes(path) != canonical_content
    ]
    require(
        not mismatches,
        f"{kind} 副本与 {display_path(canonical_path)} 内容不一致: "
        + ", ".join(mismatches),
    )
    print(f"[OK] {kind} 副本内容一致（{len(paths)} 份）")
    return canonical_content


def normalize_asset_reference(reference: str) -> str:
    normalized = html_module.unescape(reference.strip())
    normalized = unquote(normalized).replace("\\", "/")
    normalized = normalized.split("#", 1)[0].split("?", 1)[0]
    if normalized.startswith("./"):
        normalized = normalized[2:]
    normalized = normalized.lstrip("/")

    parts = PurePosixPath(normalized).parts
    require(
        len(parts) >= 2
        and parts[0].lower() == "assets"
        and all(part not in {"", ".", ".."} for part in parts),
        f"非法本地资源引用: {reference}",
    )
    return PurePosixPath(*parts).as_posix()


def extract_asset_references(html_content: str) -> set[str]:
    raw_references = {
        match.group("path") for match in ASSET_STRING_PATTERN.finditer(html_content)
    }
    raw_references.update(
        match.group("path") for match in ASSET_URL_PATTERN.finditer(html_content)
    )
    return {normalize_asset_reference(reference) for reference in raw_references}


def verify_local_assets(html_paths: tuple[Path, ...]) -> dict[Path, set[str]]:
    all_references: set[str] = set()
    references_by_html: dict[Path, set[str]] = {}
    missing: list[str] = []

    for html_path in html_paths:
        html_content = read_required_bytes(html_path).decode("utf-8")
        references = extract_asset_references(html_content)
        require(
            references,
            f"{display_path(html_path)} 未发现任何本地 assets 引用",
        )
        references_by_html[html_path] = references
        all_references.update(references)
        site_root = html_path.parent
        for reference in sorted(references):
            asset_path = site_root.joinpath(*PurePosixPath(reference).parts)
            if not asset_path.is_file():
                missing.append(f"{display_path(html_path)} -> {reference}")

    require(
        not missing,
        "HTML 引用的本地资源缺失:\n- " + "\n- ".join(missing),
    )
    print(
        f"[OK] {len(html_paths)} 个站点目录中的 "
        f"{len(all_references)} 项本地 assets 引用均存在"
    )
    return references_by_html


def verify_release_root(site_root: Path, required_files: frozenset[str]) -> None:
    require(site_root.is_dir(), f"缺少发布目录: {display_path(site_root)}")
    entries = {path.name: path for path in site_root.iterdir()}
    required_entries = required_files | {"assets"}
    missing = sorted(required_entries - entries.keys())
    extras = sorted(entries.keys() - required_entries)
    require(
        not missing,
        f"{display_path(site_root)} 缺少根级必需项: " + ", ".join(missing),
    )
    require(
        not extras,
        f"{display_path(site_root)} 包含根级白名单外项目: " + ", ".join(extras),
    )

    invalid_files = sorted(
        name
        for name in required_files
        if not entries[name].is_file() or entries[name].is_symlink()
    )
    require(
        not invalid_files,
        f"{display_path(site_root)} 的根级必需文件类型无效: "
        + ", ".join(invalid_files),
    )
    require(
        entries["assets"].is_dir() and not entries["assets"].is_symlink(),
        f"{display_path(site_root)}/assets 必须是普通目录",
    )
    print(
        f"[OK] {display_path(site_root)} 根目录仅包含 "
        f"{len(required_files)} 个必需文件与 assets/"
    )


def collect_release_asset_files(site_root: Path) -> set[str]:
    assets_root = site_root / "assets"
    require(assets_root.is_dir(), f"缺少发布资源目录: {display_path(assets_root)}")

    asset_paths = list(assets_root.rglob("*"))
    git_paths = [
        display_path(path)
        for path in asset_paths
        if ".git"
        in {part.lower() for part in path.relative_to(site_root).parts}
    ]
    require(
        not git_paths,
        f"{display_path(site_root)} 的发布资源包含 .git 路径段: "
        + ", ".join(git_paths),
    )

    return {
        PurePosixPath(*path.relative_to(site_root).parts).as_posix()
        for path in asset_paths
        if path.is_file()
    }


def verify_exact_release_assets(index_path: Path, references: set[str]) -> None:
    packaged_assets = collect_release_asset_files(index_path.parent)
    missing_assets = sorted(references - packaged_assets)
    extra_assets = sorted(packaged_assets - references)
    require(
        not missing_assets,
        f"{display_path(index_path.parent)} 缺少 index.html 引用的资源: "
        + ", ".join(missing_assets),
    )
    require(
        not extra_assets,
        f"{display_path(index_path.parent)} 包含 index.html 未引用的多余资源: "
        + ", ".join(extra_assets),
    )
    print(
        f"[OK] {display_path(index_path.parent)} 的 {len(packaged_assets)} 项 assets "
        "与 index.html 引用集合完全一致"
    )


def verify_release_asset_bytes(
    references_by_html: dict[Path, set[str]],
) -> None:
    canonical_html = HTML_PATHS[0]
    canonical_references = references_by_html[canonical_html]
    mismatches: list[str] = []

    for html_path in HTML_PATHS[1:]:
        require(
            references_by_html[html_path] == canonical_references,
            f"{display_path(html_path)} 的 assets 引用集合与源页面不一致",
        )
        for reference in sorted(canonical_references):
            parts = PurePosixPath(reference).parts
            source_asset = canonical_html.parent.joinpath(*parts)
            copied_asset = html_path.parent.joinpath(*parts)
            if source_asset.read_bytes() != copied_asset.read_bytes():
                mismatches.append(f"{display_path(html_path)} -> {reference}")

    require(
        not mismatches,
        "发布目录中的同名 assets 与 output 源资源 bytes 不一致:\n- "
        + "\n- ".join(mismatches),
    )
    print(
        f"[OK] output/dist、docs、仓库根目录与 output/dist_lite 的 "
        f"{len(canonical_references)} 项 assets 均与 output 源资源逐字节一致"
    )


def normalized_zip_name(name: str) -> str:
    normalized = name.replace("\\", "/")
    require(
        not normalized.startswith("/") and re.match(r"^[A-Za-z]:", normalized) is None,
        f"ZIP 发布包包含绝对路径: {name}",
    )
    while normalized.startswith("./"):
        normalized = normalized[2:]
    parts = [part for part in normalized.rstrip("/").split("/") if part not in {"", "."}]
    require(".." not in parts, f"ZIP 发布包包含路径穿越项: {name}")
    require(parts, f"ZIP 发布包包含空路径项: {name}")
    return PurePosixPath(*parts).as_posix()


def verify_zip_package(zip_path: Path) -> None:
    require(zip_path.is_file(), f"缺少 ZIP 发布包: {display_path(zip_path)}")

    with zipfile.ZipFile(zip_path, "r") as archive:
        infos = archive.infolist()
        git_entries = [
            info.filename
            for info in infos
            if ".git"
            in {
                part.lower()
                for part in re.split(r"[\\/]", info.filename)
                if part
            }
        ]
        require(
            not git_entries,
            "ZIP 发布包包含 .git 路径段: " + ", ".join(git_entries),
        )

        normalized_infos = [
            (normalized_zip_name(info.filename), info) for info in infos
        ]
        duplicate_entries = sorted(
            name
            for name, count in Counter(
                normalized_name for normalized_name, _ in normalized_infos
            ).items()
            if count > 1
        )
        require(
            not duplicate_entries,
            "ZIP 发布包包含重复路径项: " + ", ".join(duplicate_entries),
        )
        file_infos = {
            normalized_name: info
            for normalized_name, info in normalized_infos
            if not info.is_dir()
        }
        missing_required = sorted(LITE_ROOT_FILES - file_infos.keys())
        require(
            not missing_required,
            "ZIP 发布包缺少必要文件: " + ", ".join(missing_required),
        )
        unexpected_entries = sorted(
            normalized_name
            for normalized_name, info in normalized_infos
            if not (
                (
                    PurePosixPath(normalized_name).parts[0] == "assets"
                    and normalized_name != "assets"
                )
                or (normalized_name == "assets" and info.is_dir())
                or (normalized_name in LITE_ROOT_FILES and not info.is_dir())
            )
        )
        require(
            not unexpected_entries,
            "ZIP 发布包包含根级白名单外项目: " + ", ".join(unexpected_entries),
        )

        zip_html = archive.read(file_infos["index.html"]).decode("utf-8")
        zip_asset_references = extract_asset_references(zip_html)
        require(zip_asset_references, "ZIP 的 index.html 未发现任何本地 assets 引用")
        missing_assets = sorted(zip_asset_references - file_infos.keys())
        require(
            not missing_assets,
            "ZIP 发布包缺少 index.html 引用的本地资源: "
            + ", ".join(missing_assets),
        )
        zip_asset_files = {
            name
            for name in file_infos
            if PurePosixPath(name).parts
            and PurePosixPath(name).parts[0].lower() == "assets"
        }
        extra_assets = sorted(zip_asset_files - zip_asset_references)
        require(
            not extra_assets,
            "ZIP 发布包包含 index.html 未引用的多余资源: "
            + ", ".join(extra_assets),
        )
        mismatched_assets = sorted(
            reference
            for reference in zip_asset_references
            if archive.read(file_infos[reference])
            != read_required_bytes(
                (OUTPUT_DIR / "dist_lite").joinpath(
                    *PurePosixPath(reference).parts
                )
            )
        )
        require(
            not mismatched_assets,
            "ZIP 中的 assets 与 output/dist_lite 同名资源 bytes 不一致: "
            + ", ".join(mismatched_assets),
        )

        mismatched_root_files = sorted(
            name
            for name in LITE_ROOT_FILES
            if archive.read(file_infos[name])
            != read_required_bytes(OUTPUT_DIR / "dist_lite" / name)
        )
        require(
            not mismatched_root_files,
            "ZIP 根级文件与 output/dist_lite 内容不一致: "
            + ", ".join(mismatched_root_files),
        )

    print(
        f"[OK] ZIP 发布包结构完整，包含 {len(zip_asset_references)} 项页面资源，"
        "且不含 .git 路径段"
    )


def extract_graph_raw_data(page: str) -> dict:
    assignments = [
        (script, match)
        for script in extract_inline_scripts(page)
        for match in GRAPH_RAW_DATA_PATTERN.finditer(script)
    ]
    require(
        len(assignments) == 1,
        f"interactive_graph.html 中 graphRawData 赋值数量应为 1，实际为 {len(assignments)}",
    )
    script, assignment = assignments[0]

    try:
        graph_data, end_index = json.JSONDecoder().raw_decode(
            script, assignment.end()
        )
    except json.JSONDecodeError as exc:
        raise VerificationError(f"graphRawData 不是可精确解析的 JSON 对象: {exc}") from exc

    require(
        re.match(r"\s*;", script[end_index:]) is not None,
        "graphRawData JSON 对象后缺少语句结束分号",
    )
    require(isinstance(graph_data, dict), "graphRawData 必须是对象")
    return graph_data


def counter_difference_summary(expected: Counter, actual: Counter) -> str:
    missing = list((expected - actual).elements())
    extra = list((actual - expected).elements())

    def summarize(items: list[str]) -> str:
        if not items:
            return "无"
        preview = "; ".join(item[:240] for item in items[:2])
        suffix = f"；另有 {len(items) - 2} 项" if len(items) > 2 else ""
        return preview + suffix

    return f"缺失/不一致: {summarize(missing)}；多余/不一致: {summarize(extra)}"


def verify_embedded_graph_equivalence(kg_data: dict, graph_data: dict) -> None:
    canonical_nodes = kg_data.get("nodes")
    canonical_edges = kg_data.get("edges")
    embedded_nodes = graph_data.get("nodes")
    embedded_links = graph_data.get("links")
    require(isinstance(canonical_nodes, list), "knowledge_graph.json 缺少 nodes 数组")
    require(isinstance(canonical_edges, list), "knowledge_graph.json 缺少 edges 数组")
    require(isinstance(embedded_nodes, list), "graphRawData 缺少 nodes 数组")
    require(isinstance(embedded_links, list), "graphRawData 缺少 links 数组")

    require(
        len(canonical_nodes) == EXPECTED_NODE_COUNT,
        f"knowledge_graph.json 节点数应为 {EXPECTED_NODE_COUNT}，实际为 {len(canonical_nodes)}",
    )
    require(
        len(canonical_edges) == EXPECTED_EDGE_COUNT,
        f"knowledge_graph.json 关系数应为 {EXPECTED_EDGE_COUNT}，实际为 {len(canonical_edges)}",
    )
    require(
        len(embedded_nodes) == EXPECTED_NODE_COUNT,
        f"graphRawData 节点数应为 {EXPECTED_NODE_COUNT}，实际为 {len(embedded_nodes)}",
    )
    require(
        len(embedded_links) == EXPECTED_EDGE_COUNT,
        f"graphRawData 关系数应为 {EXPECTED_EDGE_COUNT}，实际为 {len(embedded_links)}",
    )

    for index, node in enumerate(canonical_nodes):
        require(isinstance(node, dict), f"knowledge_graph.json nodes[{index}] 不是对象")
    for index, edge in enumerate(canonical_edges):
        require(isinstance(edge, dict), f"knowledge_graph.json edges[{index}] 不是对象")
    for index, node in enumerate(embedded_nodes):
        require(isinstance(node, dict), f"graphRawData nodes[{index}] 不是对象")
    for index, link in enumerate(embedded_links):
        require(isinstance(link, dict), f"graphRawData links[{index}] 不是对象")

    canonical_node_projection = [
        {
            "id": node.get("id"),
            "label": node.get("label"),
            "category": node.get("category"),
            "description": node.get("description"),
            "properties": node.get("properties"),
        }
        for node in canonical_nodes
    ]
    embedded_node_projection = [
        {
            "id": node.get("id"),
            "label": node.get("fullLabel")
            if "fullLabel" in node
            else node.get("label"),
            "category": node.get("category"),
            "description": node.get("description"),
            "properties": node.get("properties"),
        }
        for node in embedded_nodes
    ]
    canonical_edge_projection = [
        {
            "source": edge.get("source"),
            "target": edge.get("target"),
            "relationship": edge.get("relationship"),
            "label": edge.get("label"),
            "description": edge.get("description"),
            "weight": edge.get("weight"),
        }
        for edge in canonical_edges
    ]
    embedded_edge_projection = [
        {
            "source": link.get("source"),
            "target": link.get("target"),
            "relationship": link.get("relationship"),
            "label": link.get("label"),
            "description": link.get("description"),
            "weight": link.get("weight"),
        }
        for link in embedded_links
    ]

    serialize = lambda item: json.dumps(
        item, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    expected_nodes = Counter(serialize(node) for node in canonical_node_projection)
    actual_nodes = Counter(serialize(node) for node in embedded_node_projection)
    require(
        expected_nodes == actual_nodes,
        "graphRawData 节点全集与 knowledge_graph.json 不等价；"
        + counter_difference_summary(expected_nodes, actual_nodes),
    )

    expected_edges = Counter(serialize(edge) for edge in canonical_edge_projection)
    actual_edges = Counter(serialize(edge) for edge in embedded_edge_projection)
    require(
        expected_edges == actual_edges,
        "graphRawData 关系全集与 knowledge_graph.json 不等价；"
        + counter_difference_summary(expected_edges, actual_edges),
    )
    print(
        f"[OK] graphRawData 与 knowledge_graph.json 完整等价（"
        f"{EXPECTED_NODE_COUNT} 节点 / {EXPECTED_EDGE_COUNT} 关系）"
    )


def extract_inline_scripts(page: str) -> list[str]:
    scripts = []
    for match in SCRIPT_PATTERN.finditer(page):
        attrs = match.group("attrs") or ""
        if re.search(r"\bsrc\s*=", attrs, flags=re.IGNORECASE):
            continue
        body = match.group("body")
        if body.strip():
            scripts.append(body)
    require(scripts, "interactive_graph.html 未发现可验证的内联 JavaScript")
    return scripts


def verify_inline_javascript(page: str) -> None:
    node_path = shutil.which("node")
    require(
        node_path is not None,
        "未找到 Node.js，无法执行内联 JavaScript 语法验证",
    )
    scripts = extract_inline_scripts(page)

    with tempfile.TemporaryDirectory(prefix="stahl-inline-js-") as temp_dir:
        for index, script in enumerate(scripts, start=1):
            script_path = Path(temp_dir) / f"inline-{index}.js"
            script_path.write_text(script, encoding="utf-8")
            try:
                result = subprocess.run(
                    [node_path, "--check", str(script_path)],
                    capture_output=True,
                    check=False,
                    encoding="utf-8",
                    errors="replace",
                    timeout=30,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise VerificationError(
                    f"Node.js 无法检查内联脚本 {index}: {exc}"
                ) from exc
            diagnostic = (result.stderr or result.stdout).strip()
            require(
                result.returncode == 0,
                f"内联脚本 {index} 未通过 node --check: {diagnostic}",
            )
    print(f"[OK] Node.js 已验证 {len(scripts)} 段内联 JavaScript 语法")


def verify_graph_and_page(kg_content: bytes, html_content: bytes) -> None:
    try:
        kg_data = json.loads(kg_content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"knowledge_graph.json 无法解析: {exc}") from exc
    require(isinstance(kg_data, dict), "knowledge_graph.json 顶层必须是对象")

    nodes = kg_data.get("nodes")
    edges = kg_data.get("edges")
    require(isinstance(nodes, list), "knowledge_graph.json 缺少 nodes 数组")
    require(isinstance(edges, list), "knowledge_graph.json 缺少 edges 数组")

    node_ids: list[str] = []
    for index, node in enumerate(nodes):
        require(isinstance(node, dict), f"nodes[{index}] 不是对象")
        node_id = node.get("id")
        require(
            isinstance(node_id, str) and node_id,
            f"nodes[{index}] 缺少有效 id",
        )
        node_ids.append(node_id)
    require(len(node_ids) == len(set(node_ids)), "knowledge_graph.json 存在重复节点 id")
    nodes_dict = set(node_ids)

    try:
        page = html_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"interactive_graph.html 不是有效 UTF-8: {exc}") from exc

    graph_raw_data = extract_graph_raw_data(page)
    verify_embedded_graph_equivalence(kg_data, graph_raw_data)
    verify_inline_javascript(page)

    referenced_ids = set(
        re.findall(r"[\"']((?:DRUG|REC|PATH|DIS|CLS|SE)_[A-Z0-9_]+)[\"']", page)
    )
    require(referenced_ids, "interactive_graph.html 未发现任何知识图谱节点引用")
    missing_nodes = sorted(referenced_ids - nodes_dict)
    require(
        not missing_nodes,
        "interactive_graph.html 引用了不存在的节点: " + ", ".join(missing_nodes),
    )
    print(f"[OK] KG nodes = {len(nodes_dict)}, KG edges = {len(edges)}，页面节点引用有效")

    required_dom_elements = (
        "3d-graph-container",
        "sidebar",
        "search-input",
        "btn-cascade-mode",
        "btn-expand-all",
        "btn-zoom-fit",
        "btn-auto-rotate",
        "detail-drawer",
        "drawer-title",
        "drawer-desc",
        "drawer-conns",
        "drawer-close-btn",
        "btn-release-focus",
        "btn-layout-force",
        "btn-layout-cluster",
        "btn-layout-hier",
        "filter-container",
    )
    missing_dom = [
        element_id
        for element_id in required_dom_elements
        if not re.search(rf"\bid=[\"']{re.escape(element_id)}[\"']", page)
    ]
    require(
        not missing_dom,
        "interactive_graph.html 缺少必要 DOM 节点: " + ", ".join(missing_dom),
    )

    require("卢美哌隆" in page, "interactive_graph.html 缺少“卢美哌隆”")
    require("卢玛哌酮" not in page, "interactive_graph.html 仍包含旧译名“卢玛哌酮”")
    require("3d-force-graph" in page, "interactive_graph.html 缺少 3d-force-graph")
    require("three-spritetext" in page, "interactive_graph.html 缺少 three-spritetext")
    require("onBackgroundClick" in page, "interactive_graph.html 缺少 onBackgroundClick")
    require(
        re.search(r"depthWrite\s*=\s*false", page) is not None,
        "interactive_graph.html 缺少 depthWrite 防闪烁设置",
    )
    print("[OK] 3D DOM、术语与释放焦点/防闪烁设置完整")


def main() -> None:
    html_content = verify_identical_files(HTML_PATHS, "HTML")
    kg_content = verify_identical_files(JSON_PATHS, "JSON")
    verify_graph_and_page(kg_content, html_content)
    references_by_html = verify_local_assets(HTML_PATHS)
    dist_index = OUTPUT_DIR / "dist" / "index.html"
    lite_index = OUTPUT_DIR / "dist_lite" / "index.html"
    verify_release_root(dist_index.parent, DIST_ROOT_FILES)
    verify_release_root(lite_index.parent, LITE_ROOT_FILES)
    for index_path in HTML_PATHS[1:]:
        verify_exact_release_assets(index_path, references_by_html[index_path])
    verify_release_asset_bytes(references_by_html)
    verify_zip_package(ZIP_PATH)
    print("===== 3D Web Functionality Verification Passed! =====")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
    try:
        main()
    except VerificationError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
