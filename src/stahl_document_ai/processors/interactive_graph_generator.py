# -*- coding: utf-8 -*-
"""高精交互式图谱生成器：证据驱动关系网络、单点级联扩散、全场景无缝飞越与结构化临床药理卡片"""
import json
from pathlib import Path
from stahl_document_ai.processors.graph_builder import PsychopharmacologyKnowledgeGraph


class InteractiveGraphGenerator:
    """高精精神药理学可视化：证据关系网状连接、开屏单点级联探索、医学素材深度点缀、中文在先规范"""

    CATEGORY_CONFIG = {
        "Drug": {
            "name": "精神药物",
            "color": "#38BDF8",       # 亮青蓝
            "borderColor": "#0284C7",
            "glow": "rgba(56, 189, 248, 0.45)",
            "shape": "dot",
            "level": 2,
            "icon": "assets/63653-tablets-min.png"
        },
        "DrugClass": {
            "name": "药物大类",
            "color": "#818CF8",       # 靛蓝
            "borderColor": "#4F46E5",
            "glow": "rgba(129, 140, 248, 0.45)",
            "shape": "diamond",
            "level": 1,
            "icon": "assets/Field_Inventory_Menu_02.png"
        },
        "Receptor": {
            "name": "受体与信号靶点",
            "color": "#10B981",       # 翡翠荧绿
            "borderColor": "#059669",
            "glow": "rgba(16, 185, 129, 0.45)",
            "shape": "dot",
            "level": 3,
            "icon": "assets/mission.png"
        },
        "Pathway": {
            "name": "神经通路与可塑环路",
            "color": "#C084FC",       # 梦幻极光紫
            "borderColor": "#9333EA",
            "glow": "rgba(192, 132, 252, 0.45)",
            "shape": "hexagon",
            "level": 4,
            "icon": "assets/complete.png"
        },
        "Disease": {
            "name": "疾病与危重/难治表型",
            "color": "#F472B6",       # 玫粉
            "borderColor": "#DB2777",
            "glow": "rgba(244, 114, 182, 0.45)",
            "shape": "dot",
            "level": 5,
            "icon": "assets/NOTE.png"
        },
        "SideEffect": {
            "name": "不良反应",
            "color": "#FB7185",       # 珊瑚红
            "borderColor": "#E11D48",
            "glow": "rgba(251, 113, 133, 0.45)",
            "shape": "triangle",
            "level": 5,
            "icon": "assets/Goods_Icon_Gem_490_Preset_2.png"
        },
    }

    # 节点专属高精素材映射表（结构式、真实药片图、节律图标等）
    NODE_IMAGE_MAP = {
        "DRUG_ESKETAMINE": "assets/Esketamine2DCSD.svg",
        "DRUG_LISDEXAMFETAMINE": "assets/Dexmethylphenidate_structure.svg",
        "DRUG_METHYLPHENIDATE": "assets/Methylphenidate.svg",
        "DRUG_PREGABALIN": "assets/Pregabalin.png",
        "DRUG_CLONAZEPAM": "assets/clonazepam.png",
        "DRUG_TOLUDESVENLAFAXINE": "assets/63653-tablets-min.png",
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
        "PATH_CIRCADIAN_SCN": "assets/icon_morning.png",
        "DIS_INSOMNIA": "assets/icon_night.png",
        "PATH_HYPOTHALAMIC_AROUSAL": "assets/icon_evening.png",
        "PATH_CSTC_LOOPS": "assets/complete.png",
        "PATH_VTA_NACC_REWARD": "assets/Field_Inventory_Menu_02.png",
    }

    RELATION_CONFIG = {
        "AGONIST": {"color": "#10B981", "label": "激动受体"},
        "PARTIAL_AGONIST": {"color": "#F59E0B", "label": "部分激动"},
        "ANTAGONIST": {"color": "#EF4444", "label": "拮抗/阻断"},
        "INVERSE_AGONIST": {"color": "#E11D48", "label": "反向激动"},
        "PAM": {"color": "#06B6D4", "label": "正向变构调节 (PAM)"},
        "BLOCKER": {"color": "#6366F1", "label": "离子通道阻滞/酶抑制"},
        "INHIBITS": {"color": "#E11D48", "label": "再摄取抑制/逆转"},
        "TREATS": {"color": "#38BDF8", "label": "临床治疗/急救阻断/增效"},
        "CAUSES": {"color": "#FB923C", "label": "诱发不良反应"},
        "MODULATES": {"color": "#A855F7", "label": "级联/环路调控"},
        "CORRELATED_WITH": {"color": "#EC4899", "label": "病理关联/演进"},
        "IS_A": {"color": "#64748B", "label": "分类归属"},
    }

    @classmethod
    def generate_html(cls, graph: PsychopharmacologyKnowledgeGraph, output_path: Path) -> Path:
        degree_map = {}
        for e in graph.edges:
            degree_map[e.source] = degree_map.get(e.source, 0) + 1
            degree_map[e.target] = degree_map.get(e.target, 0) + 1

        vis_nodes = []
        for n in graph.nodes:
            cfg = cls.CATEGORY_CONFIG.get(n.category, {
                "name": n.category, "color": "#94A3B8", "borderColor": "#475569", "glow": "rgba(148,163,184,0.3)", "shape": "dot", "level": 3
            })
            deg = degree_map.get(n.id, 1)
            is_critical = n.id in [
                "DIS_MDSI", "DIS_TRD", "DRUG_ESKETAMINE", "DRUG_LISDEXAMFETAMINE",
                "DRUG_TOLUDESVENLAFAXINE", "DRUG_DIMDAZENIL", "DRUG_FAZAMOREXANT", "DRUG_VORNOREXANT",
                "DRUG_ULOTARONT", "DRUG_ZURANOLONE", "DRUG_AUVELITY", "DRUG_PITOLISANT",
                "DRUG_AGOMELATINE", "REC_MT1_MT2", "PATH_CIRCADIAN_SCN", "REC_TAAR1", "REC_OX1R_OX2R",
                "REC_BDNF_TRKB", "REC_AMPA", "REC_MTORC1", "DRUG_VARENICLINE", "DRUG_LECANEMAB"
            ]
            node_size = min(40, max(18, (24 if is_critical else 16) + deg * 1.25))
            clean_label = n.label.split("(")[0].strip() if "(" in n.label else n.label

            custom_img = cls.NODE_IMAGE_MAP.get(n.id, "")

            vis_nodes.append({
                "id": n.id,
                "label": clean_label,
                "fullLabel": n.label,
                "category": n.category,
                "categoryName": cfg["name"],
                "description": n.description,
                "degree": deg,
                "level": cfg["level"],
                "customImage": custom_img,
                "color": {
                    "background": cfg["color"],
                    "border": "#FFFFFF" if is_critical else cfg["borderColor"],
                    "highlight": {
                        "background": "#FFFFFF",
                        "border": cfg["color"],
                    },
                    "hover": {
                        "background": "#FFFFFF",
                        "border": cfg["borderColor"],
                    }
                },
                "shadow": {
                    "enabled": True,
                    "color": cfg["glow"],
                    "size": 16 if is_critical else 10,
                    "x": 0,
                    "y": 0,
                },
                "shape": cfg["shape"],
                "size": node_size,
                "font": {
                    "color": "#F8FAFC",
                    "size": 13,
                    "face": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                    "strokeWidth": 2.5,
                    "strokeColor": "#070B12",
                },
                "borderWidth": 3 if is_critical else 2,
                "borderWidthSelected": 4,
            })

        vis_edges = []
        for i, e in enumerate(graph.edges):
            rel_cfg = cls.RELATION_CONFIG.get(e.relationship, {"color": "#475569", "label": e.label})
            is_key_edge = (
                e.source in [
                    "DRUG_ESKETAMINE", "REC_AMPA", "REC_MTORC1", "REC_BDNF_TRKB", "DRUG_TOLUDESVENLAFAXINE",
                    "DRUG_DIMDAZENIL", "DRUG_FAZAMOREXANT", "DRUG_VORNOREXANT", "DRUG_ULOTARONT",
                    "DRUG_ZURANOLONE", "DRUG_AGOMELATINE", "REC_MT1_MT2", "REC_OX1R_OX2R"
                ]
                or e.target in ["DIS_MDSI", "DIS_TRD", "PATH_CIRCADIAN_SCN", "PATH_CSTC_LOOPS", "PATH_VTA_NACC_REWARD", "DIS_INSOMNIA"]
            )
            vis_edges.append({
                "id": f"edge_{i}",
                "from": e.source,
                "to": e.target,
                "label": "",
                "hoverLabel": e.label,
                "relationship": e.relationship,
                "relName": rel_cfg["label"],
                "description": e.description,
                "color": {
                    "color": (rel_cfg["color"] + ("EE" if is_key_edge else "85")),
                    "highlight": "#FACC15",
                    "hover": "#38BDF8",
                    "opacity": 0.85 if is_key_edge else 0.55,
                },
                "arrows": {
                    "to": {"enabled": True, "scaleFactor": 0.55}
                },
                "width": max(1.5, min(4.2, e.weight * (1.8 if is_key_edge else 1.3))),
                "smooth": {
                    "type": "curvedCW",
                    "roundness": 0.12,
                }
            })

        graph_data_json = json.dumps({"nodes": vis_nodes, "edges": vis_edges}, ensure_ascii=False)

        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stahl 精神药理学精要 (第5版) · 全书全景知识图谱</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    :root {{
      --bg-dark: #070B12;
      --bg-card: rgba(12, 18, 30, 0.88);
      --border-light: rgba(255, 255, 255, 0.08);
      --border-glow: rgba(56, 189, 248, 0.35);
      --text-main: #F9FAFB;
      --text-sub: #94A3B8;
      --accent-blue: #38BDF8;
      --accent-purple: #C084FC;
      --accent-green: #10B981;
      --accent-amber: #F59E0B;
      --accent-pink: #F472B6;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }}
    body {{ background: var(--bg-dark); color: var(--text-main); height: 100vh; display: flex; overflow: hidden; }}

    #network-container {{
      flex: 1;
      height: 100%;
      position: relative;
      background: radial-gradient(circle at 50% 50%, #0F1A2E 0%, #070B12 92%);
    }}

    #sidebar {{
      width: 470px;
      background: var(--bg-card);
      backdrop-filter: blur(22px);
      -webkit-backdrop-filter: blur(22px);
      border-right: 1px solid var(--border-light);
      display: flex;
      flex-direction: column;
      padding: 20px;
      z-index: 20;
      box-shadow: 14px 0 45px rgba(0, 0, 0, 0.7);
      overflow-y: auto;
    }}

    .header-box {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 6px;
    }}
    .header-logo {{
      width: 42px;
      height: 42px;
      border-radius: 10px;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(192, 132, 252, 0.15));
      border: 1px solid var(--border-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
      overflow: hidden;
    }}
    .header-logo img {{ width: 30px; height: 30px; object-fit: contain; }}

    .header-title {{
      font-size: 1.25rem;
      font-weight: 800;
      background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .header-sub {{ font-size: 0.76rem; color: var(--text-sub); margin-bottom: 12px; line-height: 1.45; }}

    .mode-banner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 10px;
      padding: 8px 12px;
      margin-bottom: 14px;
      font-size: 0.76rem;
    }}
    .mode-pill {{
      background: #0284C7;
      color: #fff;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.68rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .mode-pill:hover {{ background: #0369A1; transform: scale(1.04); }}

    .scenario-section {{ margin-bottom: 16px; }}
    .section-title {{ font-size: 0.73rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #94A3B8; margin-bottom: 9px; display: flex; justify-content: space-between; align-items: center; }}
    .preset-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .chip {{
      padding: 5px 10px;
      border-radius: 18px;
      font-size: 0.72rem;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-light);
      color: #CBD5E1;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .chip img {{ width: 13px; height: 13px; object-fit: contain; border-radius: 3px; }}
    .chip:hover {{ background: rgba(56, 189, 248, 0.15); border-color: var(--accent-blue); color: #fff; transform: translateY(-1px); }}
    .chip.active {{ background: linear-gradient(135deg, #0284C7, #2563EB); border-color: #38BDF8; color: #fff; font-weight: 600; box-shadow: 0 0 14px rgba(56, 189, 248, 0.45); }}

    .search-wrapper {{ position: relative; margin-bottom: 16px; }}
    .search-input {{
      width: 100%;
      padding: 10px 14px 10px 38px;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid var(--border-light);
      border-radius: 12px;
      color: #fff;
      font-size: 0.86rem;
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{ border-color: var(--accent-blue); box-shadow: 0 0 14px rgba(56, 189, 248, 0.35); }}
    .search-icon-img {{ position: absolute; left: 12px; top: 11px; width: 16px; height: 16px; opacity: 0.7; }}

    .layout-switcher {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .layout-btn {{
      padding: 8px;
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-light);
      border-radius: 8px;
      color: #CBD5E1;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
    }}
    .layout-btn.active {{ background: rgba(56, 189, 248, 0.2); border-color: var(--accent-blue); color: var(--accent-blue); box-shadow: 0 0 10px rgba(56,189,248,0.25); }}

    .filter-list {{ display: flex; flex-direction: column; gap: 5px; margin-bottom: 16px; }}
    .filter-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 7px 10px;
      background: rgba(15, 23, 42, 0.45);
      border: 1px solid var(--border-light);
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.78rem;
      transition: all 0.15s;
    }}
    .filter-item:hover {{ background: rgba(255, 255, 255, 0.08); border-color: rgba(56, 189, 248, 0.3); }}
    .filter-item.active {{ background: rgba(56, 189, 248, 0.2); border-color: var(--accent-blue); font-weight: 700; }}
    .filter-left {{ display: flex; align-items: center; gap: 8px; }}
    .filter-icon {{ width: 14px; height: 14px; object-fit: contain; }}
    .filter-dot {{ width: 8px; height: 8px; border-radius: 50%; }}
    .filter-count {{ font-size: 0.7rem; color: var(--text-sub); background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 10px; }}

    #detail-drawer {{
      margin-top: 14px;
      background: rgba(15, 23, 42, 0.98);
      border: 1px solid var(--border-glow);
      border-radius: 14px;
      padding: 16px;
      display: none;
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
      animation: fadeIn 0.22s ease-out;
      position: relative;
    }}
    #detail-drawer.show {{ display: block; }}
    .drawer-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
    .drawer-badge {{ display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #fff; }}
    .drawer-art-preview {{ width: 46px; height: 46px; border-radius: 8px; background: rgba(255,255,255,0.05); padding: 4px; border: 1px solid var(--border-light); object-fit: contain; }}
    .drawer-title {{ font-size: 1.05rem; font-weight: 800; color: #fff; margin-bottom: 8px; line-height: 1.35; }}
    .drawer-desc-card {{ font-size: 0.80rem; color: #CBD5E1; line-height: 1.6; margin-bottom: 12px; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); white-space: pre-line; }}
    .drawer-conns-title {{ font-size: 0.75rem; font-weight: 700; color: var(--text-sub); text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between; }}
    .drawer-conns-list {{ display: flex; flex-direction: column; gap: 6px; max-height: 150px; overflow-y: auto; font-size: 0.76rem; }}
    .conn-tag {{ padding: 6px 9px; border-radius: 6px; background: rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: all 0.15s; border: 1px solid transparent; }}
    .conn-tag:hover {{ background: rgba(56, 189, 248, 0.15); border-color: var(--accent-blue); transform: translateX(2px); }}

    .top-floating-bar {{
      position: absolute;
      top: 20px;
      right: 20px;
      display: flex;
      gap: 8px;
      z-index: 10;
    }}
    .tool-btn {{
      background: var(--bg-card);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-light);
      color: #E2E8F0;
      padding: 8px 13px;
      border-radius: 10px;
      font-size: 0.80rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.4);
      transition: all 0.2s;
    }}
    .tool-btn img {{ width: 14px; height: 14px; object-fit: contain; }}
    .tool-btn:hover {{ background: rgba(56, 189, 248, 0.22); border-color: var(--accent-blue); color: #fff; }}
    .tool-btn.highlight {{ background: linear-gradient(135deg, #0284C7, #2563EB); border-color: #38BDF8; color: #fff; box-shadow: 0 0 12px rgba(56,189,248,0.4); }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>
  <div id="sidebar">
    <div class="header-box">
      <div class="header-logo">
        <img src="assets/63653-tablets-min.png" alt="Logo" />
      </div>
      <div>
        <div class="header-title">Stahl 精神药理学全景图谱</div>
        <div class="header-sub" style="margin-bottom:0;">第5版全书 14 章全域机制 · 靶点与回路全景闭环</div>
      </div>
    </div>
    <hr style="border:none; border-top:1px solid var(--border-light); margin:12px 0 14px 0;" />

    <!-- 级联探索状态横幅 -->
    <div class="mode-banner">
      <span>💡 模式: <b id="mode-text" style="color:var(--accent-blue);">单点级联探索 (点击节点自动扩散)</b></span>
      <span class="mode-pill" id="btn-toggle-all-view">全景总网</span>
    </div>

    <!-- 快捷药理场景切换 (全书 14 章重点板块) -->
    <div class="scenario-section">
      <div class="section-title">
        <span>✨ 核心专病与前沿机制透视</span>
      </div>
      <div class="preset-chips">
        <span class="chip active" data-preset="INITIAL_SEED">
          <img src="assets/Esketamine2DCSD.svg" alt="" />
          🌟 开屏单点探索 (艾司氯胺酮 Spravato®)
        </span>
        <span class="chip" data-preset="DIMDAZENIL">
          <img src="assets/63653-tablets-min.png" alt="" />
          🌿 地达西尼 (京诺宁®) / GABA-A α1 部分变构
        </span>
        <span class="chip" data-preset="DORA">
          <img src="assets/icon_night.png" alt="" />
          🌙 沃诺雷生 (Vorzzz) / 法赞雷生 / 莱博雷生 (达卫可®)
        </span>
        <span class="chip" data-preset="WAKE_NARCOLEPSY">
          <img src="assets/icon_morning.png" alt="" />
          ☀️ 替洛利生 (铧可思®) / 莫达非尼 / 促醒睡病
        </span>
        <span class="chip" data-preset="ADHD_PFC">
          <img src="assets/Dexmethylphenidate_structure.svg" alt="" />
          🚀 赖右苯丙胺（利右苯丙胺） / 维洛沙嗪 (ADHD)
        </span>
        <span class="chip" data-preset="CRISIS">
          <img src="assets/Esketamine2DCSD.svg" alt="" />
          🚨 自杀干预 (MDSI) / 难治抑郁 (TRD)
        </span>
        <span class="chip" data-preset="SNDRI">
          <img src="assets/63653-tablets-min.png" alt="" />
          💎 托鲁地文拉法辛 (若欣林®) / SNDRI
        </span>
        <span class="chip" data-preset="PPD">
          <img src="assets/63653-tablets-min.png" alt="" />
          🌸 佐拉诺酮 (Zurzuvae) / 产后抑郁 (PPD)
        </span>
        <span class="chip" data-preset="AUVELITY">
          <img src="assets/63653-tablets-min.png" alt="" />
          ⚡ 右美沙芬-安非他酮 / 快速抗抑郁 (Auvelity)
        </span>
        <span class="chip" data-preset="NEW_PSYCHOSIS">
          <img src="assets/mission.png" alt="" />
          🔮 乌洛他隆 / 卢玛哌酮 (Caplyta) / TAAR1
        </span>
        <span class="chip" data-preset="OCD_CSTC">
          <img src="assets/complete.png" alt="" />
          🕯️ 氟伏沙明 (兰释®) / 氯米帕明 / 强迫障碍 (OCD)
        </span>
        <span class="chip" data-preset="PTSD_FEAR">
          <img src="assets/NOTE.png" alt="" />
          🛡️ 哌唑嗪 / 普萘洛尔 / 创伤恐惧消退 (PTSD)
        </span>
        <span class="chip" data-preset="DEMENTIA_AD">
          <img src="assets/mission.png" alt="" />
          🧩 多奈哌齐 (安理申®) / 美金刚 / 仑卡奈单抗
        </span>
        <span class="chip" data-preset="ADDICTION_REWARD">
          <img src="assets/Field_Inventory_Menu_02.png" alt="" />
          🍷 伐尼克兰 (畅沛®) / 纳曲酮 / 戒断奖赏回路
        </span>
        <span class="chip" data-preset="AGOMELATINE">
          <img src="assets/icon_night.png" alt="" />
          🌌 阿戈美拉汀 (韦度®) / 视交叉上核节律 (MASSA)
        </span>
        <span class="chip" data-preset="PLASTICITY">
          <img src="assets/complete.png" alt="" />
          🌱 神经可塑性与突触再生 (BDNF / mTOR / AMPA)
        </span>
        <span class="chip" data-preset="D2_D3_PARTIAL">
          <img src="assets/63653-tablets-min.png" alt="" />
          ⭐ 布瑞哌唑 (敏达妥®) / 卡利拉嗪 (罗珊®)
        </span>
        <span class="chip" data-preset="SMS_VORTIO">
          <img src="assets/mission.png" alt="" />
          🧠 伏硫西汀 (心达悦® / 海马 LTP 突触再生)
        </span>
        <span class="chip" data-preset="PREGABALIN">
          <img src="assets/Pregabalin.png" alt="" />
          🛡️ 普瑞巴林 (乐瑞卡®) / 丁螺环酮 / 广泛焦虑
        </span>
        <span class="chip" data-preset="MOOD">
          <img src="assets/Field_Inventory_Menu_02.png" alt="" />
          ⚖️ 心境稳定剂 (碳酸锂 / 丙戊酸钠 / 卡马西平)
        </span>
        <span class="chip" data-preset="BZD_ANXIETY">
          <img src="assets/clonazepam.png" alt="" />
          🌿 苯二氮䓬类药物 (劳拉西泮 / 阿普唑仑)
        </span>
        <span class="chip" data-preset="ALL">
          <img src="assets/63653-tablets-min.png" alt="" />
          🌐 展开全景总网 (187点/384连线)
        </span>
      </div>
    </div>

    <!-- 搜索 -->
    <div class="search-wrapper">
      <img src="assets/mission.png" class="search-icon-img" alt="search" />
      <input type="text" id="search-input" class="search-input" placeholder="搜索全书实体 (如 京诺宁, 沃诺雷生, 铧可思, 达卫可, 敏达妥)..." />
    </div>

    <!-- 布局切换 -->
    <div class="section-title">📐 排布形态</div>
    <div class="layout-switcher">
      <button class="layout-btn active" id="btn-layout-force">💫 柔性松弛 (防挤飞)</button>
      <button class="layout-btn" id="btn-layout-cluster">🎯 同心聚类</button>
      <button class="layout-btn" id="btn-layout-hier">🌲 机制层级</button>
    </div>

    <!-- 类别过滤 -->
    <div class="section-title">
      <span>🎨 实体类别 (以相互关系为证据连接呈现)</span>
      <span id="reset-filter-btn" style="cursor:pointer; color:var(--accent-blue); text-transform:none;">重置</span>
    </div>
    <div class="filter-list" id="filter-container"></div>

    <!-- 详情抽屉 -->
    <div id="detail-drawer">
      <div class="drawer-header">
        <span class="drawer-badge" id="drawer-badge" style="background:#38BDF8">精神药物</span>
        <img id="drawer-art" class="drawer-art-preview" src="assets/63653-tablets-min.png" alt="Preview" />
      </div>
      <div class="drawer-title" id="drawer-title">...</div>
      <div class="drawer-desc-card" id="drawer-desc">...</div>
      <div class="drawer-conns-title">
        <span>🔗 关联受体靶点与神经回路 (点击跳转)</span>
      </div>
      <div class="drawer-conns-list" id="drawer-conns"></div>
    </div>
  </div>

  <div id="network-container">
    <div class="top-floating-bar">
      <button class="tool-btn highlight" id="btn-cascade-mode">
        <img src="assets/mission.png" alt="" />
        单点级联探索
      </button>
      <button class="tool-btn" id="btn-expand-all">
        <img src="assets/Field_Inventory_Menu_02.png" alt="" />
        全景宏观总网
      </button>
      <button class="tool-btn" id="btn-zoom-fit">
        <img src="assets/complete.png" alt="" />
        适配视野
      </button>
    </div>
  </div>

  <script>
    const graphData = {graph_data_json};
    const categoryConfig = {json.dumps(cls.CATEGORY_CONFIG, ensure_ascii=False)};
    
    const catCounts = {{}};
    graphData.nodes.forEach(n => {{
      catCounts[n.category] = (catCounts[n.category] || 0) + 1;
    }});

    const adjMap = {{}};
    graphData.nodes.forEach(n => adjMap[n.id] = new Set());
    graphData.edges.forEach(e => {{
      if (adjMap[e.from]) adjMap[e.from].add(e.to);
      if (adjMap[e.to]) adjMap[e.to].add(e.from);
    }});

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
          <div class="filter-dot" style="background: ${{cfg.color}}; box-shadow: 0 0 8px ${{cfg.color}};"></div>
          <span>${{cfg.name}} (${{cat}})</span>
        </div>
        <span class="filter-count">${{count}}</span>
      `;
      // 🌟 核心升级：以相互关系为证据将该类别节点与直接相互作用实体紧密连接在一起！
      item.addEventListener('click', function() {{
        document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
        isCascadeMode = false;

        // 1. 找到所有本类别的核心节点
        const primaryNodes = graphData.nodes.filter(n => n.category === cat);
        const primaryIds = new Set(primaryNodes.map(n => n.id));
        
        // 2. 收集与这些节点有直接证据关系连线的邻居节点
        const linkedIds = new Set(primaryIds);
        primaryIds.forEach(pId => {{
          const neighbors = adjMap[pId] || new Set();
          neighbors.forEach(nId => linkedIds.add(nId));
        }});

        // 3. 构建完整的证据闭环子图
        currentVisibleNodeIds = linkedIds;
        const subNodes = graphData.nodes.filter(n => linkedIds.has(n.id));
        const subEdges = graphData.edges.filter(e => linkedIds.has(e.from) && linkedIds.has(e.to));

        nodesDataSet.clear();
        edgesDataSet.clear();
        nodesDataSet.add(subNodes);
        edgesDataSet.add(subEdges);
        network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
        document.getElementById('mode-text').innerText = `已激活: ${{cfg.name}} 证据关系全网 (共 ${{subNodes.length}} 节点, ${{subEdges.length}} 关系边)`;
        
        if (primaryNodes.length > 0) {{
          focusNode(primaryNodes[0].id);
        }}
      }});
      filterContainer.appendChild(item);
    }});

    const nodesDataSet = new vis.DataSet([]);
    const edgesDataSet = new vis.DataSet([]);

    // 🛡️ 柔性流体动力学防挤飞配置
    const baseOptions = {{
      nodes: {{
        borderWidth: 2,
        shadow: true,
      }},
      edges: {{
        smooth: {{ type: 'curvedCW', roundness: 0.12 }},
        arrows: {{ to: {{ enabled: true, scaleFactor: 0.55 }} }},
        selectionWidth: 3.5,
        hoverWidth: 2.2,
      }},
      physics: {{
        barnesHut: {{
          gravitationalConstant: -26000,
          centralGravity: 0.20,
          springLength: 145,
          springConstant: 0.040,
          damping: 0.50,
          avoidOverlap: 0.88
        }},
        maxVelocity: 20,
        minVelocity: 0.1,
        timestep: 0.35,
        solver: 'barnesHut',
        stabilization: {{
          enabled: true,
          iterations: 300,
          updateInterval: 25,
          onlyDynamicEdges: false,
          fit: true
        }}
      }},
      interaction: {{
        hover: true,
        tooltipDelay: 80,
        zoomView: true
      }}
    }};

    const container = document.getElementById('network-container');
    const network = new vis.Network(container, {{ nodes: nodesDataSet, edges: edgesDataSet }}, baseOptions);

    let currentVisibleNodeIds = new Set();
    let isCascadeMode = true;

    // 🌟 单点级联扩散呈现（开屏及逐级裂变）
    function loadCascadeSeed(seedNodeId, depth = 1) {{
      const visibleIds = new Set([seedNodeId]);
      
      // 1度邻居
      const neighbors = adjMap[seedNodeId] || new Set();
      neighbors.forEach(id => visibleIds.add(id));

      if (depth >= 2) {{
        neighbors.forEach(nId => {{
          const n2 = adjMap[nId] || new Set();
          n2.forEach(id => {{
            if (visibleIds.size < 22) visibleIds.add(id);
          }});
        }});
      }}

      currentVisibleNodeIds = visibleIds;
      const subNodes = graphData.nodes.filter(n => visibleIds.has(n.id));
      const subEdges = graphData.edges.filter(e => visibleIds.has(e.from) && visibleIds.has(e.to));

      nodesDataSet.clear();
      edgesDataSet.clear();
      nodesDataSet.add(subNodes);
      edgesDataSet.add(subEdges);

      focusNode(seedNodeId);
      document.getElementById('mode-text').innerText = '单点级联扩散探索 (点击节点裂变展开)';
    }}

    // 动态级联展开邻居
    function expandCascade(nodeId) {{
      const neighbors = adjMap[nodeId] || new Set();
      let added = false;
      neighbors.forEach(nId => {{
        if (!currentVisibleNodeIds.has(nId)) {{
          currentVisibleNodeIds.add(nId);
          const nodeObj = graphData.nodes.find(n => n.id === nId);
          if (nodeObj) nodesDataSet.add(nodeObj);
          added = true;
        }}
      }});

      if (added) {{
        const newEdges = graphData.edges.filter(e => currentVisibleNodeIds.has(e.from) && currentVisibleNodeIds.has(e.to));
        edgesDataSet.clear();
        edgesDataSet.add(newEdges);
      }}
    }}

    function focusNode(nodeId) {{
      const node = graphData.nodes.find(n => n.id === nodeId);
      if (!node) return;

      // 相机平滑飞越聚焦
      network.focus(nodeId, {{
        scale: 1.18,
        animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }}
      }});

      // 展开详情抽屉
      document.getElementById('detail-drawer').classList.add('show');
      document.getElementById('drawer-title').innerText = node.fullLabel;
      document.getElementById('drawer-desc').innerText = node.description || 'Stahl 精神药理学核心实体。';
      const badge = document.getElementById('drawer-badge');
      badge.innerText = node.categoryName;
      badge.style.background = node.color.background;

      const artImg = document.getElementById('drawer-art');
      if (node.customImage) {{
        artImg.src = node.customImage;
        artImg.style.display = 'block';
      }} else {{
        const catCfg = categoryConfig[node.category];
        artImg.src = (catCfg && catCfg.icon) ? catCfg.icon : 'assets/63653-tablets-min.png';
        artImg.style.display = 'block';
      }}

      // 关联列表（支持点击跳转）
      const connsDiv = document.getElementById('drawer-conns');
      connsDiv.innerHTML = '';
      const relatedEdges = graphData.edges.filter(e => e.from === nodeId || e.to === nodeId);
      relatedEdges.forEach(e => {{
        const otherId = e.from === nodeId ? e.to : e.from;
        const otherNode = graphData.nodes.find(n => n.id === otherId);
        if (otherNode) {{
          const tag = document.createElement('div');
          tag.className = 'conn-tag';
          tag.innerHTML = `<span><b>${{e.relName}}</b> \u2192 ${{otherNode.label}}</span> <span style="color:#94A3B8; font-size:0.7rem;">${{e.description || ''}}</span>`;
          tag.addEventListener('click', function(ev) {{
            ev.stopPropagation();
            if (!currentVisibleNodeIds.has(otherId)) {{
              currentVisibleNodeIds.add(otherId);
              nodesDataSet.add(otherNode);
              const newEdges = graphData.edges.filter(ed => currentVisibleNodeIds.has(ed.from) && currentVisibleNodeIds.has(ed.to));
              edgesDataSet.clear();
              edgesDataSet.add(newEdges);
            }}
            focusNode(otherId);
            if (isCascadeMode) expandCascade(otherId);
          }});
          connsDiv.appendChild(tag);
        }}
      }});
    }}

    function resetHighlight() {{
      // 保留当前视图
    }}

    network.on('click', function(params) {{
      if (params.nodes.length > 0) {{
        const clickedId = params.nodes[0];
        focusNode(clickedId);
        if (isCascadeMode) {{
          expandCascade(clickedId);
        }}
      }}
    }});

    // 默认开屏：初始仅一个核心点（艾司氯胺酮与突触再生），级联发散周边
    loadCascadeSeed('DRUG_ESKETAMINE', 1);

    document.getElementById('btn-expand-all').addEventListener('click', function() {{
      isCascadeMode = false;
      document.getElementById('btn-cascade-mode').classList.remove('highlight');
      this.classList.add('highlight');
      document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
      const allChip = document.querySelector('[data-preset="ALL"]');
      if (allChip) allChip.classList.add('active');

      nodesDataSet.clear();
      edgesDataSet.clear();
      nodesDataSet.add(graphData.nodes);
      edgesDataSet.add(graphData.edges);
      currentVisibleNodeIds = new Set(graphData.nodes.map(n => n.id));
      network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
      document.getElementById('mode-text').innerText = '宏观全景总网 (187点/384连线)';
    }});

    document.getElementById('btn-toggle-all-view').addEventListener('click', function() {{
      document.getElementById('btn-expand-all').click();
    }});

    document.getElementById('btn-cascade-mode').addEventListener('click', function() {{
      isCascadeMode = true;
      document.getElementById('btn-expand-all').classList.remove('highlight');
      this.classList.add('highlight');
      loadCascadeSeed('DRUG_ESKETAMINE', 1);
    }});

    document.getElementById('search-input').addEventListener('input', function(e) {{
      const q = e.target.value.trim().toLowerCase();
      if (!q) return;

      const matched = graphData.nodes.find(n => n.fullLabel.toLowerCase().includes(q) || (n.description && n.description.toLowerCase().includes(q)));
      if (matched) {{
        if (!currentVisibleNodeIds.has(matched.id)) {{
          loadCascadeSeed(matched.id, 1);
        }} else {{
          focusNode(matched.id);
        }}
      }}
    }});

    // 快捷预设视角过滤
    document.querySelectorAll('.preset-chips .chip').forEach(chip => {{
      chip.addEventListener('click', function() {{
        document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
        const preset = this.dataset.preset;

        if (preset === 'INITIAL_SEED') {{
          isCascadeMode = true;
          document.getElementById('btn-cascade-mode').classList.add('highlight');
          document.getElementById('btn-expand-all').classList.remove('highlight');
          loadCascadeSeed('DRUG_ESKETAMINE', 1);
          return;
        }} else if (preset === 'ALL') {{
          document.getElementById('btn-expand-all').click();
          return;
        }}

        isCascadeMode = false;
        document.getElementById('btn-cascade-mode').classList.remove('highlight');
        document.getElementById('btn-expand-all').classList.remove('highlight');
        let filterFn = () => true;

        if (preset === 'DIMDAZENIL') {{
          const set = new Set([
            'CLS_GABAA_PARTIAL_PAM', 'DRUG_DIMDAZENIL', 'REC_GABAA_ALPHA1_PARTIAL', 'PATH_VLPO_SLEEP_SWITCH', 'DIS_INSOMNIA'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'DORA') {{
          const set = new Set([
            'CLS_DORA', 'DRUG_FAZAMOREXANT', 'DRUG_VORNOREXANT', 'DRUG_LEMBOREXANT', 'DRUG_DARIDOREXANT',
            'REC_OX1R_OX2R', 'PATH_HYPOTHALAMIC_AROUSAL', 'DIS_INSOMNIA'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'WAKE_NARCOLEPSY') {{
          const set = new Set([
            'CLS_WAKE_PROMOTING', 'CLS_H3_ANTAGONIST', 'CLS_GABAB_GHB', 'DRUG_MODAFINIL', 'DRUG_ARMODAFINIL', 'DRUG_PITOLISANT', 'DRUG_SODIUM_OXYBATE',
            'REC_DAT', 'REC_HISTAMINE_H3', 'REC_GHB_GABAB', 'PATH_HYPOTHALAMIC_AROUSAL', 'PATH_TMN_HISTAMINE_AROUSAL', 'PATH_VLPO_SLEEP_SWITCH', 'DIS_NARCOLEPSY'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'ADHD_PFC') {{
          const set = new Set([
            'CLS_ADHD_STIMULANT', 'CLS_ADHD_NON_STIMULANT', 'DRUG_LISDEXAMFETAMINE', 'DRUG_METHYLPHENIDATE', 'DRUG_ATOMOXETINE', 'DRUG_GUANFACINE', 'DRUG_VILOXAZINE',
            'REC_DAT', 'REC_NET', 'REC_VMAT2', 'REC_ALPHA2A', 'REC_D1', 'REC_5HT7', 'PATH_PFC_CIRCUITS', 'DIS_ADHD', 'SE_ADDICTION_TOLERANCE'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'CRISIS') {{
          const set = new Set([
            'DIS_MDSI', 'DIS_TRD', 'DIS_MDD', 'DRUG_ESKETAMINE', 'DRUG_LITHIUM', 'DRUG_BREXPIPRAZOLE', 'DRUG_ARIPIPRAZOLE', 'DRUG_QUETIAPINE',
            'REC_NMDA', 'REC_AMPA', 'REC_MTORC1', 'REC_BDNF_TRKB', 'REC_GSK3B',
            'PATH_HIPPOCAMPAL_PLASTICITY', 'PATH_PFC_CIRCUITS', 'CLS_NMDA_MODULATOR', 'CLS_MOOD_STABILIZER', 'CLS_D2_PARTIAL'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'SNDRI') {{
          const set = new Set([
            'CLS_SNDRI', 'DRUG_TOLUDESVENLAFAXINE', 'REC_SERT', 'REC_NET', 'REC_DAT',
            'PATH_PFC_CIRCUITS', 'DIS_MDD', 'DIS_TRD'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'PPD') {{
          const set = new Set([
            'CLS_GABAA_NEUROSTEROID_PAM', 'DRUG_ZURANOLONE', 'DRUG_BREXANOLONE', 'REC_GABAA_NEUROSTEROID',
            'PATH_AMYGDALA_CIRCUITS', 'DIS_PPD', 'DIS_MDD'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'AUVELITY') {{
          const set = new Set([
            'CLS_DXM_BUP', 'DRUG_AUVELITY', 'DRUG_BUPROPION', 'REC_NMDA', 'REC_SIGMA1', 'REC_NET', 'REC_DAT',
            'PATH_HIPPOCAMPAL_PLASTICITY', 'DIS_MDD', 'DIS_TRD', 'DIS_TOBACCO'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'NEW_PSYCHOSIS') {{
          const set = new Set([
            'CLS_TAAR1_AGONIST', 'CLS_5HT2A_INVERSE', 'CLS_SDA', 'DRUG_ULOTARONT', 'DRUG_PIMAVANSERIN', 'DRUG_LUMATEPERONE',
            'REC_TAAR1', 'REC_5HT2A_INVERSE', 'REC_5HT2A', 'REC_D2', 'PATH_MESOLIMBIC', 'PATH_MESOCORTICAL',
            'DIS_SCHIZOPHRENIA_POS', 'DIS_SCHIZOPHRENIA_NEG', 'DIS_PDP', 'DIS_BIPOLAR_DEP'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'OCD_CSTC') {{
          const set = new Set([
            'CLS_SSRI', 'CLS_TCA', 'DRUG_FLUVOXAMINE', 'DRUG_CLOMIPRAMINE', 'REC_SERT', 'REC_SIGMA1',
            'PATH_CSTC_LOOPS', 'DIS_OCD'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'PTSD_FEAR') {{
          const set = new Set([
            'DRUG_PRAZOSIN', 'DRUG_PROPRANOLOL', 'DRUG_SERTRALINE', 'REC_ALPHA1', 'REC_BETA_ADRENERGIC', 'REC_SERT',
            'PATH_FEAR_EXTINCTION', 'PATH_AMYGDALA_CIRCUITS', 'DIS_PTSD', 'DIS_SAD'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'DEMENTIA_AD') {{
          const set = new Set([
            'CLS_ACHEI', 'CLS_ANTI_AMYLOID_MAB', 'CLS_NMDA_MODULATOR', 'DRUG_DONEPEZIL', 'DRUG_RIVASTIGMINE', 'DRUG_GALANTAMINE', 'DRUG_MEMANTINE', 'DRUG_LECANEMAB', 'DRUG_DONANEMAB',
            'REC_ACHE', 'REC_NMDA', 'REC_AMYLOID_BETA', 'REC_NACHR_ALPHA4BETA2', 'PATH_BASAL_FOREBRAIN_ACH', 'PATH_HIPPOCAMPAL_PLASTICITY', 'DIS_ALZHEIMER'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'ADDICTION_REWARD') {{
          const set = new Set([
            'CLS_ADDICTION_TREATMENT', 'DRUG_VARENICLINE', 'DRUG_NALTREXONE', 'DRUG_ACAMPROSATE', 'DRUG_DISULFIRAM', 'DRUG_BUPRENORPHINE', 'DRUG_NALOXONE', 'DRUG_BUPROPION',
            'REC_NACHR_ALPHA4BETA2', 'REC_MU_OPIOID', 'REC_KAPPA_OPIOID', 'REC_ALDH', 'REC_NMDA', 'REC_DAT',
            'PATH_VTA_NACC_REWARD', 'DIS_AUD', 'DIS_OUD', 'DIS_TOBACCO'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'AGOMELATINE') {{
          const set = new Set([
            'CLS_MASSA', 'DRUG_AGOMELATINE', 'DRUG_RAMELTEON', 'REC_MT1_MT2', 'REC_5HT2C',
            'PATH_CIRCADIAN_SCN', 'PATH_PFC_CIRCUITS', 'DIS_MDD', 'DIS_INSOMNIA'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'PLASTICITY') {{
          const set = new Set([
            'REC_NMDA', 'REC_AMPA', 'REC_MTORC1', 'REC_BDNF_TRKB', 'REC_GSK3B', 'REC_SIGMA1', 'REC_5HT1A', 'REC_5HT7', 'REC_5HT3',
            'PATH_HIPPOCAMPAL_PLASTICITY', 'PATH_PFC_CIRCUITS',
            'DRUG_ESKETAMINE', 'DRUG_LITHIUM', 'DRUG_VALPROATE', 'DRUG_VORTIOXETINE', 'DRUG_SERTRALINE',
            'DIS_MDD', 'DIS_MDSI', 'DIS_TRD', 'DIS_ALZHEIMER', 'CLS_NMDA_MODULATOR', 'CLS_SMS', 'CLS_MOOD_STABILIZER'
          ]);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'D2_D3_PARTIAL') {{
          const set = new Set(['CLS_D2_PARTIAL', 'DRUG_BREXPIPRAZOLE', 'DRUG_CARIPRAZINE', 'DRUG_ARIPIPRAZOLE', 'REC_D2', 'REC_D3', 'REC_5HT1A', 'REC_5HT2A', 'PATH_MESOLIMBIC', 'PATH_MESOCORTICAL', 'DIS_SCHIZOPHRENIA_POS', 'DIS_SCHIZOPHRENIA_NEG', 'DIS_MDD', 'DIS_TRD', 'DIS_BIPOLAR_DEP', 'DIS_BIPOLAR_MANIA']);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'SMS_VORTIO') {{
          const set = new Set(['CLS_SMS', 'DRUG_VORTIOXETINE', 'REC_SERT', 'REC_5HT1A', 'REC_5HT1B_1D', 'REC_5HT3', 'REC_5HT7', 'PATH_PFC_CIRCUITS', 'PATH_HIPPOCAMPAL_PLASTICITY', 'DIS_MDD']);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'PREGABALIN') {{
          const set = new Set(['CLS_VGCC_LIGAND', 'CLS_5HT1A_PARTIAL_ANXIOLYTIC', 'DRUG_PREGABALIN', 'DRUG_BUSPIRONE', 'DRUG_TANDOSPIRONE', 'REC_ALPHA2DELTA', 'REC_5HT1A', 'PATH_AMYGDALA_CIRCUITS', 'PATH_PAIN_PATHWAY', 'DIS_GAD', 'DIS_NEURO_PAIN']);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'MOOD') {{
          const set = new Set(['CLS_MOOD_STABILIZER', 'DRUG_LITHIUM', 'DRUG_CARBAMAZEPINE', 'DRUG_VALPROATE', 'DRUG_LAMOTRIGINE', 'DRUG_OLANZAPINE', 'DRUG_CARIPRAZINE', 'REC_VGSC', 'REC_GSK3B', 'REC_BDNF_TRKB', 'DIS_BIPOLAR_MANIA', 'DIS_BIPOLAR_DEP', 'DIS_MDSI', 'DIS_TRD']);
          filterFn = n => set.has(n.id);
        }} else if (preset === 'BZD_ANXIETY') {{
          const set = new Set(['CLS_BZD', 'DRUG_LORAZEPAM', 'DRUG_ALPRAZOLAM', 'DRUG_DIAZEPAM', 'DRUG_CLONAZEPAM', 'REC_GABAA', 'PATH_AMYGDALA_CIRCUITS', 'DIS_GAD', 'DIS_PANIC', 'SE_SEDATION', 'SE_ADDICTION_TOLERANCE']);
          filterFn = n => set.has(n.id);
        }}

        const subNodes = graphData.nodes.filter(filterFn);
        const subIds = new Set(subNodes.map(n => n.id));
        currentVisibleNodeIds = subIds;
        const subEdges = graphData.edges.filter(e => subIds.has(e.from) && subIds.has(e.to));

        nodesDataSet.clear();
        edgesDataSet.clear();
        nodesDataSet.add(subNodes);
        edgesDataSet.add(subEdges);
        network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
        document.getElementById('mode-text').innerText = '专题透视视图';
        if (subNodes.length > 0) focusNode(subNodes[0].id);
      }});
    }});

    // 布局切换
    document.getElementById('btn-layout-force').addEventListener('click', function() {{
      document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      network.setOptions({{
        layout: {{ hierarchical: {{ enabled: false }} }},
        physics: {{ enabled: true, solver: 'barnesHut' }}
      }});
      network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
    }});

    document.getElementById('btn-layout-hier').addEventListener('click', function() {{
      document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      network.setOptions({{
        layout: {{
          hierarchical: {{
            enabled: true,
            direction: 'UD',
            sortMethod: 'directed',
            nodeSpacing: 180,
            levelSeparation: 150
          }}
        }},
        physics: {{ enabled: false }}
      }});
      network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
    }});

    document.getElementById('btn-layout-cluster').addEventListener('click', function() {{
      document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const categories = ['Receptor', 'Drug', 'DrugClass', 'Pathway', 'Disease', 'SideEffect'];
      const radii = {{ 'Receptor': 220, 'Drug': 420, 'DrugClass': 560, 'Pathway': 680, 'Disease': 820, 'SideEffect': 920 }};
      const catGroups = {{}};
      categories.forEach(c => catGroups[c] = []);
      graphData.nodes.forEach(n => {{
        if (currentVisibleNodeIds.has(n.id) && catGroups[n.category]) catGroups[n.category].push(n);
      }});

      const positioned = [];
      categories.forEach(cat => {{
        const group = catGroups[cat] || [];
        const r = radii[cat] || 450;
        const total = group.length;
        group.forEach((node, idx) => {{
          const angle = (idx / (total || 1)) * 2 * Math.PI;
          positioned.push({{
            id: node.id,
            x: r * Math.cos(angle),
            y: r * Math.sin(angle),
            physics: false
          }});
        }});
      }});
      network.setOptions({{ layout: {{ hierarchical: {{ enabled: false }} }}, physics: {{ enabled: false }} }});
      nodesDataSet.update(positioned);
      network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
    }});

    document.getElementById('btn-zoom-fit').addEventListener('click', () => network.fit({{ animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }} }}));
    document.getElementById('reset-filter-btn').addEventListener('click', () => {{
      document.querySelectorAll('.filter-item').forEach(f => f.classList.remove('active'));
      document.querySelector('[data-preset="INITIAL_SEED"]').click();
    }});
  </script>
</body>
</html>
'''
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding="utf-8")
        return output_path
