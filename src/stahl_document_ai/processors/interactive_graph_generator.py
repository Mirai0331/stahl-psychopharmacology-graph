# -*- coding: utf-8 -*-
"""WebGL/Three.js 3D 立体化全景脑科学知识图谱生成器 (高帧率防卡顿/抗闪烁/自由视角释放版)：
3D 立体多面体几何实体、3D 能量粒子流飞线 (Link Particle Streams)、
Three.js 材质属性级响应 (零 GC 重构卡顿)、SpriteText 深度测试优化 (零闪烁)、
点击空白背景与关闭按钮双重释放视角锁定。
"""
import json
from pathlib import Path
from stahl_document_ai.processors.graph_builder import PsychopharmacologyKnowledgeGraph


class InteractiveGraphGenerator:
    """高精 3D 精神药理学知识图谱可视化生成器"""

    CATEGORY_CONFIG = {
        "Drug": {
            "name": "精神药物",
            "color": "#5CC8F5",       # 临床青蓝
            "borderColor": "#238FBE",
            "glow": "rgba(92, 200, 245, 0.72)",
            "geometry": "sphere",
            "level": 2,
            "icon": "assets/63653-tablets-min.png",
            "badgeBg": "linear-gradient(135deg, #176786, #104A60)"
        },
        "DrugClass": {
            "name": "药物大类",
            "color": "#9B9CF9",       # 柔和靛蓝
            "borderColor": "#686AC5",
            "glow": "rgba(155, 156, 249, 0.72)",
            "geometry": "octahedron",
            "level": 1,
            "icon": "assets/Field_Inventory_Menu_02.png",
            "badgeBg": "linear-gradient(135deg, #5557A7, #3E3F7C)"
        },
        "Receptor": {
            "name": "受体与信号靶点",
            "color": "#48C9A5",       # 神经递质青绿
            "borderColor": "#258E73",
            "glow": "rgba(72, 201, 165, 0.72)",
            "geometry": "icosahedron",
            "level": 3,
            "icon": "assets/mission.png",
            "badgeBg": "linear-gradient(135deg, #17634F, #104739)"
        },
        "Pathway": {
            "name": "神经通路与可塑环路",
            "color": "#B692E6",       # 通路紫
            "borderColor": "#8063AE",
            "glow": "rgba(182, 146, 230, 0.72)",
            "geometry": "dodecahedron",
            "level": 4,
            "icon": "assets/complete.png",
            "badgeBg": "linear-gradient(135deg, #6D5198, #503A70)"
        },
        "Disease": {
            "name": "疾病与危重/难治表型",
            "color": "#E88BB7",       # 临床表型玫粉
            "borderColor": "#B45D87",
            "glow": "rgba(232, 139, 183, 0.72)",
            "geometry": "sphere",
            "level": 5,
            "icon": "assets/NOTE.png",
            "badgeBg": "linear-gradient(135deg, #8E4769, #69334D)"
        },
        "SideEffect": {
            "name": "不良反应",
            "color": "#F07D8C",       # 风险珊瑚红
            "borderColor": "#B94E5C",
            "glow": "rgba(240, 125, 140, 0.72)",
            "geometry": "cone",
            "level": 5,
            "icon": "assets/Goods_Icon_Gem_490_Preset_2.png",
            "badgeBg": "linear-gradient(135deg, #98404B, #6F2D35)"
        },
    }

    NODE_IMAGE_MAP = {
        "DRUG_ESKETAMINE": "assets/drug_sukailang.png",
        # 赖右苯丙胺没有专属素材时走类别占位，避免复用其他药物的结构式。
        "DRUG_METHYLPHENIDATE": "assets/drug_concerta_18mg.png",
        "DRUG_PREGABALIN": "assets/Pregabalin.png",
        "DRUG_CLONAZEPAM": "assets/clonazepam.png",
        "DRUG_TOLUDESVENLAFAXINE": "assets/pharma_capsule.png",
        "DRUG_DIMDAZENIL": "assets/63653-tablets-min.png",
        "DRUG_FAZAMOREXANT": "assets/icon_night.png",
        "DRUG_VORNOREXANT": "assets/icon_night.png",
        "DRUG_LEMBOREXANT": "assets/icon_night.png",
        "DRUG_DARIDOREXANT": "assets/icon_night.png",
        "DRUG_AGOMELATINE": "assets/icon_night.png",
        "DRUG_RAMELTEON": "assets/icon_evening.png",
        "DRUG_MODAFINIL": "assets/icon_morning.png",
        "DRUG_ARMODAFINIL": "assets/icon_morning.png",
        "DRUG_PITOLISANT": "assets/icon_morning.png",
        "REC_MT1_MT2": "assets/icon_night.png",
        "REC_OX1R_OX2R": "assets/icon_night.png",
        "REC_NMDA": "assets/mech_nmda_antag.png",
        "PATH_CIRCADIAN_SCN": "assets/icon_morning.png",
        "PATH_HYPOTHALAMIC_AROUSAL": "assets/icon_evening.png",
        "PATH_HIPPOCAMPAL_PLASTICITY": "assets/mech_rapid_onset.png",
        "PATH_CSTC_LOOPS": "assets/complete.png",
        "PATH_VTA_NACC_REWARD": "assets/Field_Inventory_Menu_02.png",
        "DIS_INSOMNIA": "assets/icon_night.png",
        "DIS_MDSI": "assets/mech_dissociation.png",
        "DIS_AUD": "assets/item_wine_glass.png",
        "DIS_ADHD": "assets/drug_ritalin_10mg.png",
        "CLS_ADHD_STIMULANT": "assets/badge_psychotropic_label.png",
    }

    RELATION_CONFIG = {
        "AGONIST": {"color": "#10B981", "particleColor": "#34D399", "label": "激动受体", "type": "positive"},
        "PARTIAL_AGONIST": {"color": "#F59E0B", "particleColor": "#FBBF24", "label": "部分激动", "type": "neutral"},
        "ANTAGONIST": {"color": "#EF4444", "particleColor": "#F87171", "label": "拮抗/阻断", "type": "negative"},
        "INVERSE_AGONIST": {"color": "#E11D48", "particleColor": "#FB7185", "label": "反向激动", "type": "negative"},
        "PAM": {"color": "#06B6D4", "particleColor": "#22D3EE", "label": "正向变构调节 (PAM)", "type": "modulate"},
        "BLOCKER": {"color": "#6366F1", "particleColor": "#818CF8", "label": "通道阻滞/酶抑制", "type": "block"},
        "INHIBITS": {"color": "#E11D48", "particleColor": "#F43F5E", "label": "再摄取抑制/逆转", "type": "inhibit"},
        "TREATS": {"color": "#38BDF8", "particleColor": "#7DD3FC", "label": "临床治疗/急救干预", "type": "treat"},
        "CAUSES": {"color": "#FB923C", "particleColor": "#FDBA74", "label": "诱发不良反应", "type": "harm"},
        "MODULATES": {"color": "#A855F7", "particleColor": "#C084FC", "label": "级联/环路调控", "type": "modulate"},
        "CORRELATED_WITH": {"color": "#EC4899", "particleColor": "#F472B6", "label": "病理关联/演进", "type": "link"},
        "IS_A": {"color": "#64748B", "particleColor": "#94A3B8", "label": "分类归属", "type": "class"},
    }

    @classmethod
    def generate_html(cls, graph: PsychopharmacologyKnowledgeGraph, output_path: Path) -> Path:
        degree_map = {}
        for e in graph.edges:
            degree_map[e.source] = degree_map.get(e.source, 0) + 1
            degree_map[e.target] = degree_map.get(e.target, 0) + 1

        nodes_3d = []
        for n in graph.nodes:
            cfg = cls.CATEGORY_CONFIG.get(n.category, {
                "name": n.category, "color": "#94A3B8", "borderColor": "#475569", "glow": "rgba(148,163,184,0.3)",
                "geometry": "sphere", "level": 3, "badgeBg": "#475569"
            })
            deg = degree_map.get(n.id, 1)
            is_critical = n.id in [
                "DIS_MDSI", "DIS_TRD", "DRUG_ESKETAMINE", "DRUG_LISDEXAMFETAMINE",
                "DRUG_TOLUDESVENLAFAXINE", "DRUG_DIMDAZENIL", "DRUG_FAZAMOREXANT", "DRUG_VORNOREXANT",
                "DRUG_ULOTARONT", "DRUG_ZURANOLONE", "DRUG_AUVELITY", "DRUG_PITOLISANT",
                "DRUG_AGOMELATINE", "REC_MT1_MT2", "PATH_CIRCADIAN_SCN", "REC_TAAR1", "REC_OX1R_OX2R",
                "REC_BDNF_TRKB", "REC_AMPA", "REC_MTORC1", "DRUG_VARENICLINE", "DRUG_LECANEMAB",
                "DRUG_LUMATEPERONE"
            ]
            node_val = min(13.0, max(4.5, (6.5 if is_critical else 4.0) + deg * 0.30))
            clean_label = n.label.split("(")[0].strip() if "(" in n.label else n.label
            custom_img = cls.NODE_IMAGE_MAP.get(n.id, "")

            nodes_3d.append({
                "id": n.id,
                "label": clean_label,
                "fullLabel": n.label,
                "category": n.category,
                "categoryName": cfg["name"],
                "description": n.description,
                "properties": n.properties,
                "degree": deg,
                "level": cfg["level"],
                "customImage": custom_img,
                "isCritical": is_critical,
                "color": cfg["color"],
                "borderColor": cfg["borderColor"],
                "glow": cfg["glow"],
                "geometry": cfg.get("geometry", "sphere"),
                "val": node_val
            })

        links_3d = []
        for i, e in enumerate(graph.edges):
            rel_cfg = cls.RELATION_CONFIG.get(e.relationship, {
                "color": "#475569", "particleColor": "#94A3B8", "label": e.label, "type": "link"
            })
            is_key_edge = (
                e.source in [
                    "DRUG_ESKETAMINE", "REC_AMPA", "REC_MTORC1", "REC_BDNF_TRKB", "DRUG_TOLUDESVENLAFAXINE",
                    "DRUG_DIMDAZENIL", "DRUG_FAZAMOREXANT", "DRUG_VORNOREXANT", "DRUG_ULOTARONT",
                    "DRUG_ZURANOLONE", "DRUG_AGOMELATINE", "REC_MT1_MT2", "REC_OX1R_OX2R", "DRUG_LUMATEPERONE"
                ]
                or e.target in ["DIS_MDSI", "DIS_TRD", "PATH_CIRCADIAN_SCN", "PATH_CSTC_LOOPS", "PATH_VTA_NACC_REWARD", "DIS_INSOMNIA"]
            )
            links_3d.append({
                "id": f"edge_{i}",
                "source": e.source,
                "target": e.target,
                "label": e.label,
                "relationship": e.relationship,
                "relName": rel_cfg["label"],
                "relType": rel_cfg["type"],
                "description": e.description,
                "weight": e.weight,
                "color": rel_cfg["color"],
                "particleColor": rel_cfg.get("particleColor", rel_cfg["color"]),
                "curvature": 0.18 if is_key_edge else 0.12,
                "particles": 3 if is_key_edge else 1,
                "particleSpeed": 0.007 if is_key_edge else 0.004,
                "width": max(1.2, min(3.6, e.weight * (1.6 if is_key_edge else 1.1))),
                "isKey": is_key_edge
            })

        graph_data_json = json.dumps({"nodes": nodes_3d, "links": links_3d}, ensure_ascii=False)

        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stahl 精神药理学精要 (第5版) · 3D 全景立体化脑科学知识图谱</title>
  
  <!-- WebGL 3D 动力学图谱引擎与 Three.js 依赖 -->
  <script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>
  <script src="https://unpkg.com/three-spritetext@1.8.2/dist/three-spritetext.min.js"></script>
  <script src="https://unpkg.com/3d-force-graph@1.73.4/dist/3d-force-graph.min.js"></script>

  <style>
    :root {{
      --bg-dark: #070B14;
      --bg-deep: #050811;
      --bg-card: rgba(10, 17, 29, 0.94);
      --bg-card-solid: #0A111D;
      --bg-card-hover: rgba(19, 31, 49, 0.98);
      --bg-soft: rgba(126, 153, 188, 0.08);
      --border-subtle: rgba(164, 184, 211, 0.13);
      --border-glow: rgba(92, 200, 245, 0.42);
      --border-glass: rgba(184, 204, 230, 0.18);
      --text-main: #F7FAFC;
      --text-sub: #AAB9CC;
      --text-muted: #728298;
      --accent-blue: #5CC8F5;
      --accent-blue-strong: #2698C9;
      --accent-purple: #B692E6;
      --accent-green: #48C9A5;
      --accent-amber: #F3C17C;
      --accent-pink: #E88BB7;
      --accent-cyan: #5CC8F5;
      --focus-ring: #F6D06F;
      --font-display: "Segoe UI Variable Display", "HarmonyOS Sans SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      --font-body: Inter, "Noto Sans SC", "Segoe UI Variable Text", "PingFang SC", "Microsoft YaHei", sans-serif;
      --font-data: "Cascadia Code", "SFMono-Regular", Consolas, monospace;
      --shadow-panel: 16px 0 48px rgba(0, 0, 0, 0.44);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ color-scheme: dark; background: var(--bg-dark); }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      height: 100dvh;
      display: flex;
      overflow: hidden;
      font-family: var(--font-body);
      font-size: 16px;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}
    button, input {{ font: inherit; }}
    button {{ appearance: none; }}
    ::selection {{ background: rgba(92, 200, 245, 0.26); color: #fff; }}

    /* 🌌 3D WebGL 视口画布容器 */
    #network-wrapper {{
      flex: 1;
      height: 100%;
      position: relative;
      min-width: 0;
      background: radial-gradient(ellipse at 52% 46%, rgba(20, 43, 70, 0.74) 0%, rgba(7, 11, 20, 0.96) 62%, var(--bg-deep) 100%);
      overflow: hidden;
    }}
    #3d-graph-container {{
      width: 100%;
      height: 100%;
      outline: none;
    }}

    /* 🛡️ 左侧控制侧边栏 (Cyber-Medical Glass) */
    #sidebar {{
      width: 420px;
      flex: 0 0 420px;
      background: var(--bg-card);
      backdrop-filter: blur(24px) saturate(116%);
      -webkit-backdrop-filter: blur(24px) saturate(116%);
      border-right: 1px solid var(--border-glass);
      display: flex;
      flex-direction: column;
      padding: 20px;
      z-index: 20;
      box-shadow: var(--shadow-panel);
      overflow-y: auto;
      overscroll-behavior: contain;
      scrollbar-width: thin;
      scrollbar-color: rgba(92, 200, 245, 0.34) transparent;
    }}
    #sidebar::-webkit-scrollbar {{ width: 5px; }}
    #sidebar::-webkit-scrollbar-thumb {{ background: rgba(56, 189, 248, 0.3); border-radius: 4px; }}

    .header-box {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .header-logo {{
      width: 44px;
      height: 44px;
      flex: 0 0 44px;
      border-radius: 11px;
      background: linear-gradient(145deg, rgba(92, 200, 245, 0.18), rgba(182, 146, 230, 0.14));
      border: 1px solid var(--border-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 24px rgba(24, 109, 148, 0.22);
      overflow: hidden;
    }}
    .header-logo img {{ width: 32px; height: 32px; object-fit: contain; }}

    .header-title {{
      font-family: var(--font-display);
      font-size: 1.14rem;
      font-weight: 760;
      letter-spacing: -0.025em;
      line-height: 1.2;
      background: linear-gradient(112deg, #FFFFFF 0%, #B9E9FA 52%, #CFB9ED 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .header-kicker {{ font-family: var(--font-data); font-size: 0.66rem; color: var(--text-sub); font-weight: 600; letter-spacing: 0.035em; margin-top: 3px; }}
    .header-sub {{ font-size: 0.75rem; color: var(--text-sub); margin-bottom: 14px; line-height: 1.58; }}

    .mode-banner {{
      display: flex;
      align-items: center;
      gap: 10px;
      justify-content: space-between;
      background: rgba(92, 200, 245, 0.075);
      border: 1px solid rgba(92, 200, 245, 0.26);
      border-radius: 10px;
      padding: 9px 10px 9px 12px;
      margin-bottom: 14px;
      font-size: 0.74rem;
      line-height: 1.45;
    }}
    .mode-pill {{
      flex: 0 0 auto;
      background: rgba(92, 200, 245, 0.14);
      color: #C7EEFC;
      padding: 5px 9px;
      border-radius: 7px;
      font-weight: 700;
      font-size: 0.68rem;
      cursor: pointer;
      transition: background-color 0.18s, color 0.18s, border-color 0.18s;
      border: 1px solid rgba(92, 200, 245, 0.32);
    }}
    .mode-pill:hover {{ background: rgba(92, 200, 245, 0.24); color: #fff; }}

    .scenario-section {{ margin-bottom: 15px; }}
    .section-title {{
      font-family: var(--font-display);
      font-size: 0.70rem;
      font-weight: 720;
      letter-spacing: 0.045em;
      color: var(--text-sub);
      margin-bottom: 9px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
    }}
    .section-meta {{ font-family: var(--font-data); font-size: 0.64rem; font-weight: 600; color: var(--accent-blue); letter-spacing: 0; }}
    .preset-chips {{ display: flex; flex-wrap: wrap; gap: 7px; }}
    .chip {{
      padding: 6px 9px;
      border-radius: 8px;
      font-size: 0.71rem;
      line-height: 1.25;
      cursor: pointer;
      background: var(--bg-soft);
      border: 1px solid var(--border-subtle);
      color: #C7D3E2;
      transition: background-color 0.18s, border-color 0.18s, color 0.18s, box-shadow 0.18s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-align: left;
    }}
    .chip img {{ width: 14px; height: 14px; object-fit: contain; border-radius: 3px; }}
    .chip:hover {{ background: rgba(92, 200, 245, 0.12); border-color: rgba(92, 200, 245, 0.48); color: #fff; }}
    .chip.active {{ background: #176786; border-color: #63D3FF; color: #fff; font-weight: 700; box-shadow: 0 0 0 1px rgba(99, 211, 255, 0.12), 0 6px 18px rgba(13, 83, 112, 0.28); }}

    .search-wrapper {{ position: relative; margin-bottom: 15px; }}
    .search-row {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 7px; }}
    .search-field {{ position: relative; min-width: 0; }}
    .search-input {{
      width: 100%;
      min-height: 42px;
      padding: 10px 12px 10px 39px;
      background: rgba(11, 20, 33, 0.86);
      border: 1px solid var(--border-glass);
      border-radius: 10px;
      color: #fff;
      font-size: 0.82rem;
      outline: none;
      transition: background-color 0.18s, border-color 0.18s, box-shadow 0.18s;
    }}
    .search-input::placeholder {{ color: #718198; }}
    .search-input:focus {{ border-color: var(--accent-blue); box-shadow: 0 0 0 3px rgba(92, 200, 245, 0.14); background: rgba(12, 23, 38, 0.98); }}
    .search-icon-img {{ position: absolute; left: 13px; top: 12px; width: 17px; height: 17px; opacity: 0.66; pointer-events: none; }}
    .search-submit {{
      min-height: 42px;
      padding: 0 13px;
      border-radius: 10px;
      border: 1px solid rgba(92, 200, 245, 0.42);
      background: rgba(92, 200, 245, 0.12);
      color: #C7EEFC;
      font-size: 0.75rem;
      font-weight: 720;
      cursor: pointer;
      transition: background-color 0.18s, color 0.18s, border-color 0.18s;
    }}
    .search-submit:hover {{ background: rgba(92, 200, 245, 0.22); color: #fff; border-color: var(--accent-blue); }}
    .search-status {{ display: none; margin-top: 7px; padding-left: 2px; color: var(--text-sub); font-size: 0.69rem; line-height: 1.45; }}
    .search-status.show {{ display: block; }}
    .search-status.error {{ color: #FFADB8; }}

    .layout-switcher {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 7px;
      margin-bottom: 15px;
    }}
    .layout-btn {{
      min-height: 38px;
      padding: 8px 6px;
      font-size: 0.71rem;
      font-weight: 600;
      background: var(--bg-soft);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      color: #C7D3E2;
      cursor: pointer;
      text-align: center;
      transition: background-color 0.18s, border-color 0.18s, color 0.18s, box-shadow 0.18s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
    }}
    .layout-btn:hover {{ background: rgba(92, 200, 245, 0.10); border-color: rgba(92, 200, 245, 0.38); }}
    .layout-btn.active {{ background: rgba(92, 200, 245, 0.15); border-color: var(--accent-blue); color: #AEE7FA; box-shadow: inset 0 0 0 1px rgba(92, 200, 245, 0.08); font-weight: 700; }}

    .filter-list {{ display: flex; flex-direction: column; gap: 6px; margin-bottom: 15px; }}
    .filter-item {{
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 10px;
      background: rgba(15, 25, 40, 0.58);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      cursor: pointer;
      color: var(--text-main);
      font-size: 0.76rem;
      transition: background-color 0.18s, border-color 0.18s, color 0.18s;
      text-align: left;
    }}
    .filter-item:hover {{ background: rgba(92, 200, 245, 0.10); border-color: rgba(92, 200, 245, 0.42); }}
    .filter-item.active {{ background: rgba(92, 200, 245, 0.15); border-color: var(--accent-blue); font-weight: 700; }}
    .filter-left {{ display: flex; align-items: center; gap: 9px; min-width: 0; }}
    .filter-icon {{ width: 16px; height: 16px; object-fit: contain; }}
    .filter-dot {{ width: 8px; height: 8px; border-radius: 50%; box-shadow: 0 0 10px currentColor; }}
    .filter-count {{ font-family: var(--font-data); font-size: 0.66rem; color: var(--text-sub); background: rgba(255,255,255,0.07); padding: 2px 7px; border-radius: 999px; }}

    .text-view {{
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      background: rgba(15, 25, 40, 0.48);
      overflow: hidden;
    }}
    .text-view summary {{
      min-height: 40px;
      padding: 9px 11px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      color: #CFDAE7;
      font-size: 0.74rem;
      font-weight: 680;
      cursor: pointer;
      list-style: none;
    }}
    .text-view summary::-webkit-details-marker {{ display: none; }}
    .text-view summary::after {{ content: "展开"; font-family: var(--font-data); color: var(--text-muted); font-size: 0.62rem; font-weight: 600; }}
    .text-view[open] summary {{ border-bottom: 1px solid var(--border-subtle); }}
    .text-view[open] summary::after {{ content: "收起"; }}
    .text-view-content {{ padding: 10px; }}
    .text-view-heading {{ margin: 2px 0 7px; color: var(--text-sub); font-size: 0.67rem; font-weight: 700; }}
    .accessible-node-list {{ display: flex; flex-wrap: wrap; gap: 6px; max-height: 150px; overflow-y: auto; padding-bottom: 8px; }}
    .accessible-node-btn {{
      padding: 5px 7px;
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      background: rgba(255,255,255,0.045);
      color: #D3DCE8;
      font-size: 0.68rem;
      cursor: pointer;
      text-align: left;
    }}
    .accessible-node-btn:hover {{ border-color: rgba(92, 200, 245, 0.46); background: rgba(92, 200, 245, 0.10); }}
    .accessible-link-list {{ max-height: 180px; overflow-y: auto; list-style: none; display: grid; gap: 6px; }}
    .accessible-link-list li {{ padding: 7px 8px; border-left: 2px solid rgba(92, 200, 245, 0.34); background: rgba(255,255,255,0.035); color: #C8D3E0; font-size: 0.67rem; line-height: 1.48; }}
    .accessible-link-desc {{ display: block; margin-top: 2px; color: var(--text-muted); }}

    /* 💎 临床药理多维详情看板 (Clinical Holographic Dashboard) */
    #detail-drawer {{
      margin-top: 10px;
      background: linear-gradient(150deg, rgba(15, 25, 41, 0.98), rgba(8, 14, 24, 0.99));
      border: 1px solid var(--border-glow);
      border-radius: 12px;
      padding: 15px;
      display: none;
      box-shadow: 0 16px 36px rgba(0,0,0,0.42), inset 0 1px 0 rgba(255,255,255,0.07);
      animation: slideInUp 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }}
    #detail-drawer.show {{ display: block; }}
    @keyframes slideInUp {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    .drawer-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
    .drawer-header-left {{ display: flex; align-items: center; gap: 8px; }}
    .drawer-badge {{ display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 8px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}
    
    .drawer-close-btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--text-sub);
      width: 30px;
      height: 30px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 700;
      transition: background-color 0.18s, border-color 0.18s, color 0.18s;
    }}
    .drawer-close-btn:hover {{ background: rgba(240, 125, 140, 0.16); border-color: rgba(240, 125, 140, 0.52); color: #FFD9DE; }}

    /* 🖼️ 3D 高精展柜窗口 */
    .drawer-lightbox {{
      width: 100%;
      height: 110px;
      border-radius: 10px;
      background: radial-gradient(circle at 50% 50%, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12px;
      overflow: hidden;
      position: relative;
      box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }}
    .drawer-lightbox img {{
      max-width: 86%;
      max-height: 86%;
      object-fit: contain;
      filter: drop-shadow(0 6px 16px rgba(0,0,0,0.6));
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    .drawer-lightbox:hover img {{ transform: scale(1.04); }}
    .lightbox-tag {{
      position: absolute;
      bottom: 6px;
      right: 8px;
      font-size: 0.64rem;
      color: #94A3B8;
      background: rgba(0, 0, 0, 0.6);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(255,255,255,0.08);
    }}

    .drawer-title {{ font-family: var(--font-display); font-size: 1.08rem; font-weight: 760; color: #fff; margin-bottom: 9px; line-height: 1.38; letter-spacing: -0.016em; }}
    .drawer-desc-card {{
      font-size: 0.78rem;
      color: #CDD8E6;
      line-height: 1.68;
      margin-bottom: 12px;
      background: rgba(154, 179, 210, 0.055);
      padding: 11px 12px;
      border-radius: 9px;
      border: 1px solid var(--border-subtle);
      white-space: pre-line;
    }}

    /* 🧬 机制传导流条带 (Flow Ribbon) */
    .flow-ribbon {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 14px;
      background: rgba(15, 23, 42, 0.6);
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid rgba(56, 189, 248, 0.2);
    }}
    .flow-ribbon-title {{ font-size: 0.70rem; font-weight: 700; color: var(--accent-blue); text-transform: uppercase; letter-spacing: 0.05em; }}
    .flow-steps {{ display: flex; flex-wrap: wrap; align-items: center; gap: 5px; font-size: 0.74rem; color: #E2E8F0; }}
    .flow-step {{ background: rgba(56, 189, 248, 0.15); padding: 3px 7px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.3); }}
    .flow-arrow {{ color: var(--accent-amber); font-weight: bold; font-size: 0.8rem; }}

    .drawer-actions {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }}
    .drawer-btn {{
      flex: 1;
      padding: 7px 10px;
      border-radius: 8px;
      background: rgba(92, 200, 245, 0.10);
      border: 1px solid rgba(92, 200, 245, 0.32);
      color: #BCEBFB;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: background-color 0.18s, border-color 0.18s, color 0.18s;
    }}
    .drawer-btn:hover {{ background: rgba(92, 200, 245, 0.20); border-color: var(--accent-blue); color: #fff; }}

    .drawer-conns-title {{ font-size: 0.76rem; font-weight: 700; color: var(--text-sub); text-transform: uppercase; margin-bottom: 10px; display: flex; justify-content: space-between; }}
    .drawer-conns-list {{ display: flex; flex-direction: column; gap: 6px; max-height: 180px; overflow-y: auto; font-size: 0.78rem; }}
    .conn-tag {{
      width: 100%;
      padding: 7px 10px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      color: var(--text-main);
      font: inherit;
      text-align: left;
      transition: background-color 0.18s, border-color 0.18s;
      border: 1px solid transparent;
    }}
    .conn-tag:hover {{ background: rgba(92, 200, 245, 0.14); border-color: var(--accent-blue); }}
    .conn-rel {{ font-weight: 700; }}
    .conn-rel.positive {{ color: #34D399; }}
    .conn-rel.negative {{ color: #F87171; }}
    .conn-rel.modulate {{ color: #C084FC; }}
    .conn-rel.treat {{ color: #38BDF8; }}

    /* 🛰️ 悬浮工具栏 (Floating Control Capsule) */
    .top-floating-bar {{
      position: absolute;
      top: 16px;
      right: 16px;
      display: flex;
      justify-content: flex-end;
      flex-wrap: wrap;
      gap: 8px;
      max-width: calc(100% - 32px);
      z-index: 10;
    }}
    .tool-btn {{
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-glass);
      color: #D5DEEA;
      min-height: 38px;
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 0.75rem;
      font-weight: 650;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 7px;
      box-shadow: 0 8px 22px rgba(0,0,0,0.28);
      transition: background-color 0.18s, border-color 0.18s, color 0.18s, box-shadow 0.18s;
    }}
    .tool-btn img {{ width: 15px; height: 15px; object-fit: contain; }}
    .tool-btn:hover {{ background: rgba(92, 200, 245, 0.16); border-color: var(--accent-blue); color: #fff; }}
    .tool-btn.highlight {{ background: #176786; border-color: #63D3FF; color: #fff; box-shadow: 0 8px 24px rgba(13, 83, 112, 0.34); }}
    .tool-btn.active {{ background: rgba(92, 200, 245, 0.17); border-color: var(--accent-blue); color: #AEE7FA; }}

    .mobile-panel-toggle {{
      display: none;
      position: absolute;
      top: 12px;
      left: 12px;
      z-index: 60;
      min-height: 40px;
      padding: 8px 11px;
      border-radius: 10px;
      border: 1px solid rgba(92, 200, 245, 0.48);
      background: rgba(8, 15, 26, 0.92);
      color: #D8F4FE;
      box-shadow: 0 8px 24px rgba(0,0,0,0.34);
      font-size: 0.73rem;
      font-weight: 720;
      cursor: pointer;
    }}

    /* 🎯 悬浮微型卡片 (Hover Tooltip HUD) */
    #hover-hud {{
      position: absolute;
      pointer-events: none;
      display: none;
      z-index: 30;
      background: rgba(10, 16, 28, 0.94);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-glow);
      border-radius: 10px;
      padding: 8px 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.65);
      font-size: 0.76rem;
      color: #F8FAFC;
      max-width: 260px;
      transform: translate(12px, 12px);
    }}
    #hover-hud-title {{ font-weight: 800; color: var(--accent-blue); margin-bottom: 3px; }}
    #hover-hud-cat {{ font-size: 0.68rem; color: #94A3B8; }}

    /* 3D 漫游提示条 */
    .controls-hint {{
      position: absolute;
      bottom: 14px;
      right: 16px;
      background: rgba(10, 16, 28, 0.82);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 7px 14px;
      font-size: 0.68rem;
      color: var(--text-sub);
      z-index: 10;
      pointer-events: none;
      display: flex;
      gap: 14px;
    }}
    .controls-hint span {{ display: flex; align-items: center; gap: 4px; }}
    .controls-hint kbd {{ background: rgba(255,255,255,0.12); padding: 2px 6px; border-radius: 4px; color: #E2E8F0; font-size: 0.68rem; font-weight: 600; }}

    .sr-only {{
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }}
    :where(button, input, [tabindex]):focus-visible {{
      outline: 3px solid var(--focus-ring);
      outline-offset: 3px;
    }}

    @media (max-width: 1180px) {{
      #sidebar {{ width: 380px; flex-basis: 380px; padding: 17px; }}
      .header-title {{ font-size: 1.04rem; }}
      .top-floating-bar {{ gap: 6px; }}
      .tool-btn {{ min-height: 36px; padding: 7px 9px; font-size: 0.69rem; }}
      .controls-hint {{ max-width: calc(100% - 32px); flex-wrap: wrap; justify-content: flex-end; gap: 8px 12px; }}
    }}

    @media (max-width: 900px) {{
      body {{ display: block; }}
      #network-wrapper {{ position: fixed; inset: 0; width: 100%; height: 100dvh; }}
      #sidebar {{
        position: fixed;
        left: 8px;
        right: 8px;
        bottom: 8px;
        width: auto;
        height: min(72dvh, 620px);
        max-height: calc(100dvh - 72px);
        padding: 15px;
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        box-shadow: 0 -18px 48px rgba(0,0,0,0.54);
        transform: translateY(0);
        transition: transform 0.26s cubic-bezier(0.2, 0.8, 0.2, 1);
        z-index: 50;
      }}
      body.sidebar-collapsed #sidebar {{ transform: translateY(calc(100% + 18px)); }}
      .mobile-panel-toggle {{ display: inline-flex; align-items: center; }}
      .top-floating-bar {{
        top: 12px;
        left: 118px;
        right: 10px;
        max-width: none;
        flex-wrap: nowrap;
        justify-content: flex-start;
        overflow-x: auto;
        padding: 0 2px 7px;
        scrollbar-width: none;
      }}
      .top-floating-bar::-webkit-scrollbar {{ display: none; }}
      .tool-btn {{ flex: 0 0 auto; min-height: 40px; }}
      .tool-btn img {{ width: 14px; height: 14px; }}
      .controls-hint {{ display: none; }}
      #hover-hud {{ max-width: min(250px, calc(100vw - 24px)); }}
      .header-sub {{ margin-bottom: 12px; }}
      .mode-banner {{ margin-bottom: 12px; }}
      .scenario-section {{ margin-bottom: 13px; }}
      .search-row {{ grid-template-columns: minmax(0, 1fr) 54px; }}
      .search-submit {{ padding: 0 9px; }}
      .chip {{ min-height: 34px; }}
    }}

    @media (max-width: 420px) {{
      #sidebar {{ height: min(76dvh, 640px); padding: 14px; }}
      .header-title {{ font-size: 1rem; }}
      .header-sub {{ font-size: 0.71rem; }}
      .preset-chips {{ gap: 6px; }}
      .chip {{ max-width: 100%; }}
      .layout-btn {{ font-size: 0.68rem; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{
        scroll-behavior: auto !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }}
    }}

    @media (forced-colors: active) {{
      .header-title {{
        background: none;
        color: CanvasText;
        -webkit-text-fill-color: CanvasText;
      }}
      :where(button, input, summary, [tabindex]) {{ forced-color-adjust: auto; }}
      .filter-dot {{ box-shadow: none; }}
    }}
  </style>
</head>
<body>

  <!-- 左侧控制面板 -->
  <aside id="sidebar" aria-label="图谱探索控制面板">
    <div class="header-box">
      <div class="header-logo">
        <img src="assets/drug_sukailang.png" alt="Stahl Graph Logo" />
      </div>
      <div>
        <h1 class="header-title">Stahl 精神药理学精要</h1>
        <div class="header-kicker">第5版 · 3D 神经药理证据图谱</div>
      </div>
    </div>
    <div class="header-sub">
      覆盖全书 14 大核心章节 · {len(graph.nodes)} 个药物/受体/回路实体 · {len(graph.edges)} 条关系证据。选择节点，追踪完整药理链路。
    </div>

    <div class="mode-banner">
      <span id="mode-text" aria-live="polite">单点级联探索 · 点击节点展开，点击空白释放</span>
      <button type="button" class="mode-pill" id="reset-filter-btn">重置</button>
    </div>

    <form class="search-wrapper" id="search-form" role="search">
      <label class="sr-only" for="search-input">搜索药物、受体或疾病</label>
      <div class="search-row">
        <div class="search-field">
          <img src="assets/NOTE.png" class="search-icon-img" alt="" />
          <input type="search" id="search-input" class="search-input" autocomplete="off" list="search-suggestions" placeholder="搜索药物、受体或疾病" />
          <datalist id="search-suggestions"></datalist>
        </div>
        <button type="submit" class="search-submit">定位</button>
      </div>
      <div class="search-status" id="search-status" role="status" aria-live="polite"></div>
    </form>

    <!-- 20+ 核心专病场景矩阵 -->
    <div class="scenario-section">
      <div class="section-title">
        <span>前沿机制与专病透视预设</span>
        <span class="section-meta">20+ 临床场景</span>
      </div>
      <div class="preset-chips">
        <button type="button" class="chip active" data-preset="INITIAL_SEED" aria-pressed="true">
          <img src="assets/drug_sukailang.png" alt="" />
          <span>速开朗® TRD/自杀干预 (开屏)</span>
        </button>
        <button type="button" class="chip" data-preset="TRD_KETAMINE" aria-pressed="false">
          <img src="assets/mech_nmda_antag.png" alt="" />
          <span>NMDA 阻断与突触可塑性</span>
        </button>
        <button type="button" class="chip" data-preset="ADHD_OROS" aria-pressed="false">
          <img src="assets/drug_concerta_18mg.png" alt="" />
          <span>专注达® OROS 控释与前额叶</span>
        </button>
        <button type="button" class="chip" data-preset="DORA_INSOMNIA" aria-pressed="false">
          <img src="assets/icon_night.png" alt="" />
          <span>DORA 双食欲素拮抗 (达卫可®)</span>
        </button>
        <button type="button" class="chip" data-preset="LUMATEPERONE" aria-pressed="false">
          <img src="assets/pharma_capsule.png" alt="" />
          <span>卢美哌隆 (Caplyta) 5-HT2A/D2/SERT</span>
        </button>
        <button type="button" class="chip" data-preset="TAAR1_SCHIZO" aria-pressed="false">
          <img src="assets/complete.png" alt="" />
          <span>TAAR1/5-HT1A 激动剂 (Ulotaront)</span>
        </button>
        <button type="button" class="chip" data-preset="PPD_GABA" aria-pressed="false">
          <img src="assets/pharma_capsule.png" alt="" />
          <span>产后抑郁 GABA PAM (祖拉诺酮)</span>
        </button>
        <button type="button" class="chip" data-preset="SCN_CIRCADIAN" aria-pressed="false">
          <img src="assets/icon_morning.png" alt="" />
          <span>昼夜节律 MT1/MT2/5-HT2C</span>
        </button>
        <button type="button" class="chip" data-preset="SNDRI_TRIPLE" aria-pressed="false">
          <img src="assets/63653-tablets-min.png" alt="" />
          <span>SNDRI 三重再摄取 (若舒达®)</span>
        </button>
        <button type="button" class="chip" data-preset="DIMDAZENIL" aria-pressed="false">
          <img src="assets/63653-tablets-min.png" alt="" />
          <span>地达西尼 (京诺宁®) PAM</span>
        </button>
        <button type="button" class="chip" data-preset="AD_AMYLOID" aria-pressed="false">
          <img src="assets/NOTE.png" alt="" />
          <span>阿尔茨海默病 Aβ 单抗 (仑卡奈)</span>
        </button>
      </div>
    </div>

    <!-- 3D 空间排布引擎切换 -->
    <div class="scenario-section">
      <div class="section-title">
        <span>3D 空间排布引擎</span>
        <span class="section-meta" style="color:var(--accent-purple);">三维空间几何</span>
      </div>
      <div class="layout-switcher">
        <button type="button" class="layout-btn active" id="btn-layout-force" aria-pressed="true">自由星群</button>
        <button type="button" class="layout-btn" id="btn-layout-cluster" aria-pressed="false">同心分层</button>
        <button type="button" class="layout-btn" id="btn-layout-hier" aria-pressed="false">机制柱阵</button>
      </div>
    </div>

    <!-- 实体类别过滤 -->
    <div class="scenario-section">
      <div class="section-title">
        <span>证据闭环实体子图</span>
        <span class="section-meta" style="color:var(--text-sub);">按关系连接</span>
      </div>
      <div class="filter-list" id="filter-container"></div>
    </div>

    <!-- WebGL 图谱的键盘与文本等价视图 -->
    <div class="scenario-section">
      <details class="text-view" id="text-view">
        <summary>当前可见节点与关系</summary>
        <div class="text-view-content">
          <div class="text-view-heading" id="accessible-node-heading">节点</div>
          <div class="accessible-node-list" id="accessible-node-list" aria-labelledby="accessible-node-heading"></div>
          <div class="text-view-heading" id="accessible-link-heading">关系证据</div>
          <ul class="accessible-link-list" id="accessible-link-list" tabindex="0" aria-labelledby="accessible-link-heading"></ul>
        </div>
      </details>
    </div>

    <!-- 临床药理多维看板 (详情抽屉) -->
    <section id="detail-drawer" aria-labelledby="drawer-title" aria-hidden="true">
      <div class="drawer-header">
        <div class="drawer-header-left">
          <span class="drawer-badge" id="drawer-badge">类别</span>
          <span id="drawer-level" style="font-size:0.68rem; color:#94A3B8; font-weight:600;">脑区级联</span>
        </div>
        <button type="button" class="drawer-close-btn" id="drawer-close-btn" title="收起详情并释放视角" aria-label="收起详情并释放视角">×</button>
      </div>
      
      <!-- 3D 晶莹展柜窗口 -->
      <div class="drawer-lightbox" id="drawer-lightbox">
        <img id="drawer-art" src="assets/drug_sukailang.png" alt="" />
        <span class="lightbox-tag" id="drawer-art-tag">3D 药学图解</span>
      </div>

      <h2 class="drawer-title" id="drawer-title" tabindex="-1">实体详情</h2>
      <div class="drawer-desc-card" id="drawer-desc">...</div>

      <!-- 操作快捷按钮 -->
      <div class="drawer-actions">
        <button class="drawer-btn" id="btn-release-focus">
          <span>🔓 释放视角锁定 (返回漫游)</span>
        </button>
      </div>

      <!-- 机制传导流条带 -->
      <div class="flow-ribbon" id="flow-ribbon" style="display:none;">
        <div class="flow-ribbon-title">药理机制传导流</div>
        <div class="flow-steps" id="flow-steps"></div>
      </div>

      <div class="drawer-conns-title">
        <span>关联靶点与神经回路</span>
        <span style="font-size:0.68rem; color:#38BDF8;" id="conns-count">0 关联</span>
      </div>
      <div class="drawer-conns-list" id="drawer-conns"></div>
    </section>
  </aside>

  <!-- 3D 图谱画布容器 -->
  <main id="network-wrapper" tabindex="-1" aria-label="3D 精神药理学关系图谱">
    <button type="button" class="mobile-panel-toggle" id="mobile-panel-toggle" aria-controls="sidebar" aria-expanded="true">收起探索面板</button>
    <div id="3d-graph-container" role="region" aria-label="可旋转、缩放并选择节点的三维关系图"></div>
    <div id="network-container" style="display:none;"></div>
    
    <!-- 悬浮微型 HUD 提示卡 -->
    <div id="hover-hud" role="status" aria-live="polite">
      <div id="hover-hud-title">实体名称</div>
      <div id="hover-hud-cat">类别 · 0 关联</div>
    </div>

    <!-- 顶部操作胶囊 -->
    <nav class="top-floating-bar" aria-label="图谱视图控制">
      <button type="button" class="tool-btn highlight" id="btn-cascade-mode" aria-pressed="true">
        <img src="assets/mission.png" alt="" />
        单点级联探索
      </button>
      <button type="button" class="tool-btn" id="btn-expand-all" aria-pressed="false">
        <img src="assets/Field_Inventory_Menu_02.png" alt="" />
        全景宏观总网
      </button>
      <button type="button" class="tool-btn" id="btn-auto-rotate" aria-pressed="false">
        巡航旋转
      </button>
      <button type="button" class="tool-btn" id="btn-relax-physics">
        <img src="assets/complete.png" alt="" />
        空间舒展
      </button>
      <button type="button" class="tool-btn" id="btn-zoom-fit">
        <img src="assets/NOTE.png" alt="" />
        全景视点 (释放)
      </button>
    </nav>

    <!-- 3D 漫游操作提示 -->
    <div class="controls-hint">
      <span><kbd>左键单击空白</kbd> 释放视角/取消固定</span>
      <span><kbd>左键拖拽</kbd> 3D 自由旋转</span>
      <span><kbd>右键拖拽</kbd> 平移</span>
      <span><kbd>滚轮</kbd> 推拉</span>
    </div>
  </main>

  <script>
    const graphRawData = {graph_data_json};
    const categoryConfig = {json.dumps(cls.CATEGORY_CONFIG, ensure_ascii=False)};
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const cameraDuration = () => prefersReducedMotion.matches ? 0 : 900;

    function setActiveInGroup(selector, activeElement = null) {{
      document.querySelectorAll(selector).forEach(element => {{
        const isActive = element === activeElement;
        element.classList.toggle('active', isActive);
        if (element.hasAttribute('aria-pressed')) {{
          element.setAttribute('aria-pressed', String(isActive));
        }}
      }});
    }}

    function setPrimaryViewMode(mode) {{
      const cascadeButton = document.getElementById('btn-cascade-mode');
      const expandButton = document.getElementById('btn-expand-all');
      const cascadeActive = mode === 'cascade';
      const expandActive = mode === 'all';
      cascadeButton.classList.toggle('highlight', cascadeActive);
      expandButton.classList.toggle('highlight', expandActive);
      cascadeButton.setAttribute('aria-pressed', String(cascadeActive));
      expandButton.setAttribute('aria-pressed', String(expandActive));
    }}
    
    const catCounts = {{}};
    graphRawData.nodes.forEach(n => {{
      catCounts[n.category] = (catCounts[n.category] || 0) + 1;
    }});

    const adjMap = {{}};
    graphRawData.nodes.forEach(n => adjMap[n.id] = new Set());
    graphRawData.links.forEach(e => {{
      const u = typeof e.source === 'object' ? e.source.id : e.source;
      const v = typeof e.target === 'object' ? e.target.id : e.target;
      if (adjMap[u]) adjMap[u].add(v);
      if (adjMap[v]) adjMap[v].add(u);
    }});

    const searchSuggestions = document.getElementById('search-suggestions');
    graphRawData.nodes
      .slice()
      .sort((a, b) => a.fullLabel.localeCompare(b.fullLabel, 'zh-CN'))
      .forEach(node => {{
        const option = document.createElement('option');
        option.value = node.fullLabel;
        option.label = node.categoryName;
        searchSuggestions.appendChild(option);
      }});

    // 实体类别侧边栏渲染
    const filterContainer = document.getElementById('filter-container');
    Object.keys(categoryConfig).forEach(cat => {{
      const cfg = categoryConfig[cat];
      const count = catCounts[cat] || 0;
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'filter-item';
      item.dataset.category = cat;
      item.setAttribute('aria-pressed', 'false');
      item.innerHTML = `
        <div class="filter-left">
          <img src="${{cfg.icon}}" class="filter-icon" alt="" />
          <div class="filter-dot" style="background: ${{cfg.color}}; box-shadow: 0 0 10px ${{cfg.color}};"></div>
          <span>${{cfg.name}} (${{cat}})</span>
        </div>
        <span class="filter-count">${{count}}</span>
      `;
      
      item.addEventListener('click', function() {{
        setActiveInGroup('.filter-item', this);
        setActiveInGroup('.preset-chips .chip');
        isCascadeMode = false;
        setPrimaryViewMode('filtered');

        const primaryNodes = graphRawData.nodes.filter(n => n.category === cat);
        const primaryIds = new Set(primaryNodes.map(n => n.id));
        
        const linkedIds = new Set(primaryIds);
        primaryIds.forEach(pId => {{
          const neighbors = adjMap[pId] || new Set();
          neighbors.forEach(nId => linkedIds.add(nId));
        }});

        updateGraphSubView(linkedIds);
        document.getElementById('mode-text').innerText = `已激活: ${{cfg.name}} 证据关系全网 (共 ${{linkedIds.size}} 节点)`;
        if (primaryNodes.length > 0) {{
          focusNode3D(primaryNodes[0].id);
        }}
      }});
      filterContainer.appendChild(item);
    }});

    // 🌌 3D Force Graph 初始化与实体立体化建模
    const container = document.getElementById('3d-graph-container');
    let highlightNodes = new Set();
    let highlightLinks = new Set();
    let hoverNodeObj = null;
    let isAutoRotating = false;
    let currentLayoutMode = 'force'; // 'force', 'sphere', 'cylinder'
    let activeFocusedNodeId = null;
    let isCascadeMode = true;

    // 共享几何体缓存（彻底杜绝 GC 压力与内存浪费）
    const geomCache = {{
      sphere: new THREE.SphereGeometry(1, 16, 16),
      octahedron: new THREE.OctahedronGeometry(1.1),
      icosahedron: new THREE.IcosahedronGeometry(1.0),
      dodecahedron: new THREE.DodecahedronGeometry(1.1),
      cone: new THREE.ConeGeometry(0.9, 1.6, 8)
    }};

    const Graph = ForceGraph3D()(container)
      .backgroundColor('#070B14')
      .showNavInfo(false)
      .nodeRelSize(5.5)
      .nodeResolution(16)
      .linkCurvature('curvature')
      .linkCurveRotation(0.25)
      .linkDirectionalParticles(link => prefersReducedMotion.matches ? 0 : link.particles)
      .linkDirectionalParticleSpeed(link => prefersReducedMotion.matches ? 0 : link.particleSpeed)
      .linkDirectionalParticleWidth(link => highlightLinks.has(link) ? 3.8 : 2.0)
      .linkDirectionalParticleColor(link => link.particleColor || link.color || '#38BDF8')
      .linkColor(link => {{
        if (highlightLinks.size > 0) {{
          return highlightLinks.has(link) ? link.color : 'rgba(71, 85, 105, 0.12)';
        }}
        return link.color || '#475569';
      }})
      .linkWidth(link => highlightLinks.has(link) ? 3.4 : (link.width || 1.2))
      .linkDirectionalArrowLength(4.2)
      .linkDirectionalArrowRelPos(1.0)
      .nodeThreeObject(node => {{
        const group = new THREE.Group();
        const baseRadius = node.val || 6;
        
        // 1. 3D 多面体几何体
        const baseGeom = geomCache[node.geometry] || geomCache.sphere;
        const geom = baseGeom.clone();
        geom.scale(baseRadius, baseRadius, baseRadius);

        const mat = new THREE.MeshPhongMaterial({{
          color: new THREE.Color(node.color),
          emissive: new THREE.Color(node.color),
          emissiveIntensity: node.isCritical ? 0.45 : 0.25,
          shininess: 85,
          transparent: true,
          opacity: 0.88,
          depthWrite: true
        }});
        const mesh = new THREE.Mesh(geom, mat);
        group.add(mesh);
        node.__threeMesh = mesh;

        // 2. 关键实体外层动态呼吸光环 (防 Z-fighting 闪烁优化)
        if (node.isCritical) {{
          const ringGeom = new THREE.TorusGeometry(baseRadius * 1.55, 0.38, 8, 32);
          const ringMat = new THREE.MeshBasicMaterial({{
            color: new THREE.Color(node.color),
            transparent: true,
            opacity: 0.70,
            depthWrite: false // 关键：关闭 depthWrite 消除闪烁
          }});
          const ringMesh = new THREE.Mesh(ringGeom, ringMat);
          ringMesh.rotation.x = Math.PI / 3;
          ringMesh.renderOrder = 10;
          group.add(ringMesh);
          node.__threeRing = ringMesh;
        }}

        // 3. 3D SpriteText 药学文字标牌 (防深度撕裂闪烁优化)
        const sprite = new SpriteText(node.label);
        sprite.color = '#F7FAFC';
        sprite.textHeight = Math.max(2.8, Math.min(4.2, 2.5 + (node.degree || 1) * 0.14));
        sprite.backgroundColor = 'rgba(7, 11, 20, 0.88)';
        sprite.borderColor = node.color;
        sprite.borderWidth = 0.65;
        sprite.borderRadius = 4;
        sprite.padding = [1.8, 4.2];
        sprite.fontFace = 'Inter, "Noto Sans SC", "Segoe UI Variable Text", "PingFang SC", "Microsoft YaHei", sans-serif';
        const isLongDiseaseLabel = node.category === 'Disease' && (node.fullLabel || node.label).length > 18;
        sprite.position.y = isLongDiseaseLabel
          ? baseRadius + sprite.textHeight * 1.15
          : -(baseRadius + sprite.textHeight * 0.95);
        
        // 关键抗闪烁设置
        sprite.material.depthWrite = false;
        sprite.material.transparent = true;
        sprite.renderOrder = 100;
        group.add(sprite);
        node.__threeSprite = sprite;

        node.__threeGroup = group;
        return group;
      }})
      .onNodeClick(node => {{
        if (window.matchMedia('(max-width: 900px)').matches) {{
          setSidebarOpen(true);
        }}
        focusNode3D(node.id);
        if (isCascadeMode) {{
          expandCascade3D(node.id);
        }}
      }})
      .onNodeHover(node => {{
        container.style.cursor = node ? 'pointer' : 'default';
        hoverNodeObj = node;
        
        const hoverHud = document.getElementById('hover-hud');
        if (node) {{
          hoverHud.style.display = 'block';
          document.getElementById('hover-hud-title').innerText = node.fullLabel;
          document.getElementById('hover-hud-cat').innerText = `${{node.categoryName}} · ${{node.degree}} 条药理连线`;
        }} else {{
          hoverHud.style.display = 'none';
        }}

        updateVisualHighlights();
      }})
      .onLinkHover(link => {{
        container.style.cursor = link ? 'pointer' : 'default';
        const hoverHud = document.getElementById('hover-hud');
        if (link) {{
          hoverHud.style.display = 'block';
          const sName = link.source.label || link.source.id || link.source;
          const tName = link.target.label || link.target.id || link.target;
          document.getElementById('hover-hud-title').innerText = `${{sName}} ➔ ${{tName}}`;
          document.getElementById('hover-hud-cat').innerText = `[${{link.relName}}] ${{link.description || ''}}`;
        }} else if (!hoverNodeObj) {{
          hoverHud.style.display = 'none';
        }}
      }})
      .onBackgroundClick(() => {{
        // 🌟 点击空白画布背景：立即释放视角锁定并恢复全局自由漫游
        resetViewFocus(true);
      }});

    // 🚀 轻量级属性更新函数（零 GC 重绘，保持 60FPS）
    function updateVisualHighlights() {{
      highlightNodes.clear();
      highlightLinks.clear();

      const hasFocus = activeFocusedNodeId !== null;
      const hasHover = hoverNodeObj !== null;
      const activeId = hoverNodeObj ? hoverNodeObj.id : activeFocusedNodeId;

      if (activeId) {{
        highlightNodes.add(activeId);
        const neighbors = adjMap[activeId] || new Set();
        neighbors.forEach(nId => highlightNodes.add(nId));

        const currentLinks = Graph.graphData().links;
        currentLinks.forEach(l => {{
          const sId = typeof l.source === 'object' ? l.source.id : l.source;
          const tId = typeof l.target === 'object' ? l.target.id : l.target;
          if (sId === activeId || tId === activeId) {{
            highlightLinks.add(l);
          }}
        }});
      }}

      // 直接修改节点 Mesh 材质，不触发全图重建
      const currentNodes = Graph.graphData().nodes;
      currentNodes.forEach(n => {{
        if (!n.__threeMesh) return;
        const isTarget = activeId && n.id === activeId;
        const isNeighbor = activeId && highlightNodes.has(n.id);
        const isDimmed = (hasFocus || hasHover) && !isNeighbor;

        n.__threeMesh.material.opacity = isDimmed ? 0.16 : (isTarget ? 1.0 : 0.88);
        n.__threeMesh.material.emissiveIntensity = isTarget ? 0.95 : (isNeighbor ? 0.60 : (n.isCritical ? 0.45 : 0.25));

        if (n.__threeRing) {{
          n.__threeRing.visible = !isDimmed;
        }}
        if (n.__threeSprite) {{
          n.__threeSprite.visible = !isDimmed;
          n.__threeSprite.material.opacity = isDimmed ? 0.20 : 1.0;
        }}
      }});

      // 仅需通知链接层更新高亮样式
      Graph.linkColor(Graph.linkColor());
    }}

    // 悬浮微型 HUD 鼠标跟踪
    container.addEventListener('mousemove', function(e) {{
      const hoverHud = document.getElementById('hover-hud');
      if (hoverHud.style.display === 'block') {{
        hoverHud.style.left = (e.clientX - container.getBoundingClientRect().left + 15) + 'px';
        hoverHud.style.top = (e.clientY - container.getBoundingClientRect().top + 15) + 'px';
      }}
    }});

    // 双击背景画布复位
    container.addEventListener('dblclick', () => {{
      resetViewFocus(true);
    }});

    // 🚀 3D 动力学力导向引擎参数微调
    Graph.d3Force('charge').strength(-360);
    Graph.d3Force('link').distance(link => 82 + (link.isKey ? 24 : 0));

    // 🛸 自动环绕巡航漫游 (平滑无抖动版)
    let rotateAngle = 0;
    function animationLoop() {{
      if (isAutoRotating) {{
        rotateAngle += Math.PI / 1600;
        const currentPos = Graph.cameraPosition();
        const dist = Math.hypot(currentPos.x, currentPos.z) || 450;
        Graph.cameraPosition(
          {{ x: dist * Math.sin(rotateAngle), y: currentPos.y, z: dist * Math.cos(rotateAngle) }},
          {{ x: 0, y: 0, z: 0 }}
        );
      }}
      requestAnimationFrame(animationLoop);
    }}
    animationLoop();

    document.getElementById('btn-auto-rotate').addEventListener('click', function() {{
      isAutoRotating = !isAutoRotating;
      this.classList.toggle('active', isAutoRotating);
      this.classList.toggle('highlight', isAutoRotating);
      this.setAttribute('aria-pressed', String(isAutoRotating));
      document.getElementById('mode-text').innerText = isAutoRotating ? '巡航旋转已开启，可再次点击停止' : '巡航旋转已停止';
      if (isAutoRotating) {{
        const pos = Graph.cameraPosition();
        rotateAngle = Math.atan2(pos.x, pos.z) || 0;
      }}
    }});

    let currentVisibleNodeIds = new Set();
    let lastDetailTrigger = null;
    let hasCompletedInitialFocus = false;

    function renderAccessibleGraphView() {{
      const graphData = Graph.graphData();
      const nodeList = document.getElementById('accessible-node-list');
      const linkList = document.getElementById('accessible-link-list');
      const nodeHeading = document.getElementById('accessible-node-heading');
      const linkHeading = document.getElementById('accessible-link-heading');

      nodeList.innerHTML = '';
      linkList.innerHTML = '';
      nodeHeading.innerText = `节点 · ${{graphData.nodes.length}}`;
      linkHeading.innerText = `关系证据 · ${{graphData.links.length}}`;

      const nodeById = new Map(graphData.nodes.map(node => [node.id, node]));
      graphData.nodes
        .slice()
        .sort((a, b) => a.fullLabel.localeCompare(b.fullLabel, 'zh-CN'))
        .forEach(node => {{
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'accessible-node-btn';
          button.dataset.nodeId = node.id;
          button.innerText = node.fullLabel;
          button.setAttribute('aria-label', `${{node.fullLabel}}，${{node.categoryName}}，${{node.degree}} 条关系`);
          button.addEventListener('click', () => {{
            focusNode3D(node.id);
            if (isCascadeMode) expandCascade3D(node.id);
          }});
          nodeList.appendChild(button);
        }});

      graphData.links.forEach(link => {{
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;
        const source = nodeById.get(sourceId) || graphRawData.nodes.find(node => node.id === sourceId);
        const target = nodeById.get(targetId) || graphRawData.nodes.find(node => node.id === targetId);
        const item = document.createElement('li');
        const relation = document.createElement('span');
        relation.innerText = `${{source ? source.fullLabel : sourceId}} — ${{link.relName}} → ${{target ? target.fullLabel : targetId}}`;
        item.appendChild(relation);
        if (link.description) {{
          const description = document.createElement('span');
          description.className = 'accessible-link-desc';
          description.innerText = link.description;
          item.appendChild(description);
        }}
        linkList.appendChild(item);
      }});
    }}

    // 🌟 释放视角锁定并恢复自由全景
    function resetViewFocus(animate = true) {{
      const releasedNodeId = activeFocusedNodeId;
      const returnTarget = lastDetailTrigger;
      lastDetailTrigger = null;
      activeFocusedNodeId = null;
      hoverNodeObj = null;
      const drawer = document.getElementById('detail-drawer');
      const drawerWasOpen = drawer.classList.contains('show');
      drawer.classList.remove('show');
      drawer.setAttribute('aria-hidden', 'true');
      document.getElementById('mode-text').innerText = '自由全景漫游 · 选择节点可再次聚焦';
      
      updateVisualHighlights();

      if (animate) {{
        Graph.cameraPosition({{ x: 0, y: 160, z: 560 }}, {{ x: 0, y: 0, z: 0 }}, cameraDuration());
      }}
      if (returnTarget && returnTarget.isConnected && !returnTarget.closest('[inert]')) {{
        returnTarget.focus();
      }} else if (drawerWasOpen) {{
        const stableNodeButton = releasedNodeId
          ? Array.from(document.querySelectorAll('.accessible-node-btn')).find(button => button.dataset.nodeId === releasedNodeId)
          : null;
        if (stableNodeButton && stableNodeButton.offsetParent !== null && !stableNodeButton.closest('[inert]')) {{
          stableNodeButton.focus();
          stableNodeButton.scrollIntoView({{ block: 'nearest' }});
        }} else {{
          document.getElementById('network-wrapper').focus({{ preventScroll: true }});
          document.getElementById('sidebar').scrollTo({{ top: 0, behavior: prefersReducedMotion.matches ? 'auto' : 'smooth' }});
        }}
      }}
    }}

    document.getElementById('drawer-close-btn').addEventListener('click', () => resetViewFocus(true));
    document.getElementById('btn-release-focus').addEventListener('click', () => resetViewFocus(true));
    document.addEventListener('keydown', event => {{
      if (event.key === 'Escape' && document.getElementById('detail-drawer').classList.contains('show')) {{
        resetViewFocus(true);
      }}
    }});

    // 🌟 单点级联扩散呈现（开屏及逐级裂变）
    function loadCascadeSeed3D(seedNodeId, depth = 1) {{
      const visibleIds = new Set([seedNodeId]);
      const neighbors = adjMap[seedNodeId] || new Set();
      neighbors.forEach(id => visibleIds.add(id));

      if (depth >= 2) {{
        neighbors.forEach(nId => {{
          const n2 = adjMap[nId] || new Set();
          n2.forEach(id => {{
            if (visibleIds.size < 24) visibleIds.add(id);
          }});
        }});
      }}

      updateGraphSubView(visibleIds);
      focusNode3D(seedNodeId);
      document.getElementById('mode-text').innerText = '单点级联探索 · 选择节点继续展开';
    }}

    function expandCascade3D(nodeId) {{
      const neighbors = adjMap[nodeId] || new Set();
      let added = false;
      neighbors.forEach(nId => {{
        if (!currentVisibleNodeIds.has(nId)) {{
          currentVisibleNodeIds.add(nId);
          added = true;
        }}
      }});

      if (added) {{
        updateGraphSubView(currentVisibleNodeIds);
      }}
    }}

    function updateGraphSubView(visibleNodeIds) {{
      currentVisibleNodeIds = visibleNodeIds;
      const subNodes = graphRawData.nodes.filter(n => visibleNodeIds.has(n.id));
      const subLinks = graphRawData.links.filter(e => {{
        const u = typeof e.source === 'object' ? e.source.id : e.source;
        const v = typeof e.target === 'object' ? e.target.id : e.target;
        return visibleNodeIds.has(u) && visibleNodeIds.has(v);
      }});

      const cleanNodes = subNodes.map(n => ({{ ...n }}));
      const cleanLinks = subLinks.map(l => ({{ ...l }}));

      Graph.graphData({{ nodes: cleanNodes, links: cleanLinks }});
      renderAccessibleGraphView();
      
      if (currentLayoutMode !== 'force') {{
        applyCustom3DLayout(currentLayoutMode);
      }}
    }}

    // 🎬 电影级 3D 平滑运镜聚焦
    function focusNode3D(nodeId) {{
      const shouldRevealDetails = hasCompletedInitialFocus;
      const activeElement = document.activeElement;
      if (activeElement && activeElement.matches('.accessible-node-btn, .conn-tag, #search-input, .filter-item, .chip')) {{
        lastDetailTrigger = activeElement;
      }}
      activeFocusedNodeId = nodeId;
      const currentNodes = Graph.graphData().nodes;
      const node = currentNodes.find(n => n.id === nodeId) || graphRawData.nodes.find(n => n.id === nodeId);
      if (!node) return;

      const viewportWidth = Math.max(container.clientWidth, 360);
      const distance = Math.min(720, Math.max(340, 340 * (1020 / viewportWidth)));
      const currentPos = Graph.cameraPosition();
      const nx = node.x || 0;
      const ny = node.y || 0;
      const nz = node.z || 0;

      const distVec = {{
        x: currentPos.x - nx,
        y: currentPos.y - ny,
        z: currentPos.z - nz
      }};
      const currentDist = Math.hypot(distVec.x, distVec.y, distVec.z) || 1;
      const targetCamPos = {{
        x: nx + (distVec.x / currentDist) * distance,
        y: ny + (distVec.y / currentDist) * distance * 0.4 + 18,
        z: nz + (distVec.z / currentDist) * distance
      }};

      Graph.cameraPosition(targetCamPos, {{ x: nx, y: ny, z: nz }}, cameraDuration());

      // 展开现代化全景看板
      const drawer = document.getElementById('detail-drawer');
      const drawerTitle = document.getElementById('drawer-title');
      drawer.classList.add('show');
      drawer.setAttribute('aria-hidden', 'false');
      drawerTitle.innerText = node.fullLabel;
      document.getElementById('drawer-desc').innerText = node.description || 'Stahl 精神药理学核心实体。';
      
      const badge = document.getElementById('drawer-badge');
      badge.innerText = node.categoryName;
      const catCfg = categoryConfig[node.category] || {{}};
      badge.style.background = catCfg.badgeBg || catCfg.color || '#38BDF8';
      document.getElementById('drawer-level').innerText = `网络度数: ${{node.degree}} · 节点层级 L${{node.level}}`;

      // 3D 展柜与医学资产预览
      const artImg = document.getElementById('drawer-art');
      const artTag = document.getElementById('drawer-art-tag');
      if (node.customImage) {{
        artImg.src = node.customImage;
        artImg.alt = `${{node.fullLabel}}相关药物或机制图像`;
        artTag.innerText = '高精医学素材 / 结构式';
      }} else {{
        artImg.src = (catCfg && catCfg.icon) ? catCfg.icon : 'assets/63653-tablets-min.png';
        artImg.alt = '';
        artTag.innerText = '分类范畴图解';
      }}

      // 机制传导流条带动态渲染
      const flowRibbon = document.getElementById('flow-ribbon');
      const flowSteps = document.getElementById('flow-steps');
      const relatedLinks = graphRawData.links.filter(e => {{
        const u = typeof e.source === 'object' ? e.source.id : e.source;
        const v = typeof e.target === 'object' ? e.target.id : e.target;
        return u === nodeId || v === nodeId;
      }});
      
      if (relatedLinks.length > 0) {{
        flowRibbon.style.display = 'flex';
        flowSteps.innerHTML = '';
        
        const step1 = document.createElement('span');
        step1.className = 'flow-step';
        step1.innerText = node.label;
        flowSteps.appendChild(step1);

        const sampleLinks = relatedLinks.slice(0, 3);
        sampleLinks.forEach(e => {{
          const arrow = document.createElement('span');
          arrow.className = 'flow-arrow';
          arrow.innerText = '➔';
          flowSteps.appendChild(arrow);

          const stepRel = document.createElement('span');
          stepRel.className = 'flow-step';
          const u = typeof e.source === 'object' ? e.source.id : e.source;
          const v = typeof e.target === 'object' ? e.target.id : e.target;
          const otherId = u === nodeId ? v : u;
          const otherNode = graphRawData.nodes.find(n => n.id === otherId);
          stepRel.innerText = `${{e.relName}} [${{otherNode ? otherNode.label : otherId}}]`;
          flowSteps.appendChild(stepRel);
        }});
      }} else {{
        flowRibbon.style.display = 'none';
      }}

      // 关联靶点卡片列表
      const connsDiv = document.getElementById('drawer-conns');
      connsDiv.innerHTML = '';
      document.getElementById('conns-count').innerText = `${{relatedLinks.length}} 个直接相互作用`;

      relatedLinks.forEach(e => {{
        const u = typeof e.source === 'object' ? e.source.id : e.source;
        const v = typeof e.target === 'object' ? e.target.id : e.target;
        const otherId = u === nodeId ? v : u;
        const otherNode = graphRawData.nodes.find(n => n.id === otherId);
        if (otherNode) {{
          const tag = document.createElement('button');
          tag.type = 'button';
          tag.className = 'conn-tag';
          const relType = e.relType || 'link';
          tag.innerHTML = `
            <span><b class="conn-rel ${{relType}}">${{e.relName}}</b> → ${{otherNode.label}}</span>
            <span style="color:#94A3B8; font-size:0.68rem;">${{e.description || ''}}</span>
          `;
          tag.setAttribute('aria-label', `${{e.relName}}，前往 ${{otherNode.fullLabel}}。${{e.description || ''}}`);
          tag.addEventListener('click', function(ev) {{
            ev.stopPropagation();
            if (!currentVisibleNodeIds.has(otherId)) {{
              currentVisibleNodeIds.add(otherId);
              updateGraphSubView(currentVisibleNodeIds);
            }}
            focusNode3D(otherId);
            if (isCascadeMode) expandCascade3D(otherId);
          }});
          connsDiv.appendChild(tag);
        }}
      }});

      updateVisualHighlights();
      if (shouldRevealDetails) {{
        drawer.scrollIntoView({{ behavior: prefersReducedMotion.matches ? 'auto' : 'smooth', block: 'nearest' }});
        if (lastDetailTrigger && lastDetailTrigger.matches('.accessible-node-btn, .conn-tag')) {{
          drawerTitle.focus({{ preventScroll: true }});
        }}
      }}
      hasCompletedInitialFocus = true;
    }}

    // 🌟 单点级联探索模式按钮
    document.getElementById('btn-cascade-mode').addEventListener('click', function() {{
      isCascadeMode = true;
      setActiveInGroup('.filter-item');
      const initialPreset = document.querySelector('[data-preset="INITIAL_SEED"]');
      setActiveInGroup('.chip', initialPreset);
      setPrimaryViewMode('cascade');
      loadCascadeSeed3D('DRUG_ESKETAMINE', 1);
    }});

    // 🌟 展开全景宏观总网按钮
    document.getElementById('btn-expand-all').addEventListener('click', function() {{
      isCascadeMode = false;
      setActiveInGroup('.filter-item');
      setActiveInGroup('.chip');
      setPrimaryViewMode('all');
      
      const allIds = new Set(graphRawData.nodes.map(n => n.id));
      updateGraphSubView(allIds);

      Graph.d3ReheatSimulation();
      resetViewFocus(true);
      document.getElementById('mode-text').innerText = `宏观全景总网 · ${{graphRawData.nodes.length}} 节点 / ${{graphRawData.links.length}} 关系`;
    }});

    // 🌟 20+ 核心场景预设 (精准节点映射)
    const PRESET_CONFIGS = {{
      'INITIAL_SEED': ['DRUG_ESKETAMINE'],
      'TRD_KETAMINE': ['DRUG_ESKETAMINE', 'REC_NMDA', 'REC_AMPA', 'REC_BDNF_TRKB', 'REC_MTORC1', 'DIS_TRD', 'DIS_MDSI', 'PATH_HIPPOCAMPAL_PLASTICITY'],
      'ADHD_OROS': ['DRUG_METHYLPHENIDATE', 'DRUG_LISDEXAMFETAMINE', 'REC_DAT', 'REC_NET', 'REC_ALPHA2A', 'REC_D1', 'DIS_ADHD', 'PATH_PFC_CIRCUITS', 'CLS_ADHD_STIMULANT'],
      'DORA_INSOMNIA': ['DRUG_LEMBOREXANT', 'DRUG_DARIDOREXANT', 'DRUG_FAZAMOREXANT', 'DRUG_VORNOREXANT', 'REC_OX1R_OX2R', 'PATH_HYPOTHALAMIC_AROUSAL', 'DIS_INSOMNIA'],
      'LUMATEPERONE': ['DRUG_LUMATEPERONE', 'REC_5HT2A', 'REC_D2', 'REC_SERT', 'DIS_SCHIZOPHRENIA_POS', 'DIS_BIPOLAR_DEP', 'CLS_SDA'],
      'TAAR1_SCHIZO': ['DRUG_ULOTARONT', 'REC_TAAR1', 'REC_5HT1A', 'DIS_SCHIZOPHRENIA_POS', 'DIS_SCHIZOPHRENIA_NEG', 'CLS_TAAR1_AGONIST'],
      'PPD_GABA': ['DRUG_ZURANOLONE', 'DRUG_BREXANOLONE', 'REC_GABAA_NEUROSTEROID', 'DIS_PPD', 'DIS_MDD', 'CLS_GABAA_NEUROSTEROID_PAM'],
      'SCN_CIRCADIAN': ['DRUG_AGOMELATINE', 'DRUG_RAMELTEON', 'REC_MT1_MT2', 'REC_5HT2C', 'PATH_CIRCADIAN_SCN', 'DIS_MDD', 'DIS_INSOMNIA'],
      'SNDRI_TRIPLE': ['DRUG_TOLUDESVENLAFAXINE', 'REC_SERT', 'REC_NET', 'REC_DAT', 'DIS_MDD', 'CLS_SNDRI'],
      'DIMDAZENIL': ['DRUG_DIMDAZENIL', 'REC_GABAA_ALPHA1_PARTIAL', 'DIS_INSOMNIA', 'DIS_GAD', 'CLS_GABAA_PARTIAL_PAM'],
      'AD_AMYLOID': ['DRUG_LECANEMAB', 'DRUG_DONANEMAB', 'REC_AMYLOID_BETA', 'DIS_ALZHEIMER', 'CLS_ANTI_AMYLOID_MAB']
    }};

    document.querySelectorAll('.preset-chips .chip').forEach(chip => {{
      chip.addEventListener('click', function() {{
        setActiveInGroup('.preset-chips .chip', this);
        setActiveInGroup('.filter-item');
        isCascadeMode = false;
        setPrimaryViewMode('filtered');

        const presetKey = this.dataset.preset;
        const seedNodeIds = PRESET_CONFIGS[presetKey] || ['DRUG_ESKETAMINE'];

        const subNodeIds = new Set(seedNodeIds);
        seedNodeIds.forEach(seedId => {{
          const neighbors = adjMap[seedId] || new Set();
          neighbors.forEach(nId => subNodeIds.add(nId));
        }});

        updateGraphSubView(subNodeIds);
        document.getElementById('mode-text').innerText = `已激活: ${{this.innerText.trim()}} 专题视图 (${{subNodeIds.size}} 节点)`;
        if (seedNodeIds.length > 0) focusNode3D(seedNodeIds[0]);
      }});
    }});

    // 🔍 显式提交搜索：避免每次击键都触发 3D 运镜
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchStatus = document.getElementById('search-status');

    function setSearchStatus(message = '', isError = false) {{
      searchStatus.innerText = message;
      searchStatus.classList.toggle('show', Boolean(message));
      searchStatus.classList.toggle('error', isError);
    }}

    function findMatchingNode(rawQuery) {{
      const query = rawQuery.trim().toLowerCase();
      if (!query) return null;
      const exactMatch = graphRawData.nodes.find(node =>
        node.label.toLowerCase() === query ||
        node.fullLabel.toLowerCase() === query ||
        node.id.toLowerCase() === query
      );
      return exactMatch || graphRawData.nodes.find(node =>
        node.label.toLowerCase().includes(query) ||
        node.fullLabel.toLowerCase().includes(query) ||
        node.id.toLowerCase().includes(query)
      );
    }}

    searchForm.addEventListener('submit', event => {{
      event.preventDefault();
      const query = searchInput.value.trim();
      if (!query) {{
        setSearchStatus('请输入药物、受体、通路或疾病名称。', true);
        searchInput.focus();
        return;
      }}

      const matchedNode = findMatchingNode(query);
      if (!matchedNode) {{
        setSearchStatus(`未找到“${{query}}”。可尝试中文名、英文名或内部节点 ID。`, true);
        return;
      }}

      if (!currentVisibleNodeIds.has(matchedNode.id)) {{
        currentVisibleNodeIds.add(matchedNode.id);
        updateGraphSubView(currentVisibleNodeIds);
      }}
      setActiveInGroup('.filter-item');
      setActiveInGroup('.chip');
      isCascadeMode = false;
      setPrimaryViewMode('filtered');
      lastDetailTrigger = searchInput;
      focusNode3D(matchedNode.id);
      document.getElementById('mode-text').innerText = `搜索定位 · ${{matchedNode.label}}`;
      setSearchStatus(`已定位：${{matchedNode.fullLabel}} · ${{matchedNode.categoryName}}`);
    }});

    searchInput.addEventListener('input', () => {{
      if (!searchInput.value.trim()) setSearchStatus();
    }});

    // 🌟 3D 空间排布算法引擎
    function applyCustom3DLayout(mode) {{
      currentLayoutMode = mode;
      const currentNodes = Graph.graphData().nodes;
      if (!currentNodes || currentNodes.length === 0) return;

      if (mode === 'force') {{
        currentNodes.forEach(node => {{
          node.fx = undefined;
          node.fy = undefined;
          node.fz = undefined;
        }});
        Graph.d3Force('charge').strength(-360);
        Graph.d3ReheatSimulation();
      }} else if (mode === 'sphere') {{
        const categories = ['Receptor', 'Drug', 'DrugClass', 'Pathway', 'Disease', 'SideEffect'];
        const baseRadii = {{
          'Receptor': 140,
          'Drug': 260,
          'DrugClass': 380,
          'Pathway': 490,
          'Disease': 590,
          'SideEffect': 680
        }};

        const catGroups = {{}};
        categories.forEach(c => catGroups[c] = []);
        currentNodes.forEach(n => {{
          if (catGroups[n.category] !== undefined) {{
            catGroups[n.category].push(n);
          }}
        }});

        categories.forEach(cat => {{
          const group = catGroups[cat] || [];
          const N = group.length;
          if (N === 0) return;
          const R = baseRadii[cat] || 300;
          const phi = Math.PI * (Math.sqrt(5) - 1);

          group.forEach((node, i) => {{
            const y = 1 - (i / (N - 1 || 1)) * 2;
            const radiusAtY = Math.sqrt(1 - y * y);
            const theta = phi * i;

            node.fx = Math.cos(theta) * radiusAtY * R;
            node.fy = y * R;
            node.fz = Math.sin(theta) * radiusAtY * R;
          }});
        }});
        Graph.d3ReheatSimulation();
      }} else if (mode === 'cylinder') {{
        const catZLevels = {{
          'Receptor': -240,
          'Drug': -80,
          'DrugClass': 40,
          'Pathway': 160,
          'Disease': 280,
          'SideEffect': 380
        }};
        const catRadius = {{
          'Receptor': 180,
          'Drug': 220,
          'DrugClass': 260,
          'Pathway': 240,
          'Disease': 210,
          'SideEffect': 250
        }};

        const catGroups = {{}};
        Object.keys(catZLevels).forEach(c => catGroups[c] = []);
        currentNodes.forEach(n => {{
          if (catGroups[n.category] !== undefined) {{
            catGroups[n.category].push(n);
          }}
        }});

        Object.keys(catZLevels).forEach(cat => {{
          const group = catGroups[cat] || [];
          const N = group.length;
          if (N === 0) return;
          const Z = catZLevels[cat];
          const R = catRadius[cat];

          group.forEach((node, i) => {{
            const angle = (i / N) * 2 * Math.PI;
            node.fx = R * Math.cos(angle);
            node.fy = R * Math.sin(angle);
            node.fz = Z;
          }});
        }});
        Graph.d3ReheatSimulation();
      }}
    }}

    document.getElementById('btn-layout-force').addEventListener('click', function() {{
      setActiveInGroup('.layout-btn', this);
      applyCustom3DLayout('force');
      document.getElementById('mode-text').innerText = '空间布局：自由星群';
    }});

    document.getElementById('btn-layout-cluster').addEventListener('click', function() {{
      setActiveInGroup('.layout-btn', this);
      applyCustom3DLayout('sphere');
      document.getElementById('mode-text').innerText = '空间布局：同心分层';
    }});

    document.getElementById('btn-layout-hier').addEventListener('click', function() {{
      setActiveInGroup('.layout-btn', this);
      applyCustom3DLayout('cylinder');
      document.getElementById('mode-text').innerText = '空间布局：机制柱阵';
    }});

    // 💫 3D 空间舒展按钮
    document.getElementById('btn-relax-physics').addEventListener('click', function() {{
      if (currentLayoutMode !== 'force') {{
        document.getElementById('btn-layout-force').click();
      }}
      Graph.d3Force('charge').strength(-550);
      Graph.d3ReheatSimulation();
      setTimeout(() => {{
        Graph.d3Force('charge').strength(-360);
      }}, 1200);
    }});

    document.getElementById('btn-zoom-fit').addEventListener('click', () => {{
      resetViewFocus(true);
    }});

    document.getElementById('reset-filter-btn').addEventListener('click', () => {{
      setActiveInGroup('.filter-item');
      document.getElementById('btn-cascade-mode').click();
    }});

    const mobilePanelToggle = document.getElementById('mobile-panel-toggle');
    const mobileLayout = window.matchMedia('(max-width: 900px)');

    function setSidebarOpen(isOpen) {{
      const sidebar = document.getElementById('sidebar');
      const shouldHideSidebar = mobileLayout.matches && !isOpen;
      if (shouldHideSidebar && sidebar.contains(document.activeElement)) {{
        mobilePanelToggle.focus({{ preventScroll: true }});
      }}
      document.body.classList.toggle('sidebar-collapsed', !isOpen);
      mobilePanelToggle.setAttribute('aria-expanded', String(isOpen));
      mobilePanelToggle.innerText = isOpen ? '收起探索面板' : '打开探索面板';
      sidebar.toggleAttribute('inert', shouldHideSidebar);
      if (shouldHideSidebar) {{
        sidebar.setAttribute('aria-hidden', 'true');
      }} else {{
        sidebar.removeAttribute('aria-hidden');
      }}
      requestAnimationFrame(() => {{
        Graph.width(container.clientWidth);
        Graph.height(container.clientHeight);
      }});
    }}

    mobilePanelToggle.addEventListener('click', () => {{
      const isOpen = mobilePanelToggle.getAttribute('aria-expanded') === 'true';
      const willOpen = !isOpen;
      setSidebarOpen(willOpen);
      if (willOpen) {{
        requestAnimationFrame(() => document.getElementById('search-input').focus({{ preventScroll: true }}));
      }}
    }});

    function syncResponsiveLayout() {{
      setSidebarOpen(!mobileLayout.matches);
    }}
    mobileLayout.addEventListener('change', syncResponsiveLayout);
    syncResponsiveLayout();

    prefersReducedMotion.addEventListener('change', () => {{
      Graph.linkDirectionalParticles(link => prefersReducedMotion.matches ? 0 : link.particles);
      Graph.linkDirectionalParticleSpeed(link => prefersReducedMotion.matches ? 0 : link.particleSpeed);
      if (prefersReducedMotion.matches && isAutoRotating) {{
        document.getElementById('btn-auto-rotate').click();
      }}
    }});

    // 🚀 开屏默认：以艾司氯胺酮 Spravato® 为种子单点级联扩散
    setPrimaryViewMode('cascade');
    loadCascadeSeed3D('DRUG_ESKETAMINE', 1);
  </script>
</body>
</html>
'''
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding="utf-8")
        return output_path
