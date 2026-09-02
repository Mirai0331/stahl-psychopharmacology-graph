# -*- coding: utf-8 -*-
"""WebGL/Three.js 3D 立体化全景脑科学知识图谱生成器：
3D 立体多面体几何实体、3D 能量粒子流飞线 (Link Particle Streams)、
三维空间同心球层/机制晶体柱/柔性星云排布引擎、电影级 3D 飞掠聚焦与自转巡航。
"""
import json
from pathlib import Path
from stahl_document_ai.processors.graph_builder import PsychopharmacologyKnowledgeGraph


class InteractiveGraphGenerator:
    """高精 3D 精神药理学知识图谱可视化生成器"""

    CATEGORY_CONFIG = {
        "Drug": {
            "name": "精神药物",
            "color": "#38BDF8",       # 亮青蓝
            "borderColor": "#0284C7",
            "glow": "rgba(56, 189, 248, 0.85)",
            "geometry": "sphere",
            "level": 2,
            "icon": "assets/63653-tablets-min.png",
            "badgeBg": "linear-gradient(135deg, #0284C7, #0369A1)"
        },
        "DrugClass": {
            "name": "药物大类",
            "color": "#818CF8",       # 靛蓝
            "borderColor": "#4F46E5",
            "glow": "rgba(129, 140, 248, 0.85)",
            "geometry": "octahedron",
            "level": 1,
            "icon": "assets/Field_Inventory_Menu_02.png",
            "badgeBg": "linear-gradient(135deg, #4F46E5, #3730A3)"
        },
        "Receptor": {
            "name": "受体与信号靶点",
            "color": "#10B981",       # 翡翠荧绿
            "borderColor": "#059669",
            "glow": "rgba(16, 185, 129, 0.85)",
            "geometry": "icosahedron",
            "level": 3,
            "icon": "assets/mission.png",
            "badgeBg": "linear-gradient(135deg, #059669, #047857)"
        },
        "Pathway": {
            "name": "神经通路与可塑环路",
            "color": "#C084FC",       # 梦幻极光紫
            "borderColor": "#9333EA",
            "glow": "rgba(192, 132, 252, 0.85)",
            "geometry": "dodecahedron",
            "level": 4,
            "icon": "assets/complete.png",
            "badgeBg": "linear-gradient(135deg, #9333EA, #7E22CE)"
        },
        "Disease": {
            "name": "疾病与危重/难治表型",
            "color": "#F472B6",       # 玫粉
            "borderColor": "#DB2777",
            "glow": "rgba(244, 114, 182, 0.85)",
            "geometry": "sphere",
            "level": 5,
            "icon": "assets/NOTE.png",
            "badgeBg": "linear-gradient(135deg, #DB2777, #BE185D)"
        },
        "SideEffect": {
            "name": "不良反应",
            "color": "#FB7185",       # 珊瑚红
            "borderColor": "#E11D48",
            "glow": "rgba(251, 113, 133, 0.85)",
            "geometry": "cone",
            "level": 5,
            "icon": "assets/Goods_Icon_Gem_490_Preset_2.png",
            "badgeBg": "linear-gradient(135deg, #E11D48, #9F1239)"
        },
    }

    # 节点专属高精素材映射表（结构式、真实药片图、节律图标等）
    NODE_IMAGE_MAP = {
        "DRUG_ESKETAMINE": "assets/drug_sukailang.png",
        "DRUG_LISDEXAMFETAMINE": "assets/Dexmethylphenidate_structure.svg",
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
            node_val = min(14.0, max(4.5, (6.8 if is_critical else 4.2) + deg * 0.32))
            clean_label = n.label.split("(")[0].strip() if "(" in n.label else n.label
            custom_img = cls.NODE_IMAGE_MAP.get(n.id, "")

            nodes_3d.append({
                "id": n.id,
                "label": clean_label,
                "fullLabel": n.label,
                "category": n.category,
                "categoryName": cfg["name"],
                "description": n.description,
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
                "color": rel_cfg["color"],
                "particleColor": rel_cfg.get("particleColor", rel_cfg["color"]),
                "curvature": 0.20 if is_key_edge else 0.14,
                "particles": 4 if is_key_edge else 2,
                "particleSpeed": 0.008 if is_key_edge else 0.005,
                "width": max(1.2, min(3.8, e.weight * (1.8 if is_key_edge else 1.2))),
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
      --bg-dark: #050811;
      --bg-card: rgba(10, 16, 28, 0.92);
      --bg-card-hover: rgba(16, 24, 42, 0.96);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-glow: rgba(56, 189, 248, 0.40);
      --border-glass: rgba(255, 255, 255, 0.14);
      --text-main: #FFFFFF;
      --text-sub: #94A3B8;
      --text-muted: #64748B;
      --accent-blue: #38BDF8;
      --accent-purple: #C084FC;
      --accent-green: #10B981;
      --accent-amber: #F59E0B;
      --accent-pink: #F472B6;
      --accent-cyan: #06B6D4;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }}
    body {{ background: var(--bg-dark); color: var(--text-main); height: 100vh; display: flex; overflow: hidden; }}

    /* 🌌 3D WebGL 视口画布容器 */
    #network-wrapper {{
      flex: 1;
      height: 100%;
      position: relative;
      background: radial-gradient(circle at 50% 50%, rgba(14, 28, 54, 0.75) 0%, rgba(5, 8, 17, 0.98) 90%);
      overflow: hidden;
    }}
    #3d-graph-container {{
      width: 100%;
      height: 100%;
    }}

    /* 🛡️ 左侧控制侧边栏 (Cyber-Medical Glass) */
    #sidebar {{
      width: 480px;
      background: var(--bg-card);
      backdrop-filter: blur(28px);
      -webkit-backdrop-filter: blur(28px);
      border-right: 1px solid var(--border-glass);
      display: flex;
      flex-direction: column;
      padding: 22px;
      z-index: 20;
      box-shadow: 18px 0 50px rgba(0, 0, 0, 0.85);
      overflow-y: auto;
      scrollbar-width: thin;
      scrollbar-color: rgba(56,189,248,0.3) transparent;
    }}
    #sidebar::-webkit-scrollbar {{ width: 5px; }}
    #sidebar::-webkit-scrollbar-thumb {{ background: rgba(56, 189, 248, 0.3); border-radius: 4px; }}

    .header-box {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 8px;
    }}
    .header-logo {{
      width: 46px;
      height: 46px;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(192, 132, 252, 0.25));
      border: 1px solid var(--border-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
      overflow: hidden;
    }}
    .header-logo img {{ width: 34px; height: 34px; object-fit: contain; }}

    .header-title {{
      font-size: 1.30rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 50%, #C084FC 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .header-sub {{ font-size: 0.78rem; color: var(--text-sub); margin-bottom: 14px; line-height: 1.5; }}

    .mode-banner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(192, 132, 252, 0.08));
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 12px;
      padding: 9px 14px;
      margin-bottom: 16px;
      font-size: 0.78rem;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }}
    .mode-pill {{
      background: linear-gradient(135deg, #0284C7, #2563EB);
      color: #fff;
      padding: 4px 10px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.70rem;
      cursor: pointer;
      transition: all 0.2s;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .mode-pill:hover {{ background: #0369A1; transform: scale(1.05); }}

    .scenario-section {{ margin-bottom: 16px; }}
    .section-title {{ font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94A3B8; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }}
    .preset-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .chip {{
      padding: 6px 11px;
      border-radius: 20px;
      font-size: 0.73rem;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: #CBD5E1;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .chip img {{ width: 14px; height: 14px; object-fit: contain; border-radius: 3px; }}
    .chip:hover {{ background: rgba(56, 189, 248, 0.16); border-color: var(--accent-blue); color: #fff; transform: translateY(-1.5px); box-shadow: 0 4px 12px rgba(56,189,248,0.25); }}
    .chip.active {{ background: linear-gradient(135deg, #0284C7, #2563EB); border-color: #38BDF8; color: #fff; font-weight: 700; box-shadow: 0 0 16px rgba(56, 189, 248, 0.5); }}

    .search-wrapper {{ position: relative; margin-bottom: 16px; }}
    .search-input {{
      width: 100%;
      padding: 11px 14px 11px 40px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-glass);
      border-radius: 12px;
      color: #fff;
      font-size: 0.88rem;
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{ border-color: var(--accent-blue); box-shadow: 0 0 16px rgba(56, 189, 248, 0.4); background: rgba(15, 23, 42, 0.95); }}
    .search-icon-img {{ position: absolute; left: 14px; top: 12px; width: 17px; height: 17px; opacity: 0.75; }}

    .layout-switcher {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .layout-btn {{
      padding: 9px 6px;
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      color: #CBD5E1;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
    }}
    .layout-btn:hover {{ background: rgba(255, 255, 255, 0.08); border-color: rgba(56, 189, 248, 0.3); }}
    .layout-btn.active {{ background: rgba(56, 189, 248, 0.22); border-color: var(--accent-blue); color: var(--accent-blue); box-shadow: 0 0 14px rgba(56,189,248,0.3); font-weight: 700; }}

    .filter-list {{ display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }}
    .filter-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      background: rgba(15, 23, 42, 0.50);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      cursor: pointer;
      font-size: 0.80rem;
      transition: all 0.18s;
    }}
    .filter-item:hover {{ background: rgba(255, 255, 255, 0.08); border-color: rgba(56, 189, 248, 0.4); transform: translateX(2px); }}
    .filter-item.active {{ background: rgba(56, 189, 248, 0.22); border-color: var(--accent-blue); font-weight: 700; box-shadow: 0 0 12px rgba(56,189,248,0.25); }}
    .filter-left {{ display: flex; align-items: center; gap: 10px; }}
    .filter-icon {{ width: 16px; height: 16px; object-fit: contain; }}
    .filter-dot {{ width: 9px; height: 9px; border-radius: 50%; }}
    .filter-count {{ font-size: 0.72rem; color: var(--text-sub); background: rgba(255,255,255,0.08); padding: 2px 7px; border-radius: 12px; }}

    /* 💎 临床药理多维详情看板 (Clinical Holographic Dashboard) */
    #detail-drawer {{
      margin-top: 14px;
      background: linear-gradient(145deg, rgba(14, 22, 38, 0.96), rgba(8, 12, 22, 0.98));
      border: 1px solid var(--border-glow);
      border-radius: 16px;
      padding: 18px;
      display: none;
      box-shadow: 0 12px 40px rgba(0,0,0,0.75), inset 0 1px 0 rgba(255,255,255,0.1);
      animation: slideInUp 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }}
    #detail-drawer.show {{ display: block; }}
    @keyframes slideInUp {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    .drawer-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; gap: 10px; }}
    .drawer-badge {{ display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 8px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}
    
    /* 🖼️ 3D 高精展柜窗口 */
    .drawer-lightbox {{
      width: 100%;
      height: 120px;
      border-radius: 12px;
      background: radial-gradient(circle at 50% 50%, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 14px;
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
    .drawer-lightbox:hover img {{ transform: scale(1.08); }}
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

    .drawer-title {{ font-size: 1.15rem; font-weight: 800; color: #fff; margin-bottom: 10px; line-height: 1.38; letter-spacing: -0.01em; }}
    .drawer-desc-card {{
      font-size: 0.82rem;
      color: #CBD5E1;
      line-height: 1.65;
      margin-bottom: 14px;
      background: rgba(255, 255, 255, 0.035);
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.06);
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

    .drawer-conns-title {{ font-size: 0.76rem; font-weight: 700; color: var(--text-sub); text-transform: uppercase; margin-bottom: 10px; display: flex; justify-content: space-between; }}
    .drawer-conns-list {{ display: flex; flex-direction: column; gap: 6px; max-height: 180px; overflow-y: auto; font-size: 0.78rem; }}
    .conn-tag {{
      padding: 7px 10px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: all 0.18s;
      border: 1px solid transparent;
    }}
    .conn-tag:hover {{ background: rgba(56, 189, 248, 0.18); border-color: var(--accent-blue); transform: translateX(3px); box-shadow: 0 2px 10px rgba(56,189,248,0.25); }}
    .conn-rel {{ font-weight: 700; }}
    .conn-rel.positive {{ color: #34D399; }}
    .conn-rel.negative {{ color: #F87171; }}
    .conn-rel.modulate {{ color: #C084FC; }}
    .conn-rel.treat {{ color: #38BDF8; }}

    /* 🛰️ 悬浮工具栏 (Floating Control Capsule) */
    .top-floating-bar {{
      position: absolute;
      top: 22px;
      right: 22px;
      display: flex;
      gap: 10px;
      z-index: 10;
    }}
    .tool-btn {{
      background: var(--bg-card);
      backdrop-filter: blur(18px);
      border: 1px solid var(--border-glass);
      color: #E2E8F0;
      padding: 9px 15px;
      border-radius: 12px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 7px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.5);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .tool-btn img {{ width: 15px; height: 15px; object-fit: contain; }}
    .tool-btn:hover {{ background: rgba(56, 189, 248, 0.25); border-color: var(--accent-blue); color: #fff; transform: translateY(-1.5px); box-shadow: 0 8px 25px rgba(56,189,248,0.3); }}
    .tool-btn.highlight {{ background: linear-gradient(135deg, #0284C7, #2563EB); border-color: #38BDF8; color: #fff; box-shadow: 0 0 16px rgba(56,189,248,0.45); }}
    .tool-btn.active {{ background: rgba(56, 189, 248, 0.25); border-color: var(--accent-blue); color: var(--accent-blue); }}

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
      bottom: 18px;
      right: 22px;
      background: rgba(10, 16, 28, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 0.72rem;
      color: #94A3B8;
      z-index: 10;
      pointer-events: none;
      display: flex;
      gap: 12px;
    }}
    .controls-hint span {{ display: flex; align-items: center; gap: 4px; }}
    .controls-hint kbd {{ background: rgba(255,255,255,0.1); padding: 1px 5px; border-radius: 4px; color: #E2E8F0; font-size: 0.68rem; }}
  </style>
</head>
<body>

  <!-- 左侧控制面板 -->
  <div id="sidebar">
    <div class="header-box">
      <div class="header-logo">
        <img src="assets/drug_sukailang.png" alt="Stahl Graph Logo" />
      </div>
      <div>
        <h1 class="header-title">Stahl 精神药理学精要</h1>
        <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">第5版 · 3D 全景立体脑科学知识图谱</div>
      </div>
    </div>
    <div class="header-sub">
      覆盖全书 14 大核心章节 · 187 个受体/药物/回路实体 · 384 条机制证据链 · WebGL 3D 动力学粒子飞线与高精图解看板
    </div>

    <div class="mode-banner">
      <span id="mode-text">单点级联扩散探索 (点击节点裂变展开)</span>
      <span class="mode-pill" id="reset-filter-btn">重置开屏</span>
    </div>

    <div class="search-wrapper">
      <img src="assets/NOTE.png" class="search-icon-img" alt="" />
      <input type="text" id="search-input" class="search-input" placeholder="输入药名/受体 (如: 艾司氯胺酮, 卢美哌隆, TAAR1, 专注达)..." />
    </div>

    <!-- 20+ 核心专病场景矩阵 -->
    <div class="scenario-section">
      <div class="section-title">
        <span>前沿机制与专病透视预设</span>
        <span style="font-size:0.68rem; color:#38BDF8;">20+ 临床场景</span>
      </div>
      <div class="preset-chips">
        <div class="chip active" data-preset="INITIAL_SEED">
          <img src="assets/drug_sukailang.png" alt="" />
          <span>速开朗® TRD/自杀干预 (开屏)</span>
        </div>
        <div class="chip" data-preset="TRD_KETAMINE">
          <img src="assets/mech_nmda_antag.png" alt="" />
          <span>NMDA 阻断与突触可塑性</span>
        </div>
        <div class="chip" data-preset="ADHD_OROS">
          <img src="assets/drug_concerta_18mg.png" alt="" />
          <span>专注达® OROS 控释与前额叶</span>
        </div>
        <div class="chip" data-preset="DORA_INSOMNIA">
          <img src="assets/icon_night.png" alt="" />
          <span>DORA 双食欲素拮抗 (达卫可®)</span>
        </div>
        <div class="chip" data-preset="LUMATEPERONE">
          <img src="assets/pharma_capsule.png" alt="" />
          <span>卢美哌隆 (Caplyta) 5-HT2A/D2/SERT</span>
        </div>
        <div class="chip" data-preset="TAAR1_SCHIZO">
          <img src="assets/complete.png" alt="" />
          <span>TAAR1/5-HT1A 激动剂 (Ulotaront)</span>
        </div>
        <div class="chip" data-preset="PPD_GABA">
          <img src="assets/pharma_capsule.png" alt="" />
          <span>产后抑郁 GABA PAM (祖拉诺酮)</span>
        </div>
        <div class="chip" data-preset="SCN_CIRCADIAN">
          <img src="assets/icon_morning.png" alt="" />
          <span>昼夜节律 MT1/MT2/5-HT2C</span>
        </div>
        <div class="chip" data-preset="SNDRI_TRIPLE">
          <img src="assets/63653-tablets-min.png" alt="" />
          <span>SNDRI 三重再摄取 (若舒达®)</span>
        </div>
        <div class="chip" data-preset="DIMDAZENIL">
          <img src="assets/63653-tablets-min.png" alt="" />
          <span>地达西尼 (京诺宁®) PAM</span>
        </div>
        <div class="chip" data-preset="AD_AMYLOID">
          <img src="assets/NOTE.png" alt="" />
          <span>阿尔茨海默病 Aβ 单抗 (仑卡奈)</span>
        </div>
      </div>
    </div>

    <!-- 3D 空间排布引擎切换 -->
    <div class="scenario-section">
      <div class="section-title">
        <span>3D 空间排布引擎</span>
        <span style="font-size:0.68rem; color:#C084FC;">三维空间几何</span>
      </div>
      <div class="layout-switcher">
        <div class="layout-btn active" id="btn-layout-force">💫 宇宙星云</div>
        <div class="layout-btn" id="btn-layout-cluster">🎯 同心球层</div>
        <div class="layout-btn" id="btn-layout-hier">🌲 机制晶体柱</div>
      </div>
    </div>

    <!-- 实体类别过滤 -->
    <div class="scenario-section">
      <div class="section-title">
        <span>证据闭环实体子图</span>
        <span style="font-size:0.68rem; color:#94A3B8;">点击以关系连接</span>
      </div>
      <div class="filter-list" id="filter-container"></div>
    </div>

    <!-- 临床药理多维看板 (详情抽屉) -->
    <div id="detail-drawer">
      <div class="drawer-header">
        <span class="drawer-badge" id="drawer-badge">类别</span>
        <span id="drawer-level" style="font-size:0.68rem; color:#94A3B8; font-weight:600;">脑区级联</span>
      </div>
      
      <!-- 3D 晶莹展柜窗口 -->
      <div class="drawer-lightbox" id="drawer-lightbox">
        <img id="drawer-art" src="assets/drug_sukailang.png" alt="" />
        <span class="lightbox-tag" id="drawer-art-tag">3D 药学图解</span>
      </div>

      <div class="drawer-title" id="drawer-title">实体详情</div>
      <div class="drawer-desc-card" id="drawer-desc">...</div>

      <!-- 机制传导流条带 -->
      <div class="flow-ribbon" id="flow-ribbon" style="display:none;">
        <div class="flow-ribbon-title">⚡ 脑科学药理机制传导流</div>
        <div class="flow-steps" id="flow-steps"></div>
      </div>

      <div class="drawer-conns-title">
        <span>🔗 关联受体靶点与神经回路 (点击 3D 飞掠跳转)</span>
        <span style="font-size:0.68rem; color:#38BDF8;" id="conns-count">0 关联</span>
      </div>
      <div class="drawer-conns-list" id="drawer-conns"></div>
    </div>
  </div>

  <!-- 3D 图谱画布容器 -->
  <div id="network-wrapper">
    <div id="3d-graph-container"></div>
    <div id="network-container" style="display:none;"></div>
    
    <!-- 悬浮微型 HUD 提示卡 -->
    <div id="hover-hud">
      <div id="hover-hud-title">实体名称</div>
      <div id="hover-hud-cat">类别 · 0 关联</div>
    </div>

    <!-- 顶部操作胶囊 -->
    <div class="top-floating-bar">
      <button class="tool-btn highlight" id="btn-cascade-mode">
        <img src="assets/mission.png" alt="" />
        单点级联探索
      </button>
      <button class="tool-btn" id="btn-expand-all">
        <img src="assets/Field_Inventory_Menu_02.png" alt="" />
        全景宏观总网
      </button>
      <button class="tool-btn" id="btn-auto-rotate">
        <span>🚀</span>
        3D 巡航自转
      </button>
      <button class="tool-btn" id="btn-relax-physics">
        <img src="assets/complete.png" alt="" />
        💫 3D 空间舒展
      </button>
      <button class="tool-btn" id="btn-zoom-fit">
        <img src="assets/NOTE.png" alt="" />
        全景视点
      </button>
    </div>

    <!-- 3D 漫游操作提示 -->
    <div class="controls-hint">
      <span><kbd>左键拖拽</kbd> 3D 自由旋转</span>
      <span><kbd>右键拖拽</kbd> 空间平移</span>
      <span><kbd>滚轮</kbd> 距离推拉</span>
      <span><kbd>左键单击</kbd> 电影级运镜聚焦</span>
    </div>
  </div>

  <script>
    const graphRawData = {graph_data_json};
    const categoryConfig = {json.dumps(cls.CATEGORY_CONFIG, ensure_ascii=False)};
    
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

    // 实体类别侧边栏渲染
    const filterContainer = document.getElementById('filter-container');
    Object.keys(categoryConfig).forEach(cat => {{
      const cfg = categoryConfig[cat];
      const count = catCounts[cat] || 0;
      const item = document.createElement('div');
      item.className = 'filter-item';
      item.dataset.category = cat;
      item.innerHTML = `
        <div class="filter-left">
          <img src="${{cfg.icon}}" class="filter-icon" alt="" />
          <div class="filter-dot" style="background: ${{cfg.color}}; box-shadow: 0 0 10px ${{cfg.color}};"></div>
          <span>${{cfg.name}} (${{cat}})</span>
        </div>
        <span class="filter-count">${{count}}</span>
      `;
      
      item.addEventListener('click', function() {{
        document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
        isCascadeMode = false;

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

    const Graph = ForceGraph3D()(container)
      .backgroundColor('#050811')
      .showNavInfo(false)
      .nodeRelSize(5.5)
      .nodeResolution(16)
      .linkCurvature('curvature')
      .linkCurveRotation(0.25)
      .linkDirectionalParticles('particles')
      .linkDirectionalParticleSpeed('particleSpeed')
      .linkDirectionalParticleWidth(link => highlightLinks.has(link) ? 4.0 : 2.4)
      .linkDirectionalParticleColor(link => link.particleColor || link.color || '#38BDF8')
      .linkColor(link => {{
        if (highlightLinks.size > 0) {{
          return highlightLinks.has(link) ? link.color : 'rgba(71, 85, 105, 0.12)';
        }}
        return link.color || '#475569';
      }})
      .linkWidth(link => highlightLinks.has(link) ? 3.6 : (link.width || 1.4))
      .linkDirectionalArrowLength(4.5)
      .linkDirectionalArrowRelPos(1.0)
      .nodeThreeObject(node => {{
        const group = new THREE.Group();
        const isHovered = hoverNodeObj && hoverNodeObj.id === node.id;
        const isDimmed = highlightNodes.size > 0 && !highlightNodes.has(node.id);
        
        // 1. 3D 立体多面体几何体构建
        const baseRadius = node.val || 6;
        let geom;
        const geomType = node.geometry || 'sphere';
        if (geomType === 'octahedron') {{
          geom = new THREE.OctahedronGeometry(baseRadius * 1.05);
        }} else if (geomType === 'icosahedron') {{
          geom = new THREE.IcosahedronGeometry(baseRadius * 0.95);
        }} else if (geomType === 'dodecahedron') {{
          geom = new THREE.DodecahedronGeometry(baseRadius * 1.05);
        }} else if (geomType === 'cone') {{
          geom = new THREE.ConeGeometry(baseRadius * 0.85, baseRadius * 1.5, 6);
        }} else {{
          geom = new THREE.SphereGeometry(baseRadius, 16, 16);
        }}

        const mat = new THREE.MeshPhongMaterial({{
          color: new THREE.Color(node.color),
          emissive: new THREE.Color(node.color),
          emissiveIntensity: isHovered ? 0.85 : (node.isCritical ? 0.45 : 0.25),
          shininess: 90,
          transparent: true,
          opacity: isDimmed ? 0.15 : (isHovered ? 1.0 : 0.90)
        }});
        const mesh = new THREE.Mesh(geom, mat);
        group.add(mesh);

        // 2. 关键实体外层动态呼吸光环 (Pulse Torus Halo)
        if (node.isCritical && !isDimmed) {{
          const ringGeom = new THREE.TorusGeometry(baseRadius * 1.5, 0.4, 8, 32);
          const ringMat = new THREE.MeshBasicMaterial({{
            color: new THREE.Color(node.color),
            transparent: true,
            opacity: 0.75
          }});
          const ringMesh = new THREE.Mesh(ringGeom, ringMat);
          ringMesh.rotation.x = Math.PI / 3;
          group.add(ringMesh);
        }}

        // 3. 3D SpriteText 药学文字标牌
        if (!isDimmed) {{
          const sprite = new SpriteText(node.label);
          sprite.color = '#FFFFFF';
          sprite.textHeight = Math.max(3.8, Math.min(6.5, 3.2 + (node.degree || 1) * 0.24));
          sprite.backgroundColor = 'rgba(5, 8, 17, 0.82)';
          sprite.borderColor = node.color;
          sprite.borderWidth = 0.8;
          sprite.borderRadius = 4;
          sprite.padding = [2, 5];
          sprite.fontFace = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif';
          sprite.position.y = -(baseRadius + sprite.textHeight * 0.95);
          group.add(sprite);
        }}

        return group;
      }})
      .onNodeClick(node => {{
        focusNode3D(node.id);
        if (isCascadeMode) {{
          expandCascade3D(node.id);
        }}
      }})
      .onNodeHover(node => {{
        container.style.cursor = node ? 'pointer' : 'default';
        hoverNodeObj = node;
        highlightNodes.clear();
        highlightLinks.clear();

        const hoverHud = document.getElementById('hover-hud');
        if (node) {{
          hoverHud.style.display = 'block';
          document.getElementById('hover-hud-title').innerText = node.fullLabel;
          document.getElementById('hover-hud-cat').innerText = `${{node.categoryName}} · ${{node.degree}} 条药理连线`;

          highlightNodes.add(node.id);
          const neighbors = adjMap[node.id] || new Set();
          neighbors.forEach(nId => highlightNodes.add(nId));

          const currentLinks = Graph.graphData().links;
          currentLinks.forEach(l => {{
            const sId = typeof l.source === 'object' ? l.source.id : l.source;
            const tId = typeof l.target === 'object' ? l.target.id : l.target;
            if (sId === node.id || tId === node.id) {{
              highlightLinks.add(l);
            }}
          }});
        }} else {{
          hoverHud.style.display = 'none';
        }}

        // 刷新 3D 对象材质透明度与发光状态
        Graph.nodeThreeObject(Graph.nodeThreeObject());
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
      }});

    // 悬浮微型 HUD 鼠标跟踪
    container.addEventListener('mousemove', function(e) {{
      const hoverHud = document.getElementById('hover-hud');
      if (hoverHud.style.display === 'block') {{
        hoverHud.style.left = (e.clientX - container.getBoundingClientRect().left + 15) + 'px';
        hoverHud.style.top = (e.clientY - container.getBoundingClientRect().top + 15) + 'px';
      }}
    }});

    // 🚀 3D 动力学力导向引擎参数微调
    Graph.d3Force('charge').strength(-320);
    Graph.d3Force('link').distance(link => 65 + (link.isKey ? 20 : 0));

    // 🛸 自动环绕巡航漫游 (Auto-Rotate Orbit Mode)
    let rotateAngle = 0;
    function animationLoop() {{
      if (isAutoRotating) {{
        rotateAngle += Math.PI / 1200;
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
      if (isAutoRotating) {{
        const pos = Graph.cameraPosition();
        rotateAngle = Math.atan2(pos.x, pos.z) || 0;
      }}
    }});

    let currentVisibleNodeIds = new Set();
    let isCascadeMode = true;
    let activeFocusedNodeId = null;

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
      document.getElementById('mode-text').innerText = '单点级联扩散探索 (点击节点裂变展开)';
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

      // 深度拷贝以避免 3d-force-graph 内部对象绑定冲突
      const cleanNodes = subNodes.map(n => ({{ ...n }}));
      const cleanLinks = subLinks.map(l => ({{ ...l }}));

      Graph.graphData({{ nodes: cleanNodes, links: cleanLinks }});
      
      if (currentLayoutMode !== 'force') {{
        applyCustom3DLayout(currentLayoutMode);
      }}
    }}

    // 🎬 电影级 3D 平滑运镜聚焦
    function focusNode3D(nodeId) {{
      activeFocusedNodeId = nodeId;
      const currentNodes = Graph.graphData().nodes;
      const node = currentNodes.find(n => n.id === nodeId) || graphRawData.nodes.find(n => n.id === nodeId);
      if (!node) return;

      // 3D 摄像机飞掠聚焦 (Fly-To)
      const distance = 140;
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
        y: ny + (distVec.y / currentDist) * distance * 0.4 + 20,
        z: nz + (distVec.z / currentDist) * distance
      }};

      Graph.cameraPosition(targetCamPos, {{ x: nx, y: ny, z: nz }}, 1000);

      // 展开现代化全景看板
      document.getElementById('detail-drawer').classList.add('show');
      document.getElementById('drawer-title').innerText = node.fullLabel;
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
        artTag.innerText = '高精医学素材 / 结构式';
      }} else {{
        artImg.src = (catCfg && catCfg.icon) ? catCfg.icon : 'assets/63653-tablets-min.png';
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
          const tag = document.createElement('div');
          tag.className = 'conn-tag';
          const relType = e.relType || 'link';
          tag.innerHTML = `
            <span><b class="conn-rel ${{relType}}">${{e.relName}}</b> → ${{otherNode.label}}</span>
            <span style="color:#94A3B8; font-size:0.72rem;">${{e.description ? e.description.substring(0, 20) + '...' : ''}}</span>
          `;
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
    }}

    // 🌟 单点级联探索模式按钮
    document.getElementById('btn-cascade-mode').addEventListener('click', function() {{
      isCascadeMode = true;
      document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      document.querySelector('[data-preset="INITIAL_SEED"]').classList.add('active');
      loadCascadeSeed3D('DRUG_ESKETAMINE', 1);
    }});

    // 🌟 展开全景宏观总网按钮
    document.getElementById('btn-expand-all').addEventListener('click', function() {{
      isCascadeMode = false;
      document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      
      const allIds = new Set(graphRawData.nodes.map(n => n.id));
      updateGraphSubView(allIds);

      Graph.d3ReheatSimulation();
      Graph.cameraPosition({{ x: 0, y: 180, z: 620 }}, {{ x: 0, y: 0, z: 0 }}, 1000);
      document.getElementById('mode-text').innerText = '宏观全景总网 (187点/384连线)';
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
        document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
        document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
        this.classList.add('active');
        isCascadeMode = false;

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

    // 🔍 实时搜索与模糊匹配
    document.getElementById('search-input').addEventListener('input', function(e) {{
      const query = e.target.value.trim().toLowerCase();
      if (!query) return;

      const matchedNode = graphRawData.nodes.find(n => 
        n.label.toLowerCase().includes(query) || 
        n.fullLabel.toLowerCase().includes(query) ||
        n.id.toLowerCase().includes(query)
      );

      if (matchedNode) {{
        if (!currentVisibleNodeIds.has(matchedNode.id)) {{
          currentVisibleNodeIds.add(matchedNode.id);
          updateGraphSubView(currentVisibleNodeIds);
        }}
        focusNode3D(matchedNode.id);
      }}
    }});

    // 🌟 3D 空间排布算法引擎
    function applyCustom3DLayout(mode) {{
      currentLayoutMode = mode;
      const currentNodes = Graph.graphData().nodes;
      if (!currentNodes || currentNodes.length === 0) return;

      if (mode === 'force') {{
        // 恢复柔性动力学
        currentNodes.forEach(node => {{
          node.fx = undefined;
          node.fy = undefined;
          node.fz = undefined;
        }});
        Graph.d3Force('charge').strength(-320);
        Graph.d3ReheatSimulation();
      }} else if (mode === 'sphere') {{
        // 3D 同心球层宇宙排布 (Concentric Spheres via Fibonacci Sphere Algorithm)
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
          const phi = Math.PI * (Math.sqrt(5) - 1); // 黄金角

          group.forEach((node, i) => {{
            const y = 1 - (i / (N - 1 || 1)) * 2; // y 从 1 到 -1
            const radiusAtY = Math.sqrt(1 - y * y);
            const theta = phi * i;

            node.fx = Math.cos(theta) * radiusAtY * R;
            node.fy = y * R;
            node.fz = Math.sin(theta) * radiusAtY * R;
          }});
        }});
        Graph.d3ReheatSimulation();
      }} else if (mode === 'cylinder') {{
        // 3D 机制层级晶体柱排布 (Hierarchical Crystal Cylinder)
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
      document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      applyCustom3DLayout('force');
    }});

    document.getElementById('btn-layout-cluster').addEventListener('click', function() {{
      document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      applyCustom3DLayout('sphere');
    }});

    document.getElementById('btn-layout-hier').addEventListener('click', function() {{
      document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      applyCustom3DLayout('cylinder');
    }});

    // 💫 3D 空间舒展按钮：短暂提升斥力并重新舒展三维拓扑
    document.getElementById('btn-relax-physics').addEventListener('click', function() {{
      if (currentLayoutMode !== 'force') {{
        document.getElementById('btn-layout-force').click();
      }}
      Graph.d3Force('charge').strength(-600);
      Graph.d3ReheatSimulation();
      setTimeout(() => {{
        Graph.d3Force('charge').strength(-320);
      }}, 1200);
    }});

    document.getElementById('btn-zoom-fit').addEventListener('click', () => {{
      Graph.cameraPosition({{ x: 0, y: 160, z: 580 }}, {{ x: 0, y: 0, z: 0 }}, 800);
    }});

    document.getElementById('reset-filter-btn').addEventListener('click', () => {{
      document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
      document.querySelector('[data-preset="INITIAL_SEED"]').click();
    }});

    // 🚀 开屏默认：以艾司氯胺酮 Spravato® 为种子单点级联扩散
    loadCascadeSeed3D('DRUG_ESKETAMINE', 1);
  </script>
</body>
</html>
'''
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding="utf-8")
        return output_path
