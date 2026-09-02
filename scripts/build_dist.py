# -*- coding: utf-8 -*-
"""打包生成标准的静态网站发布包并同步到 GitHub P·L·A·N·A 分支"""
import os
import json
import shutil
import zipfile
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "output"
dist = root / "dist"
dist.mkdir(parents=True, exist_ok=True)

# 1. 复制 index.html
shutil.copy2(root / "interactive_graph.html", dist / "index.html")

# 2. 复制 assets 目录 (如果存在)
dist_assets = dist / "assets"
if dist_assets.exists():
    shutil.rmtree(dist_assets)
if (root / "assets").exists():
    shutil.copytree(root / "assets", dist_assets)

# 3. 复制知识图谱数据
shutil.copy2(root / "knowledge_graph.json", dist / "knowledge_graph.json")

# 4. 创建 Vercel 静态配置
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
lite_dir = root / "dist_lite"
shutil.copy2(dist / "index.html", lite_dir / "index.html")
shutil.copy2(dist / "knowledge_graph.json", lite_dir / "knowledge_graph.json")

# 6. 生成精简 ZIP 发布包
zip_path = root / "stahl_web_deploy.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for file in lite_dir.rglob("*"):
        if file.is_file():
            arcname = file.relative_to(lite_dir)
            zipf.write(file, arcname)

print(f"[OK] 静态发布包已就绪: {dist}")
print(f"[OK] 精简部署包已就绪: {zip_path}")
