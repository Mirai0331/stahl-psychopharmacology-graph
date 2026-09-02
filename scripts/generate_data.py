# -*- coding: utf-8 -*-
"""《Stahl 精神药理学精要 (第5版)》全景图谱数据：规范中国内地官方商品名、沃诺雷生、地达西尼(京诺宁®)、全套临床药理结构化详情"""
import json
from pathlib import Path

TARGET_JSON = Path(__file__).resolve().parent.parent / "src" / "stahl_document_ai" / "processors" / "graph_data.json"

# ==========================================
# 1. 全书受体、离子通道、转运体与分子靶点 (Receptors & Targets)
# ==========================================
receptors = [
    # 多巴胺受体与转运体
    {"id": "REC_D2", "label": "D2 多巴胺受体 (D2)", "category": "Receptor", "description": "【受体类型】Gi蛋白偶联受体。\n【生理功能】抑制腺苷酸环化酶，调节运动协调、奖赏强化与催乳素分泌。\n【药理意义】抗精神病药主要治疗靶点。中脑边缘通路阻断抗阳性症状；黑质纹状体阻断>80%诱发锥体外系反应 (EPS)；结节漏斗阻断致高催乳素血症。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_D3", "label": "D3 多巴胺受体 (D3)", "category": "Receptor", "description": "【受体类型】Gi蛋白偶联受体。\n【分布特征】高表达于边缘岛、伏隔核与前额叶皮质。\n【药理意义】优先调节认知、社交动机与心境。卡利拉嗪 (Vraylar) 对 D3 具有超高亲和力（D3>D2 达10倍），显著改善精神分裂症阴性症状与认知缺陷。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_D1", "label": "D1 多巴胺受体 (D1)", "category": "Receptor", "description": "【受体类型】Gs蛋白偶联受体。\n【生理功能】前额叶锥体细胞高表达，介导工作记忆与执行功能调谐。\n【药理意义】呈现典型的“倒 U 型”反应曲线，适度 D1 激活提升前额叶网络信噪比与注意力聚焦。", "properties": {"type": "GPCR_Gs"}},
    {"id": "REC_DAT", "label": "DAT (DA 转运体)", "category": "Receptor", "description": "【靶点类型】12次跨膜单胺再摄取泵。\n【生理功能】快速回收突触间隙多巴胺至胞浆。\n【药理意义】中枢兴奋剂（赖右苯丙胺、哌甲酯）、SNDRI（托鲁地文拉法辛）与 NDRI（安非他酮）核心抑制靶点，提升突触间隙 DA 浓度以改善动机与专注。", "properties": {"type": "Transporter"}},
    {"id": "REC_VMAT2", "label": "VMAT2 (囊泡单胺转运体 2)", "category": "Receptor", "description": "【靶点类型】囊泡膜单胺转运蛋白。\n【生理功能】将胞浆内的单胺递质转运装载入突触囊泡。\n【药理意义】伐苯那嗪 (Ingrezza) 高选择性抑制 VMAT2 治疗迟发性运动障碍 (TD)；中枢兴奋剂可逆转其转运方向促进单胺释放。", "properties": {"type": "Transporter"}},

    # 5-HT 受体与转运体
    {"id": "REC_5HT1A", "label": "5-HT1A 受体", "category": "Receptor", "description": "【受体类型】Gi蛋白偶联受体（胞体树突自身受体 & 突触后受体）。\n【生理功能】降低神经元放电，抗焦虑、抗抑郁，上调海马 BDNF/TrkB 表达。\n【药理意义】丁螺环酮、坦度螺酮部分激动发挥平稳抗焦虑；布瑞哌唑、阿立哌唑激动发挥抗抑郁增效。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_5HT1B_1D", "label": "5-HT1B/1D 自身受体", "category": "Receptor", "description": "【受体类型】突触前轴突末梢自身受体。\n【药理意义】阻断解除负反馈刹车，爆发性促进 5-HT 释放。伏硫西汀 (心达悦®) 靶向调节该受体以增强抗抑郁疗效。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_5HT2A", "label": "5-HT2A 受体", "category": "Receptor", "description": "【受体类型】Gq蛋白偶联受体。\n【药理意义】非典型抗精神病药关键靶点。拮抗 5-HT2A 解除对多巴胺释放的刹车，降低 EPS、改善阴性症状并提升慢波睡眠。", "properties": {"type": "GPCR_Gq"}},
    {"id": "REC_5HT2A_INVERSE", "label": "5-HT2A 反向激动位点", "category": "Receptor", "description": "【受体类型】构象特异性 GPCR 反向激动结合位点。\n【药理意义】匹莫范色林 (Nuplazid) 高特异性结合，下调受体基底内在活性，特异性治疗帕金森病精神病 (PDP) 且不损害多巴胺运动功能。", "properties": {"type": "GPCR_Conformation"}},
    {"id": "REC_5HT2C", "label": "5-HT2C 受体", "category": "Receptor", "description": "【受体类型】Gq蛋白偶联受体。\n【生理功能】抑制前额叶多巴胺与去甲肾上腺素释放，抑制食欲。\n【药理意义】拮抗 5-HT2C 脱抑制促进前额叶 DA/NE 释放（阿戈美拉汀、米氮平、氟西汀），抗抑郁但易增加食欲与体重。", "properties": {"type": "GPCR_Gq"}},
    {"id": "REC_5HT3", "label": "5-HT3 受体 (配体门控离子通道)", "category": "Receptor", "description": "【受体类型】5-HT 受体家族中唯一的配体门控阳离子通道。\n【生理功能】介导恶心呕吐与抑制神经递质释放。\n【药理意义】伏硫西汀强效拮抗 5-HT3，脱抑制促进乙酰胆碱、多巴胺、去甲肾上腺素及组胺释放，显著增强长时程增强 (LTP) 与认知功能。", "properties": {"type": "IonChannel"}},
    {"id": "REC_5HT7", "label": "5-HT7 受体", "category": "Receptor", "description": "【受体类型】Gs蛋白偶联受体。\n【生理功能】调节昼夜生物节律与突触重塑。\n【药理意义】拮抗显著增强海马树突分支与突触可塑性，改善抑郁伴随的认知迟滞（伏硫西汀、鲁拉西酮靶向）。", "properties": {"type": "GPCR_Gs"}},
    {"id": "REC_SERT", "label": "SERT (5-HT 转运体)", "category": "Receptor", "description": "【靶点类型】5-HT 再摄取泵。\n【药理意义】SSRI/SNRI/SNDRI 核心靶点。抑制 SERT 提高突触间隙 5-HT 浓度，长期作用驱动海马神经新生与神经可塑性修复。", "properties": {"type": "Transporter"}},

    # 去甲肾上腺素受体与转运体
    {"id": "REC_NET", "label": "NET (NE 转运体)", "category": "Receptor", "description": "【靶点类型】NE 再摄取泵。\n【生理特征】在前额叶皮质中由于 DAT 表达极低，NET 同时负责回收 NE 与 DA。\n【药理意义】SNRI、SNDRI、NDRI 及托莫西汀抑制 NET，在前额叶同步提升 NE 与 DA，增强注意聚焦与精力。", "properties": {"type": "Transporter"}},
    {"id": "REC_ALPHA1", "label": "α1 肾上腺素受体", "category": "Receptor", "description": "【受体类型】Gq蛋白偶联受体。\n【药理意义】外周阻断引起直立性低血压；中枢哌唑嗪阻断可平息蓝斑核过度放电，特异性消除 PTSD 创伤性噩梦与过度觉醒。", "properties": {"type": "GPCR_Gq"}},
    {"id": "REC_ALPHA2A", "label": "α2A 肾上腺素受体", "category": "Receptor", "description": "【受体类型】Gi蛋白偶联受体。\n【生理功能】前额叶锥体细胞突触后受体，抑制 cAMP-HCN 通路关闭，强化突触连接。\n【药理意义】胍法辛高亲和力激动 α2A，增强前额叶信号信噪比，改善 ADHD 注意力缺陷与执行功能。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_BETA_ADRENERGIC", "label": "β 肾上腺素受体 (β1/β2)", "category": "Receptor", "description": "【受体类型】Gs蛋白偶联受体。\n【药理意义】介导心悸手抖等躯体焦虑；普萘洛尔阻断该受体可阻断杏仁核恐惧记忆再巩固，缓解 PTSD 与社交焦虑。", "properties": {"type": "GPCR_Gs"}},

    # TAAR1 受体
    {"id": "REC_TAAR1", "label": "TAAR1 (微量胺相关受体 1)", "category": "Receptor", "description": "【受体类型】突触前细胞内 GPCR 靶点。\n【药理意义】乌洛他隆 (Ulotaront) 激动 TAAR1，通过细胞内级联负反馈抑制多巴胺神经元过度放电，不阻断突触后 D2，抗精神病且完全无 EPS、催乳素升高与代谢紊乱。", "properties": {"type": "GPCR_Gs_Gq"}},

    # GABA 受体全谱
    {"id": "REC_GABAA", "label": "GABA-A 受体 (氯离子通道)", "category": "Receptor", "description": "【受体类型】五聚体配体门控氯离子通道。\n【药理意义】BZD 类正向变构调节剂 (PAM) 结合位点，增加通道开放频率引起超极化，介导快速中枢镇静、抗焦虑与肌松。", "properties": {"type": "IonChannel"}},
    {"id": "REC_GABAA_ALPHA1_PARTIAL", "label": "GABA-A α1 亚型部分变构结合位点 (pPAM)", "category": "Receptor", "description": "【受体类型】α1 亚基特异性部分正向变构位点。\n【药理意义】地达西尼 (京诺宁®) 特异性结合，内在活性适中（约 40-50%），精准产生促眠效应，彻底克服了完全激动剂的过度肌松跌倒、宿醉嗜睡、反跳性失眠与依赖成瘾风险。", "properties": {"type": "IonChannel_Subunit"}},
    {"id": "REC_GABAA_NEUROSTEROID", "label": "GABA-A 神经类固醇受体 (δ 亚基)", "category": "Receptor", "description": "【受体类型】突触外高亲和力变构调节位点。\n【药理意义】佐拉诺酮 (Zurzuvae) 与别孕烷醇酮 (Zulresso) 结合，介导持续紧张性抑制 (Tonic Inhibition)，快速治愈产后抑郁 (PPD) 与重度抑郁。", "properties": {"type": "IonChannel_Extrasynaptic"}},
    {"id": "REC_GHB_GABAB", "label": "GABA-B / GHB 受体", "category": "Receptor", "description": "【受体类型】Gi偶联受体。\n【药理意义】羟丁酸钠 (Xyrem) 激动该受体，恢复并巩固深慢波睡眠，特异性消除发作性睡病猝倒发作。", "properties": {"type": "GPCR_Gi"}},

    # 谷氨酸受体、神经可塑性与激酶级联
    {"id": "REC_NMDA", "label": "NMDA 谷氨酸受体", "category": "Receptor", "description": "【受体类型】配体与电压双重门控钙离子通道。\n【药理意义】艾司氯胺酮 (速开朗®) 瞬时阻断 GABA 抑制中间神经元 NMDA 触发谷氨酸爆发；美金刚 (易倍申®) 拮抗过度兴奋毒性保护阿尔茨海默病突触。", "properties": {"type": "IonChannel"}},
    {"id": "REC_AMPA", "label": "AMPA 谷氨酸受体", "category": "Receptor", "description": "【受体类型】配体门控阳离子通道。\n【药理意义】介导快速兴奋性传递。艾司氯胺酮引起的谷氨酸爆发激活突触后 AMPA，开启 VDCC 钙内流与 mTORC1 级联，驱动突触结构再生与长时程增强 (LTP)。", "properties": {"type": "IonChannel_Plasticity"}},
    {"id": "REC_BDNF_TRKB", "label": "BDNF / TrkB 信号轴", "category": "Receptor", "description": "【靶点类型】酪氨酸激酶受体 B (TrkB) 与脑源性神经营养因子。\n【生理功能】促进神经元存活、树突分支发生、突触棘成熟。\n【药理意义】抗抑郁药物长期起效、快速抗抑郁药突触再生的终末共同通路。", "properties": {"type": "Neurotrophin_Receptor"}},
    {"id": "REC_MTORC1", "label": "mTORC1 突触蛋白合成级联", "category": "Receptor", "description": "【靶点类型】细胞内雷帕霉素靶蛋白复合物 1。\n【药理意义】快速抗抑郁核心开关。激活后迅速启动 PSD-95、GluA1 等关键突触骨架蛋白翻译，数小时内逆转突触萎缩。", "properties": {"type": "Kinase_Complex"}},
    {"id": "REC_GSK3B", "label": "GSK-3β 激酶", "category": "Receptor", "description": "【靶点类型】糖原合酶激酶 3β。\n【生理机制】过度活跃导致突触退化与神经元凋亡。\n【药理意义】碳酸锂直接竞争性抑制 GSK-3β，激活 Wnt/β-catenin 与 BDNF 转录，发挥神经保护、突触重塑与经典防自杀效应。", "properties": {"type": "Kinase_Target"}},
    {"id": "REC_SIGMA1", "label": "Sigma-1 伴侣受体", "category": "Receptor", "description": "【靶点类型】内质网分子伴侣蛋白。\n【药理意义】氟伏沙明 (兰释®)、舍曲林、右美沙芬激动 Sigma-1，促进突触可塑性、细胞自噬及减轻内质网应激炎症。", "properties": {"type": "Chaperone_Protein"}},

    # 离子通道靶点
    {"id": "REC_ALPHA2DELTA", "label": "α2δ 电压门控钙通道 (VGCC)", "category": "Receptor", "description": "【靶点类型】电压门控钙通道 α2δ 辅助亚基。\n【药理意义】普瑞巴林结合 α2δ 抑制过度钙内流，减少病理性谷氨酸、P物质释放，快速抗焦虑与缓解神经病理性疼痛。", "properties": {"type": "IonChannel_Subunit"}},
    {"id": "REC_VGSC", "label": "VGSC 电压门控钠通道", "category": "Receptor", "description": "【靶点类型】电压依赖性快速钠通道。\n【药理意义】卡马西平、拉莫三嗪使用依赖性阻断钠通道，抑制高频病理性神经元爆发放电，发挥心境稳定与抗癫痫作用。", "properties": {"type": "IonChannel"}},

    # 褪黑素、食欲素与组胺受体
    {"id": "REC_MT1_MT2", "label": "MT1 / MT2 褪黑素受体", "category": "Receptor", "description": "【受体类型】下丘脑视交叉上核 (SCN) Gi偶联受体。\n【药理意义】MT1 介导促进入睡，MT2 介导昼夜节律相位重调。阿戈美拉汀 (韦度®) 与雷美替胺激动 MT1/MT2 重塑生物钟。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_OX1R_OX2R", "label": "OX1R / OX2R 食欲素受体", "category": "Receptor", "description": "【受体类型】下丘脑觉醒中枢神经肽受体。\n【生理机制】OX2R 直接主导睡眠-觉醒开关，OX1R 调控警觉与应激。\n【药理意义】双重食欲素拮抗剂 (DORA：法赞雷生、沃诺雷生 Vorzzz、莱博雷生 达卫可®、达利雷生 Quviviq) 阻断觉醒信号，恢复生理性睡眠结构，无耐受与宿醉。", "properties": {"type": "GPCR_Trio"}},
    {"id": "REC_H1", "label": "H1 组胺受体", "category": "Receptor", "description": "【受体类型】Gq蛋白偶联受体。\n【药理意义】中枢阻断导致嗜睡、镇静、食欲亢进及代谢体重增加（低剂量多虑平催眠）。", "properties": {"type": "GPCR_Gq"}},
    {"id": "REC_HISTAMINE_H3", "label": "H3 组胺自身/异源受体", "category": "Receptor", "description": "【受体类型】突触前负反馈 Gi 偶联受体。\n【药理意义】替洛利生 (铧可思®) 拮抗/反向激动 H3 解除自身刹车，促进脑内组胺爆发释放，强效促醒并消除发作性睡病猝倒。", "properties": {"type": "GPCR_Gi"}},

    # 胆碱能与阿尔茨海默病病理靶点
    {"id": "REC_ACHE", "label": "AChE (乙酰胆碱酯酶)", "category": "Receptor", "description": "【靶点类型】胆碱能突触间隙降解酶。\n【药理意义】多奈哌齐 (安理申®)、卡巴拉汀 (艾斯能®)、加兰他敏可逆性抑制 AChE，提升脑内乙酰胆碱水平改善认知。", "properties": {"type": "Enzyme"}},
    {"id": "REC_NACHR_ALPHA4BETA2", "label": "α4β2 烟碱型乙酰胆碱受体 (nAChR)", "category": "Receptor", "description": "【靶点类型】中脑多巴胺奖赏中枢配体门控通道。\n【药理意义】伐尼克兰 (畅沛®) 高度选择性部分激动，适度释放多巴胺缓解戒断痛苦，同时阻断尼古丁结合以戒烟。", "properties": {"type": "IonChannel"}},
    {"id": "REC_M1", "label": "M1 毒蕈碱胆碱受体", "category": "Receptor", "description": "【受体类型】Gq偶联受体。\n【药理意义】皮层与海马重要认知受体；抗精神病药与三环类阻断导致口干、便秘、视物模糊及认知损害。", "properties": {"type": "GPCR_Gq"}},
    {"id": "REC_AMYLOID_BETA", "label": "Aβ 淀粉样蛋白原纤维 (Amyloid-β)", "category": "Receptor", "description": "【靶点类型】阿尔茨海默病核心毒性可溶性原纤维与沉积斑块。\n【药理意义】仑卡奈单抗 (乐意保®) 与多奈单抗 (Kisunla) 特异性结合并清除 Aβ，显著延缓阿尔茨海默病早期认知衰退进程。", "properties": {"type": "Protein_Aggregate"}},

    # 阿片受体与代谢酶
    {"id": "REC_MU_OPIOID", "label": "μ-阿片受体 (MOR)", "category": "Receptor", "description": "【受体类型】Gi蛋白偶联受体。\n【药理意义】介导镇痛与强效奖赏欣快感。丁丙诺啡部分激动用于替代维持；纳曲酮阻断防复吸；纳洛酮纯拮抗用于急性中毒解毒。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_KAPPA_OPIOID", "label": "κ-阿片受体 (KOR)", "category": "Receptor", "description": "【受体类型】Gi偶联受体。\n【药理意义】介导戒断烦躁负性情绪。丁丙诺啡拮抗 κ-受体产生抗抑郁与防复吸协同效应。", "properties": {"type": "GPCR_Gi"}},
    {"id": "REC_ALDH", "label": "ALDH (乙醛脱氢酶)", "category": "Receptor", "description": "【靶点类型】肝脏酒精代谢关键酶。\n【药理意义】双硫仑不可逆抑制 ALDH，饮酒后乙醛剧烈蓄积诱发面红恶心胸闷厌恶反应，强制戒酒。", "properties": {"type": "Enzyme"}},
]

# ==========================================
# 2. 全书神经通路与环路 (Pathways & Circuits)
# ==========================================
pathways = [
    {"id": "PATH_CIRCADIAN_SCN", "label": "视交叉上核 (SCN) 昼夜节律网络", "category": "Pathway", "description": "体内主生物钟起搏器。阿戈美拉汀 (韦度®) 通过 MT1/MT2 激动结合 5-HT2C 拮抗协同重塑昼夜生物节律，恢复慢波睡眠与情绪节律", "properties": {"neurotransmitter": "Melatonin/5-HT/GABA"}},
    {"id": "PATH_MESOLIMBIC", "label": "中脑边缘多巴胺通路 (Mesolimbic)", "category": "Pathway", "description": "从腹侧被盖区 (VTA) 至伏隔核，功能亢进介导幻觉、妄想等阳性精神病性症状", "properties": {"neurotransmitter": "Dopamine"}},
    {"id": "PATH_MESOCORTICAL", "label": "中脑皮质多巴胺通路 (Mesocortical)", "category": "Pathway", "description": "从 VTA 至前额叶皮质 (DLPFC/VMPFC)，功能低下介导阴性症状与认知缺陷", "properties": {"neurotransmitter": "Dopamine"}},
    {"id": "PATH_NIGROSTRIATAL", "label": "黑质纹状体多巴胺通路 (Nigrostriatal)", "category": "Pathway", "description": "控制运动协调，D2 阻断>80%诱发锥体外系反应 (EPS)，VMAT2 调节多巴胺囊泡释放改善迟发性运动障碍", "properties": {"neurotransmitter": "Dopamine"}},
    {"id": "PATH_TUBEROINFUNDIBULAR", "label": "结节漏斗多巴胺通路 (Tuberoinfundibular)", "category": "Pathway", "description": "多巴胺抑制垂体催乳素释放，D2 阻断导致高催乳素血症", "properties": {"neurotransmitter": "Dopamine"}},
    {"id": "PATH_PFC_CIRCUITS", "label": "前额叶皮质认知网络 (PFC Circuits)", "category": "Pathway", "description": "执行功能、工作记忆与认知注意力网络（ADHD、抑郁认知迟滞、快感缺失与突触可塑性核心）", "properties": {"neurotransmitter": "Glu/GABA/DA/NE/5-HT"}},
    {"id": "PATH_AMYGDALA_CIRCUITS", "label": "杏仁核恐惧与焦虑环路 (Amygdala Circuits)", "category": "Pathway", "description": "焦虑与恐惧的核心中枢，GABA-A 增强或 α2δ 钙通道阻断可平息其过度放电", "properties": {"neurotransmitter": "5-HT/GABA/Glu"}},
    {"id": "PATH_CSTC_LOOPS", "label": "皮质-纹状体-丘脑-皮质 (CSTC) 环路", "category": "Pathway", "description": "强迫障碍 (OCD) 与冲动控制的核心环路，调节闯入性思维、仪式动作与习惯化行为（氟伏沙明/氯米帕明靶向）", "properties": {"neurotransmitter": "5-HT/Glu/DA/GABA"}},
    {"id": "PATH_FEAR_EXTINCTION", "label": "前额叶-杏仁核恐惧消退网络 (Fear Extinction)", "category": "Pathway", "description": "创伤后应激障碍 (PTSD) 核心病理环路，腹内侧前额叶无法抑制杏仁核过度恐惧反应（β阻断/α1拮抗/SSRI调控）", "properties": {"neurotransmitter": "NE/5-HT/Glu/GABA"}},
    {"id": "PATH_PAIN_PATHWAY", "label": "脊髓后角下行疼痛调制通路 (Pain Pathway)", "category": "Pathway", "description": "5-HT/NE 双重神经元自上而下抑制脊髓后角伤害性信号传导（度洛西汀/普瑞巴林/米那普仑靶向）", "properties": {"neurotransmitter": "5-HT/NE/Glu"}},
    {"id": "PATH_HYPOTHALAMIC_AROUSAL", "label": "下丘脑觉醒-睡眠节律环路 (Arousal Circuits)", "category": "Pathway", "description": "结节乳头体核与侧下丘脑食欲素/组胺觉醒系统（法赞雷生/沃诺雷生/莱博雷生/达利雷生靶向）", "properties": {"neurotransmitter": "Orexin/Histamine/GABA"}},
    {"id": "PATH_VLPO_SLEEP_SWITCH", "label": "腹外侧视前核 (VLPO) 睡眠开启中枢", "category": "Pathway", "description": "中枢睡眠开关，通过 GABA 和甘氨酸抑制脑干觉醒中心，地达西尼 (京诺宁®) 与 BZD 类协同激活促进入睡", "properties": {"neurotransmitter": "GABA/Glycine"}},
    {"id": "PATH_TMN_HISTAMINE_AROUSAL", "label": "结节乳头体核 (TMN) 组胺促醒通路", "category": "Pathway", "description": "释放组胺维持大脑皮层警觉与清醒状态，替洛利生 (铧可思®) 通过 H3 拮抗激活该通路促醒", "properties": {"neurotransmitter": "Histamine"}},
    {"id": "PATH_HIPPOCAMPAL_PLASTICITY", "label": "海马突触再生与神经可塑性环路 (Hippocampal Plasticity)", "category": "Pathway", "description": "海马齿状回 (DG) 神经新生与 CA1/CA3 树突棘重构，逆转慢性应激所致的突触丢失与脑萎缩", "properties": {"neurotransmitter": "BDNF/TrkB/Glu/5-HT"}},
    {"id": "PATH_BASAL_FOREBRAIN_ACH", "label": "基底前脑 Meynert 核胆碱能认知通路", "category": "Pathway", "description": "投射至海马与全脑皮层，维持学习、记忆与注意力（阿尔茨海默病退化核心）", "properties": {"neurotransmitter": "Acetylcholine"}},
    {"id": "PATH_VTA_NACC_REWARD", "label": "中脑腹侧被盖区-伏隔核 (VTA-NAcc) 奖赏中枢", "category": "Pathway", "description": "多巴胺奖赏强化回路，物质成瘾（酒精/尼古丁/阿片）渴求与心理依赖的核心生化基础", "properties": {"neurotransmitter": "Dopamine/Opioid/GABA"}},
]

# ==========================================
# 3. 疾病与危重/难治表型 (Diseases，中文在先，英文缩写在后)
# ==========================================
diseases = [
    {"id": "DIS_MDSI", "label": "伴急性自杀意念或行为的重度抑郁发作 (MDSI)", "category": "Disease", "description": "精神科紧急危重表型（Major Depressive Episode with Acute Suicidal Ideation or Behavior）。艾司氯胺酮 (速开朗®) 联合口服抗抑郁药可在 4~24 小时内快速缓解急性自杀意念，碳酸锂具长期防自杀效应"},
    {"id": "DIS_TRD", "label": "难治性抑郁障碍 (TRD)", "category": "Disease", "description": "对≥2种不同机制足量足疗程抗抑郁药应答不佳的难治状态（Treatment-Resistant Depression）。艾司氯胺酮 (速开朗®)、SNDRI 托鲁地文拉法辛 (若欣林®)、Auvelity、D2/D3 部分激动剂（布瑞哌唑 敏达妥®、阿立哌唑）、喹硫平、锂盐增效为关键方案"},
    {"id": "DIS_MDD", "label": "抑郁障碍 (Depressive Disorders)", "category": "Disease", "description": "情绪低落、快感缺失 (Anhedonia)、精力减退、认知执行功能障碍及海马突触萎缩"},
    {"id": "DIS_PPD", "label": "产后抑郁障碍 (PPD)", "category": "Disease", "description": "产后神经类固醇急剧骤降导致 GABA-A 受体失调的特异表型，佐拉诺酮 (Zurzuvae) 与别孕烷醇酮 (Zulresso) 靶向快速显效"},

    {"id": "DIS_SCHIZOPHRENIA_POS", "label": "精神分裂症阳性症状 (Positive Symptoms)", "category": "Disease", "description": "幻觉、妄想、瓦解性言语与行为（D2 阻断/TAAR1 调节）"},
    {"id": "DIS_SCHIZOPHRENIA_NEG", "label": "精神分裂症阴性与认知症状 (Negative/Cognitive)", "category": "Disease", "description": "情感淡漠、社交退缩、执行功能损害（卡利拉嗪 D3/布瑞哌唑/乌洛他隆优势）"},
    {"id": "DIS_PDP", "label": "帕金森病精神病 (PDP)", "category": "Disease", "description": "帕金森患者多巴胺替代治疗后诱发的幻觉妄想，匹莫范色林 (Nuplazid) 5-HT2A 反向激动特异性治疗且不损害运动功能"},

    {"id": "DIS_BIPOLAR_MANIA", "label": "双相情感障碍躁狂发作 (Bipolar Mania)", "category": "Disease", "description": "心境高涨、夸大、思维奔逸、冲动（锂盐/卡马西平/丙戊酸/非典型抗精神病药一线）"},
    {"id": "DIS_BIPOLAR_DEP", "label": "双相抑郁发作 (Bipolar Depression)", "category": "Disease", "description": "双相障碍抑郁期，需防止转躁（卡利拉嗪/卢美哌隆 Caplyta/喹硫平/拉莫三嗪一线）"},

    {"id": "DIS_GAD", "label": "广泛性焦虑障碍 (GAD)", "category": "Disease", "description": "过度担忧、紧张自主神经亢进（普瑞巴林/丁螺环酮/SSRI/SNRI/BZD）"},
    {"id": "DIS_PANIC", "label": "惊恐障碍 (Panic Disorder)", "category": "Disease", "description": "急性突发惊恐发作与濒死感（阿普唑仑/氯硝西泮/SSRI）"},
    {"id": "DIS_SAD", "label": "社交焦虑障碍 (SAD)", "category": "Disease", "description": "社交场合强烈恐惧回避，普萘洛尔缓解躯体震颤心悸，SSRI/SNRI 长期治疗"},
    {"id": "DIS_PTSD", "label": "创伤后应激障碍 (PTSD)", "category": "Disease", "description": "创伤再体验、噩梦、警觉过高与恐惧消退障碍（舍曲林/哌唑嗪/普萘洛尔）"},
    {"id": "DIS_OCD", "label": "强迫障碍 (OCD)", "category": "Disease", "description": "强迫思维与强迫仪式动作，CSTC 环路功能失调（氟伏沙明 兰释®/高剂量 SSRI/氯米帕明一线）"},

    {"id": "DIS_INSOMNIA", "label": "失眠障碍 (Insomnia)", "category": "Disease", "description": "入睡困难与睡眠维持困难（地达西尼 京诺宁®/法赞雷生/沃诺雷生 Vorzzz/莱博雷生 达卫可®/达利雷生/阿戈美拉汀靶向）"},
    {"id": "DIS_NARCOLEPSY", "label": "发作性睡病与猝倒症 (Narcolepsy)", "category": "Disease", "description": "下丘脑食欲素神经元丢失所致日间不可抗拒睡眠与情绪诱发猝倒（莫达非尼/替洛利生 铧可思®/羟丁酸钠）"},

    {"id": "DIS_ADHD", "label": "注意力缺陷多动障碍 (ADHD)", "category": "Disease", "description": "注意力不集中、多动与冲动（赖右苯丙胺（利右苯丙胺）/哌甲酯 专注达®/托莫西汀 择思达®/胍法辛/维洛沙嗪 Qelbree）"},
    {"id": "DIS_NEURO_PAIN", "label": "神经病理性疼痛与纤维肌痛 (Neuropathic Pain)", "category": "Disease", "description": "带状疱疹后神经痛、糖尿病周围神经痛、纤维肌痛中枢敏化（普瑞巴林/度洛西汀/米那普仑）"},
    {"id": "DIS_ALZHEIMER", "label": "阿尔茨海默病与认知障碍 (Alzheimer's Disease)", "category": "Disease", "description": "进行性记忆力减退、定向力障碍与突触退行性损害（多奈哌齐 安理申®/卡巴拉汀 艾斯能®/美金刚 易倍申®/仑卡奈单抗 乐意保®）"},
    {"id": "DIS_TD", "label": "迟发性运动障碍 (TD)", "category": "Disease", "description": "长期使用抗精神病药后多巴胺受体超敏导致的不自主口面部及肢体舞蹈样运动（VMAT2 抑制剂伐苯那嗪 欣维妥® 治疗）"},

    {"id": "DIS_AUD", "label": "酒精使用障碍 (AUD / 酒精依赖)", "category": "Disease", "description": "慢性强迫性饮酒、耐受与戒断反应（纳曲酮/阿坎酸/双硫仑）"},
    {"id": "DIS_OUD", "label": "阿片类物质使用障碍 (OUD / 阿片依赖与急救)", "category": "Disease", "description": "阿片类药物成瘾依赖与急性中毒呼吸抑制（美沙酮/丁丙诺啡维持，纳洛酮急救解毒）"},
    {"id": "DIS_TOBACCO", "label": "烟草依赖与戒烟 (Tobacco / Nicotine Dependence)", "category": "Disease", "description": "尼古丁成瘾与戒断焦虑（伐尼克兰 畅沛®/安非他酮）"},

    # 不良反应
    {"id": "SE_EPS", "label": "锥体外系反应 (EPS)", "category": "SideEffect", "description": "急性肌张力障碍、静坐不能、类帕金森综合征（D2 阻断>80%）"},
    {"id": "SE_METABOLIC", "label": "代谢综合征 (Metabolic Syndrome)", "category": "SideEffect", "description": "体重显著增加、高血糖、血脂异常（H1/5-HT2C 强阻断诱发）"},
    {"id": "SE_HYPERPROLACTIN", "label": "高催乳素血症 (Hyperprolactinemia)", "category": "SideEffect", "description": "催乳素升高、溢乳、月经紊乱、性功能障碍（结节漏斗 D2 阻断）"},
    {"id": "SE_SEDATION", "label": "嗜睡与过度镇静 (Sedation)", "category": "SideEffect", "description": "日间警觉性下降、困倦（H1/α1/GABA-A 增强诱发）"},
    {"id": "SE_ADDICTION_TOLERANCE", "label": "耐受与依赖风险 (Tolerance & Dependence)", "category": "SideEffect", "description": "中枢兴奋剂与 BZD 类需评估耐受、成瘾与戒断风险（赖右苯丙胺通过前药机制降低滥用倾向，地达西尼 京诺宁® 通过部分变构极大降低成瘾）"},
    {"id": "SE_ANTICHOLINERGIC", "label": "抗胆碱能不良反应 (Anticholinergic Effects)", "category": "SideEffect", "description": "口干、视物模糊、便秘、嗜睡与认知障碍（M1 受体强阻断诱发）"},
    {"id": "SE_ORTHOSTATIC_HYPOTENSION", "label": "直立性低血压与头晕 (Orthostatic Hypotension)", "category": "SideEffect", "description": "体位改变时血压急剧下降、头晕、反射性心动过速（α1 肾上腺素受体阻断诱发）"},
]

# ==========================================
# 4. 药物大类 (Drug Classes)
# ==========================================
drug_classes = [
    # 精神分裂症与精神病
    {"id": "CLS_FGA", "label": "第一代典型抗精神病药 (FGA)", "category": "DrugClass", "description": "强效阻断 D2 受体，如氟哌啶醇、氯丙嗪，抗阳性症状确切但 EPS 与催乳素升高风险高"},
    {"id": "CLS_SDA", "label": "第二代非典型抗精神病药 (SDA / 5-HT2A-D2 拮抗)", "category": "DrugClass", "description": "5-HT2A/D2 拮抗剂（如奥氮平、利培酮、喹硫平、氯氮平、卢美哌隆 Caplyta）"},
    {"id": "CLS_D2_PARTIAL", "label": "D2/D3 部分激动剂 (SDAM / DPA)", "category": "DrugClass", "description": "多巴胺活性稳定器（阿立哌唑、布瑞哌唑 敏达妥®、卡利拉嗪 Vraylar）"},
    {"id": "CLS_TAAR1_AGONIST", "label": "TAAR1 激动剂与非 D2 阻断抗精神病药 (TAAR1 Agonists)", "category": "DrugClass", "description": "乌洛他隆 (Ulotaront)，不阻断突触后 D2，通过突触前 TAAR1 调谐单胺与谷氨酸，无 EPS 及代谢副作用"},
    {"id": "CLS_5HT2A_INVERSE", "label": "5-HT2A 反向激动剂 (5-HT2A Inverse Agonists)", "category": "DrugClass", "description": "匹莫范色林 (Nuplazid)，高选择性反向激动 5-HT2A，特异性治疗帕金森病精神病 (PDP)"},

    # 抗抑郁药
    {"id": "CLS_SSRI", "label": "选择性 5-HT 再摄取抑制剂 (SSRI)", "category": "DrugClass", "description": "一线抗抑郁抗焦虑药（氟西汀、舍曲林、艾司西酞普兰、氟伏沙明 兰释®），长期使用上调 BDNF"},
    {"id": "CLS_SNRI", "label": "5-HT / NE 双重再摄取抑制剂 (SNRI)", "category": "DrugClass", "description": "双通道提升单胺（文拉法辛、度洛西汀、米那普仑）"},
    {"id": "CLS_SNDRI", "label": "5-HT / NE / DA 三重再摄取抑制剂 (SNDRI / TRI)", "category": "DrugClass", "description": "三重单胺再摄取抑制剂。同步抑制 SERT、NET 和 DAT，改善快感缺失与疲乏（托鲁地文拉法辛 若欣林®）"},
    {"id": "CLS_NDRI", "label": "NE / DA 双重再摄取抑制剂 (NDRI)", "category": "DrugClass", "description": "安非他酮 (Bupropion)，抑制 DAT 与 NET，抗抑郁、戒烟，无体重增加与性功能障碍"},
    {"id": "CLS_SMS", "label": "5-HT 多模式调节剂 (SMS)", "category": "DrugClass", "description": "再摄取抑制 + 多重 5-HT 受体变构调节，强效增强突触可塑性（伏硫西汀 心达悦®）"},
    {"id": "CLS_SPARI", "label": "5-HT 再摄取抑制与 5-HT1A 部分激动剂 (SPARI)", "category": "DrugClass", "description": "维拉佐酮 (Viibryd)，快速抗抑郁且较少性功能副作用"},
    {"id": "CLS_MASSA", "label": "褪黑素受体激动与 5-HT2C 拮抗剂 (MASSA)", "category": "DrugClass", "description": "褪黑素能与单胺能协同抗抑郁药，激活 MT1/MT2 并拮抗 5-HT2C（阿戈美拉汀 韦度®）"},
    {"id": "CLS_GABAA_NEUROSTEROID_PAM", "label": "GABA-A 神经类固醇受体正向变构调节剂 (Neurosteroids)", "category": "DrugClass", "description": "佐拉诺酮 (Zurzuvae) 与别孕烷醇酮 (Zulresso)，靶向突触外 δ-GABA-A 受体，快速治疗产后与重度抑郁"},
    {"id": "CLS_DXM_BUP", "label": "NMDA 拮抗与单胺调节复方 (Auvelity)", "category": "DrugClass", "description": "右美沙芬-安非他酮复方 (Auvelity)，口服快速起效抗抑郁突破药"},
    {"id": "CLS_NMDA_MODULATOR", "label": "NMDA 调节与突触再生剂 (NMDA Modulators)", "category": "DrugClass", "description": "艾司氯胺酮 (速开朗®，激活 AMPA/mTOR 快速突触再生、治疗 TRD 与 MDSI)、美金刚 (易倍申®，阿尔茨海默病神经保护)"},
    {"id": "CLS_TCA", "label": "三环类抗抑郁药 (TCA)", "category": "DrugClass", "description": "阿米替林、氯米帕明，强效抑制再摄取但受体广泛阻断"},

    # 心境稳定剂
    {"id": "CLS_MOOD_STABILIZER", "label": "心境稳定剂 (Mood Stabilizers)", "category": "DrugClass", "description": "锂盐、抗癫痫钠通道调节剂（卡马西平、丙戊酸钠、拉莫三嗪），通过抑制 GSK-3β 促进突触保护与防自杀"},

    # 焦虑、睡眠与镇静
    {"id": "CLS_GABAA_PARTIAL_PAM", "label": "GABA-A 受体部分正向变构调节剂 (Partial PAM / 半激动剂)", "category": "DrugClass", "description": "地达西尼 (京诺宁®)，高选择性结合 α1 亚基部分激活，精准助眠且无肌无力、宿醉与反跳成瘾"},
    {"id": "CLS_VGCC_LIGAND", "label": "α2δ 钙通道配体 (加巴喷丁类 / VGCC)", "category": "DrugClass", "description": "普瑞巴林 (Pregabalin)、加巴喷丁 (Gabapentin)，抑制突触前钙内流抗焦虑与镇痛"},
    {"id": "CLS_BZD", "label": "苯二氮䓬类药物 (BZD / GABA-A PAM)", "category": "DrugClass", "description": "GABA-A 正向变构调节剂 (劳拉西泮、阿普唑仑、地西泮、氯硝西泮)"},
    {"id": "CLS_5HT1A_PARTIAL_ANXIOLYTIC", "label": "5-HT1A 部分激动抗焦虑剂 (Azapirones)", "category": "DrugClass", "description": "丁螺环酮 (Buspirone)、坦度螺酮 (律康®)，无镇静肌松成瘾"},
    {"id": "CLS_DORA", "label": "双重食欲素受体拮抗剂 (DORA / 双食欲素拮抗)", "category": "DrugClass", "description": "靶向阻断 OX1R 和 OX2R 受体，生理性诱导入睡与睡眠维持（法赞雷生、沃诺雷生 Vorzzz、莱博雷生 达卫可®、达利雷生 Quviviq）"},

    # 促醒与发作性睡病
    {"id": "CLS_WAKE_PROMOTING", "label": "中枢促醒剂 (Wake-Promoting Agents)", "category": "DrugClass", "description": "莫达非尼 (Provigil)、阿莫达非尼 (Nuvigil)，弱 DAT 抑制促醒"},
    {"id": "CLS_H3_ANTAGONIST", "label": "H3 组胺受体拮抗/反向激动剂 (H3 Antagonists)", "category": "DrugClass", "description": "替洛利生 (铧可思®)，促进脑内组胺释放促醒"},
    {"id": "CLS_GABAB_GHB", "label": "GABA-B / GHB 受体激动剂", "category": "DrugClass", "description": "羟丁酸钠 (Xyrem)，重塑慢波睡眠治疗发作性睡病猝倒"},

    # ADHD 药物
    {"id": "CLS_ADHD_STIMULANT", "label": "ADHD 中枢兴奋剂与前药 (Stimulants)", "category": "DrugClass", "description": "阻断/逆转 DAT 与 NET（赖右苯丙胺（利右苯丙胺） Vyvanse、哌甲酯 专注达®）"},
    {"id": "CLS_ADHD_NON_STIMULANT", "label": "ADHD 非中枢兴奋剂 (Non-Stimulants)", "category": "DrugClass", "description": "选择性 NET 抑制 (托莫西汀 择思达®、维洛沙嗪 Qelbree) 或 α2A 激动 (胍法辛)"},

    # 痴呆与认知
    {"id": "CLS_ACHEI", "label": "乙酰胆碱酯酶抑制剂 (AChEI)", "category": "DrugClass", "description": "多奈哌齐 (安理申®)、卡巴拉汀 (艾斯能®)、加兰他敏 (Galantamine)"},
    {"id": "CLS_ANTI_AMYLOID_MAB", "label": "抗 Aβ 淀粉样蛋白单克隆抗体 (Anti-Aβ mAbs)", "category": "DrugClass", "description": "仑卡奈单抗 (乐意保®)、多奈单抗 (Kisunla)，清除脑内 Aβ 原纤维延缓阿尔茨海默病进展"},

    # 成瘾与运动障碍
    {"id": "CLS_ADDICTION_TREATMENT", "label": "物质成瘾与戒断治疗药 (Addiction Therapeutics)", "category": "DrugClass", "description": "伐尼克兰 (畅沛® 戒烟)、纳曲酮 (戒酒/戒阿片)、阿坎酸 (戒酒维持)、双硫仑、丁丙诺啡、纳洛酮 (急救)"},
    {"id": "CLS_VMAT2_INHIBITOR", "label": "VMAT2 抑制剂 (囊泡单胺转运体抑制)", "category": "DrugClass", "description": "伐苯那嗪 (欣维妥®)，靶向治疗迟发性运动障碍 (TD)"},
]

# ==========================================
# 5. 代表性精神药物 (全套结构化详细药理信息)
# ==========================================
drugs = [
    # 精神分裂症与抗精神病药
    {"id": "DRUG_HALOPERIDOL", "label": "氟哌啶醇 (Haloperidol)", "category": "Drug", "description": "【药物分类】第一代典型抗精神病药 (FGA)。\n【药理机制】高选择性超强阻断中脑边缘 D2 受体 (Ki=0.7nM)。\n【适应症】精神分裂症急性阳性兴奋、幻觉妄想及抽动秽语综合征。\n【临床特点】抗幻觉妄想迅速强效，但易诱发严重锥体外系反应 (EPS) 及高催乳素血症。"},
    {"id": "DRUG_CLOZAPINE", "label": "氯氮平 (Clozapine)", "category": "Drug", "description": "【药物分类】第二代非典型抗精神病药 (SDA)。\n【药理机制】5-HT2A/D2/5-HT1A/H1/M1/α1 多受体拮抗，D2 快解离。\n【适应症】难治性精神分裂症治疗黄金标准与自杀风险干预。\n【临床优势与警戒】极低 EPS 且不升高催乳素，但需严格定期监测粒细胞缺乏症、心肌炎及代谢综合征。"},
    {"id": "DRUG_OLANZAPINE", "label": "奥氮平 (Olanzapine / 再普乐®)", "category": "Drug", "description": "【药物分类】第二代非典型抗精神病药 (SDA)。\n【药理机制】强效拮抗 5-HT2A、D2、5-HT2C、H1 及 M1 受体。\n【适应症】精神分裂症、双相情感障碍急性躁狂发作及预防复发。\n【临床特点】镇静助眠起效快，抗精神病与抗躁狂确切；但 H1/5-HT2C 强阻断导致体重增加与代谢综合征风险高。"},
    {"id": "DRUG_RISPERIDONE", "label": "利培酮 (Risperidone / 维思通®)", "category": "Drug", "description": "【药物分类】第二代非典型抗精神病药 (SDA)。\n【药理机制】极高亲和力拮抗 5-HT2A (Ki=0.17nM) 与 D2 (Ki=3.7nM) 及 α1。\n【适应症】精神分裂症、双相躁狂及孤独症易激惹。\n【临床特点】抗阳性症状确切，但高剂量时对 D2 阻断率高，易诱发 EPS 与高催乳素血症。"},
    {"id": "DRUG_QUETIAPINE", "label": "喹硫平 (Quetiapine / 思瑞康®)", "category": "Drug", "description": "【药物分类】广谱多靶点非典型抗精神病药。\n【药理机制】D2 快解离弱拮抗；活性代谢产物去甲基喹硫平强效抑制 NET 并部分激动 5-HT1A，同时强阻断 H1/5-HT2A。\n【适应症】精神分裂症、双相情感障碍（单药获批躁狂与抑郁）及难治性抑郁 (TRD) 辅助增效。\n【临床特点】EPS 风险极低，镇静助眠效果显著。"},
    {"id": "DRUG_ARIPIPRAZOLE", "label": "阿立哌唑 (Aripiprazole / 安律凡®)", "category": "Drug", "description": "【药物分类】多巴胺受体部分激动剂 (DPA / SDAM)。\n【药理机制】D2 部分激动（内在活性约30%）+ 5-HT1A 部分激动 + 5-HT2A 拮抗。\n【适应症】精神分裂症、双相障碍及抑郁障碍一线辅助增效。\n【临床优势】多巴胺系统“双向调节稳定器”，不引起催乳素升高与镇静，代谢中性。"},
    {"id": "DRUG_BREXPIPRAZOLE", "label": "布瑞哌唑 (Brexpiprazole / 敏达妥® / Rexulti)", "category": "Drug", "description": "【药物分类】新一代 5-HT-DA 活性调节剂 (SDAM)。\n【药理机制】D2 部分激动（内在活性较阿立哌唑更低，静坐不能风险极低）+ 强效 5-HT1A 部分激动 + 5-HT2A 拮抗。\n【适应症】精神分裂症及难治性抑郁障碍 (TRD) 一线增效。\n【临床优势】改善抑郁心境与认知，极少发生镇静、催乳素升高与 EPS。"},
    {"id": "DRUG_CARIPRAZINE", "label": "卡利拉嗪 (Cariprazine / 罗珊® / Vraylar / Reagila)", "category": "Drug", "description": "【药物分类】D3 偏好型 D3/D2 多巴胺部分激动剂。\n【药理机制】对 D3 亲和力是 D2 的 10 倍 (Ki=0.085nM)，同时激动 5-HT1A。\n【适应症】精神分裂症（尤其阴性症状与认知缺陷优势）、双相 I 型抑郁与躁狂发作。\n【临床优势】显著改善精神分裂症情感淡漠与执行功能损害，超长半衰期活性代谢物保证平稳疗效。"},
    {"id": "DRUG_LUMATEPERONE", "label": "卢美哌隆 (Lumateperone / Caplyta)", "category": "Drug", "description": "【药物分类】全新多靶点非典型抗精神病药。\n【药理机制】超高亲和力拮抗 5-HT2A (比 D2 强 60 倍) + 突触后特异性 D2 磷酸化调控 + SERT 抑制 + 激活 AMPA/NMDA。\n【适应症】精神分裂症及双相 I/II 型抑郁障碍（单药及联合锂盐/丙戊酸）。\n【临床优势】代谢中性（完全不增加体重、血糖与血脂），无 EPS 与催乳素升高，心血管安全性卓越。"},
    {"id": "DRUG_PIMAVANSERIN", "label": "匹莫范色林 (Pimavanserin / Nuplazid)", "category": "Drug", "description": "【药物分类】选择性 5-HT2A 反向激动剂。\n【药理机制】高特异性反向激动 5-HT2A 受体，完全不结合 D2、组胺或胆碱能受体。\n【适应症】帕金森病精神病 (PDP) 幻觉妄想。\n【临床优势】特异性平息精神病性症状，彻底杜绝了传统抗精神病药导致的帕金森运动症状恶化。"},
    {"id": "DRUG_ULOTARONT", "label": "乌洛他隆 (Ulotaront)", "category": "Drug", "description": "【药物分类】首创新机制 TAAR1 激动剂 (非 D2 阻断型抗精神病药)。\n【药理机制】激动细胞内微量胺受体 1 (TAAR1) 与 5-HT1A，通过突触前调谐抑制多巴胺过度放电，完全不阻断突触后 D2 受体。\n【适应症】精神分裂症阳性与阴性症状。\n【临床突破】从机制根源消除锥体外系反应 (EPS)、高催乳素血症与代谢综合征。"},

    # 抗抑郁药
    {"id": "DRUG_FLUOXETINE", "label": "氟西汀 (Fluoxetine / 百优解®)", "category": "Drug", "description": "【药物分类】选择性 5-HT 再摄取抑制剂 (SSRI)。\n【药理机制】抑制 SERT，兼具弱 5-HT2C 拮抗脱抑制促进前额叶 DA/NE 释放。\n【适应症】抑郁障碍、强迫障碍、神经性贪食症。\n【临床特点】半衰期长，赋能激活效应明显，适合伴精神运动性迟滞患者。"},
    {"id": "DRUG_SERTRALINE", "label": "舍曲林 (Sertraline / 左洛复®)", "category": "Drug", "description": "【药物分类】选择性 5-HT 再摄取抑制剂 (SSRI)。\n【药理机制】抑制 SERT，兼具弱 DAT 抑制与强 Sigma-1 伴侣受体激动。\n【适应症】抑郁障碍、广泛性焦虑、惊恐障碍、创伤后应激障碍 (PTSD) 一线。\n【临床特点】心血管安全性极高，促进神经突触可塑性。"},
    {"id": "DRUG_ESCITALOPRAM", "label": "艾司西酞普兰 (Escitalopram / 来士普®)", "category": "Drug", "description": "【药物分类】高选择性变构 SSRI。\n【药理机制】纯变构抑制 SERT，高特异性增加 5-HT。\n【适应症】抑郁障碍、广泛性焦虑障碍 (GAD) 一线。\n【临床特点】起效平稳迅速，药物相互作用极小，耐受性优异。"},
    {"id": "DRUG_FLUVOXAMINE", "label": "氟伏沙明 (Fluvoxamine / 兰释®)", "category": "Drug", "description": "【药物分类】选择性 5-HT 再摄取抑制剂 (SSRI)。\n【药理机制】强效抑制 SERT，兼具超强亲和力激动 Sigma-1 受体 (Ki=36nM)。\n【适应症】强迫障碍 (OCD) 指南首选一线药、抑郁障碍。\n【临床优势】显著调控 CSTC 强迫环路，抗炎及抗内质网应激突触损伤。"},
    {"id": "DRUG_VENLAFAXINE", "label": "文拉法辛 (Venlafaxine / 怡诺思®)", "category": "Drug", "description": "【药物分类】5-HT / NE 双重再摄取抑制剂 (SNRI)。\n【药理机制】低剂量抑制 SERT，中高剂量同步强效抑制 NET。\n【适应症】抑郁障碍、广泛性焦虑障碍、社交焦虑障碍。\n【临床特点】双通道提升单胺，改善精力减退、动力缺乏与注意涣散。"},
    {"id": "DRUG_DULOXETINE", "label": "度洛西汀 (Duloxetine / 欣百达®)", "category": "Drug", "description": "【药物分类】5-HT / NE 双重再摄取抑制剂 (SNRI)。\n【药理机制】全剂量范围内均衡抑制 SERT 与 NET，激活下行镇痛通路。\n【适应症】抑郁障碍、广泛性焦虑、糖尿病周围神经痛及慢性肌肉骨骼疼痛。\n【临床特点】抗抑郁与缓解躯体疼痛双重获益。"},
    {"id": "DRUG_MIRTAZAPINE", "label": "米氮平 (Mirtazapine / 瑞美隆®)", "category": "Drug", "description": "【药物分类】去甲肾上腺素能与特异性 5-HT 能抗抑郁药 (NaSSA)。\n【药理机制】拮抗突触前 α2 自调节受体脱抑制促单胺释放 + 阻断 5-HT2A/5-HT2C/H1。\n【适应症】伴显著失眠、食欲下降及消瘦的抑郁障碍。\n【临床特点】强效镇静助眠与增进食欲，完全无性功能副作用与胃肠道恶心。"},
    {"id": "DRUG_VORTIOXETINE", "label": "伏硫西汀 (Vortioxetine / 心达悦® / Brintellix)", "category": "Drug", "description": "【药物分类】5-HT 多模式调节剂 (SMS)。\n【药理机制】抑制 SERT + 全激动 5-HT1A + 部分激动 5-HT1B/1D + 强拮抗 5-HT3 与 5-HT7。\n【适应症】抑郁障碍（尤其伴认知损害、工作记忆减退者）。\n【临床优势】直接增强海马 LTP 长时程增强与突触再生，显著改善抑郁相关执行功能损害。"},
    {"id": "DRUG_VILAZODONE", "label": "维拉佐酮 (Vilazodone / Viibryd)", "category": "Drug", "description": "【药物分类】5-HT 再摄取抑制与 5-HT1A 部分激动剂 (SPARI)。\n【药理机制】高亲和力抑制 SERT 同时部分激动突触后 5-HT1A 受体。\n【适应症】成人抑郁障碍。\n【临床特点】起效较快，性功能障碍与体重增加发生率极低。"},
    {"id": "DRUG_TOLUDESVENLAFAXINE", "label": "托鲁地文拉法辛 (Toludesvenlafaxine / 若欣林®)", "category": "Drug", "description": "【药物分类】中国首创 1 类创新药，三重单胺再摄取抑制剂 (SNDRI / TRI)。\n【药理机制】同时高亲和力抑制 SERT、NET 及 DAT 再摄取。\n【适应症】抑郁障碍、难治性抑郁 (TRD)。\n【临床优势】全面突破单/双通道瓶颈，显著攻克快感缺失 (Anhedonia)、疲乏迟滞与认知减退。"},
    {"id": "DRUG_AGOMELATINE", "label": "阿戈美拉汀 (Agomelatine / 韦度® / Valdoxan)", "category": "Drug", "description": "【药物分类】褪黑素受体激动与 5-HT2C 拮抗剂 (MASSA)。\n【药理机制】激动视交叉上核 (SCN) MT1/MT2 重塑生物钟 + 拮抗 5-HT2C 脱抑制促进前额叶 DA/NE 释放。\n【适应症】抑郁障碍伴睡眠节律紊乱。\n【临床优势】重塑昼夜生理节律，无撤药反应，完全无性功能副作用与体重增加。"},
    {"id": "DRUG_BUPROPION", "label": "安非他酮 (Bupropion / 悦亭® / Wellbutrin)", "category": "Drug", "description": "【药物分类】去甲肾上腺素-多巴胺再摄取抑制剂 (NDRI)。\n【药理机制】选择性抑制 DAT 与 NET，兼具烟碱受体拮抗。\n【适应症】抑郁障碍、烟草依赖戒烟。\n【临床优势】改善疲劳、嗜睡与精力缺乏，完全无性功能损害与体重增加风险。"},
    {"id": "DRUG_AUVELITY", "label": "右美沙芬-安非他酮 (Auvelity)", "category": "Drug", "description": "【药物分类】首个口服快速起效谷氨酸-单胺复方抗抑郁药。\n【药理机制】右美沙芬非竞争性拮抗 NMDA 受体并激动 Sigma-1；安非他酮抑制 CYP2D6 提升其血药浓度并抑制 NET/DAT。\n【适应症】重度抑郁障碍、难治性抑郁 (TRD)。\n【临床突破】打破 4~6 周起效延迟，口服 1 周内快速显著改善抑郁症状。"},
    {"id": "DRUG_ZURANOLONE", "label": "佐拉诺酮 (Zuranolone / Zurzuvae)", "category": "Drug", "description": "【药物分类】首个口服 GABA-A 神经类固醇正向变构调节剂。\n【药理机制】特异性作用于突触外 δ 亚基 GABA-A 受体，重建紧张性神经抑制平衡。\n【适应症】产后抑郁障碍 (PPD)、重度抑郁障碍。\n【临床突破】每日 1 次口服仅需 14 天短程治疗，快速且持久缓解产后抑郁与绝望。"},
    {"id": "DRUG_BREXANOLONE", "label": "别孕烷醇酮 (Brexanolone / Zulresso)", "category": "Drug", "description": "【药物分类】内源性神经类固醇静脉注射制剂。\n【药理机制】正向变构调节突触内外 GABA-A 受体。\n【适应症】重度产后抑郁障碍 (PPD)。\n【临床特点】60 小时持续静脉滴注特异性快速逆转产后急性抑郁危机。"},
    {"id": "DRUG_ESKETAMINE", "label": "艾司氯胺酮 (Esketamine / 速开朗® / Spravato)", "category": "Drug", "description": "【药物分类】NMDA 受体非竞争性拮抗剂 (快速突触再生剂)。\n【药理机制】阻断 GABA 抑制中间神经元 NMDA 触发谷氨酸爆发，激活突触后 AMPA，开启 mTORC1 级联并上调 BDNF/TrkB，数小时内驱动树突棘突触再生。\n【适应症】伴急性自杀意念或行为的重度抑郁发作 (MDSI)、难治性抑郁 (TRD)。\n【临床突破】鼻喷给药 4~24 小时内快速阻断急性自杀冲动，突破传统抗抑郁瓶颈。"},
    {"id": "DRUG_CLOMIPRAMINE", "label": "氯米帕明 (Clomipramine / 安拿芬尼®)", "category": "Drug", "description": "【药物分类】三环类抗抑郁药 (TCA)。\n【药理机制】对 SERT 具有极高抑制亲和力，强效提升 5-HT。\n【适应症】强迫障碍 (OCD) 经典二线特效药、抑郁障碍。\n【临床注意】受体阻断广泛，需注意抗胆碱能口干便秘与心脏传导阻滞。"},

    # 心境稳定剂
    {"id": "DRUG_LITHIUM", "label": "碳酸锂 (Lithium)", "category": "Drug", "description": "【药物分类】经典一线心境稳定剂。\n【药理机制】直接抑制 GSK-3β 激酶与肌醇单磷酸酶 (IMPase)，激活 Wnt 与 BDNF/TrkB 突触保护通路。\n【适应症】双相障碍躁狂发作、双相维持期预防复发、抑郁发作防自杀 (MDSI) 及难治抑郁 (TRD) 增效。\n【临床优势与警戒】循证证实显著降低自杀率与突触退化；需定期监测血锂浓度（治疗窗 0.6~1.2 mmol/L）、肾功与甲状腺。"},
    {"id": "DRUG_VALPROATE", "label": "丙戊酸钠 (Valproate / 德巴金®)", "category": "Drug", "description": "【药物分类】广谱抗躁狂心境稳定剂与抗癫痫药。\n【药理机制】抑制 GSK-3β、阻断钠通道、抑制 HDAC 组蛋白去乙酰化酶并促进 GABA 合成。\n【适应症】双相情感障碍急性躁狂发作。\n【临床特点】急性抗躁狂起效迅速；育龄期女性需警惕致畸风险。"},
    {"id": "DRUG_CARBAMAZEPINE", "label": "卡马西平 (Carbamazepine / 得理多®)", "category": "Drug", "description": "【药物分类】使用依赖性钠通道阻滞心境稳定剂。\n【药理机制】延缓失活状态 VGSC 钠通道恢复，抑制病理性高频放电。\n【适应症】双相急性躁狂发作、三叉神经痛。\n【临床特点】经典一线抗躁狂；需监测 CYP3A4 自我诱导与过敏皮疹 (HLA-B*1502)。"},
    {"id": "DRUG_LAMOTRIGINE", "label": "拉莫三嗪 (Lamotrigine / 利必通®)", "category": "Drug", "description": "【药物分类】突触前谷氨酸释放抑制剂。\n【药理机制】使用依赖性抑制电压门控钠通道，特异性减少病理性谷氨酸释放。\n【适应症】双相障碍抑郁发作的长期预防复发一线。\n【临床特点】预防双相抑郁复发优势显著，需缓慢滴定剂量以防重症药疹。"},

    # 焦虑、睡眠与催眠新药 (地达西尼 京诺宁®)
    {"id": "DRUG_DIMDAZENIL", "label": "地达西尼 (Dimdazenil / 京诺宁®)", "category": "Drug", "description": "【药物分类】中国首个自主研发 1 类 GABA-A 受体部分正向变构调节剂 (pPAM / 半激动剂)。\n【药理机制】高选择性作用于 GABA-A 受体 α1 亚型，发挥适度的部分正向变构调节（最大内在活性约 40-50%），温和促使 Cl- 内流。\n【适应症】失眠障碍（入睡困难与睡眠维持障碍）。\n【临床突破】既能快速诱导并维持生理性睡眠，又彻底克服了传统完全激动剂导致的过度肌松跌倒风险、记忆受损、宿醉嗜睡、反跳性失眠与依赖成瘾性。"},
    {"id": "DRUG_PREGABALIN", "label": "普瑞巴林 (Pregabalin / 乐瑞卡®)", "category": "Drug", "description": "【药物分类】α2δ 电压门控钙通道配体 (加巴喷丁类)。\n【药理机制】高亲和力结合突触前 α2δ 亚基，抑制过度钙内流与兴奋性递质释放。\n【适应症】广泛性焦虑障碍 (GAD) 一线、周围神经病理性疼痛与纤维肌痛。\n【临床优势】快速平息杏仁核焦虑放电，改善睡眠质量，起效迅速且无性功能副作用。"},
    {"id": "DRUG_BUSPIRONE", "label": "丁螺环酮 (Buspirone)", "category": "Drug", "description": "【药物分类】5-HT1A 受体部分激动剂 (Azapirones)。\n【药理机制】选择性部分激动突触前自身与突触后 5-HT1A 受体。\n【适应症】广泛性焦虑障碍 (GAD) 一线。\n【临床优势】无镇静嗜睡、无肌松、无共济失调，完全无依赖耐受与戒断反跳。"},
    {"id": "DRUG_TANDOSPIRONE", "label": "坦度螺酮 (Tandospirone / 律康®)", "category": "Drug", "description": "【药物分类】高选择性 5-HT1A 受体部分激动剂。\n【药理机制】调节 5-HT 神经传递平衡，平复边缘系统自主神经亢进。\n【适应症】广泛性焦虑、躯体化障碍伴焦虑。\n【临床特点】显著改善心身躯体化症状，无依赖成瘾。"},
    {"id": "DRUG_PROPRANOLOL", "label": "普萘洛尔 (Propranolol / 心得安®)", "category": "Drug", "description": "【药物分类】非选择性 β-受体阻滞剂。\n【药理机制】阻断中枢与外周 β1/β2 受体，抑制肾上腺素能过度激活。\n【适应症】社交焦虑障碍（表演型）、PTSD 恐惧记忆再巩固阻断、抗精神病药静坐不能。\n【临床特点】迅速平息心悸、手抖、出汗等自主神经躯体焦虑。"},
    {"id": "DRUG_PRAZOSIN", "label": "哌唑嗪 (Prazosin)", "category": "Drug", "description": "【药物分类】中枢 α1-肾上腺素受体拮抗剂。\n【药理机制】特异性阻断中枢 α1 受体，平息蓝斑核夜间过度去甲肾上腺素风暴。\n【适应症】创伤后应激障碍 (PTSD) 创伤性噩梦与过度警觉。\n【临床优势】显著减少创伤相关噩梦，改善睡眠连续性。"},
    {"id": "DRUG_LORAZEPAM", "label": "劳拉西泮 (Lorazepam / 罗拉®)", "category": "Drug", "description": "【药物分类】中效苯二氮䓬类 (BZD)。\n【药理机制】增强 GABA-A 受体介导的氯离子内流。\n【适应症】急性焦虑发作、失眠短期治疗、紧张症。\n【临床特点】直接经葡萄糖醛酸化代谢，无活性代谢产物，老年及肝功不全者相对安全。"},
    {"id": "DRUG_ALPRAZOLAM", "label": "阿普唑仑 (Alprazolam / 佳静安定®)", "category": "Drug", "description": "【药物分类】短中效高亲和力苯二氮䓬类 (BZD)。\n【药理机制】高亲和力正向变构调节 GABA-A 受体。\n【适应症】惊恐障碍急性发作、重度焦虑状态。\n【临床特点】抗惊恐起效极快，需注意避免长期使用引起药物依赖。"},
    {"id": "DRUG_DIAZEPAM", "label": "地西泮 (Diazepam / 安定®)", "category": "Drug", "description": "【药物分类】长效经典苯二氮䓬类 (BZD)。\n【药理机制】广谱正向变构调节 GABA-A 受体。\n【适应症】焦虑症、癫痫持续状态急救、中枢性肌痉挛。\n【临床特点】抗惊厥与肌松作用强，代谢产物半衰期长。"},
    {"id": "DRUG_CLONAZEPAM", "label": "氯硝西泮 (Clonazepam)", "category": "Drug", "description": "【药物分类】长效高亲和力苯二氮䓬类 (BZD)。\n【药理机制】强效增强 GABA-A 抑制信号。\n【适应症】惊恐障碍、快动眼睡眠行为障碍 (RBD)、难治性癫痫。\n【临床特点】抗惊厥与抗惊恐效力极强。"},

    # 睡眠障碍 DORA 四大代表药与促醒药
    {"id": "DRUG_FAZAMOREXANT", "label": "法赞雷生 (Fazamorexant)", "category": "Drug", "description": "【药物分类】中国首个自主研发 1 类双重食欲素受体拮抗剂 (DORA)。\n【药理机制】高亲和力双重阻断下丘脑 OX1R 与 OX2R 促觉醒信号通路。\n【适应症】失眠障碍（入睡困难与睡眠维持障碍）。\n【临床优势】恢复生理性正常睡眠结构，不改变 REM/慢波睡眠比例，无依赖性、耐受性与次日宿醉残留。"},
    {"id": "DRUG_VORNOREXANT", "label": "沃诺雷生 (Vornorexant / Vorzzz)", "category": "Drug", "description": "【药物分类】新一代超快解离型双重食欲素受体拮抗剂 (DORA)。\n【药理机制】快速阻断 OX1R 和 OX2R，半衰期短且快解离动力学。\n【适应症】失眠障碍。\n【临床突破】既能迅速促进入睡与延长总睡眠，清晨血药浓度又极速清除，实现“次日清晨零残留嗜睡”，显著提升日间精力。"},
    {"id": "DRUG_LEMBOREXANT", "label": "莱博雷生 (Lemborexant / 达卫可® / Dayvigo)", "category": "Drug", "description": "【药物分类】第二代双重食欲素受体拮抗剂 (DORA)。\n【药理机制】特异性阻断 OX1R 和 OX2R，关闭觉醒驱动中枢。\n【适应症】失眠障碍（入睡困难与睡眠维持障碍）。\n【临床优势】显著缩短入睡潜伏期并减少中途醒来次数，次日宿醉极低且无依赖成瘾。"},
    {"id": "DRUG_DARIDOREXANT", "label": "达利雷生 (Daridorexant / Quviviq)", "category": "Drug", "description": "【药物分类】优化半衰期双重食欲素受体拮抗剂 (DORA)。\n【药理机制】阻断 OX1R 和 OX2R，设计半衰期约 8 小时。\n【适应症】成人慢性失眠障碍。\n【临床突破】改善夜间睡眠质量的同时，三期临床明确证实显著提升日间功能与精力。"},
    {"id": "DRUG_RAMELTEON", "label": "雷美替胺 (Ramelteon / 柔速瑞® / Rozerem)", "category": "Drug", "description": "【药物分类】高选择性 MT1/MT2 褪黑素受体激动剂。\n【药理机制】高选择性激动下丘脑视交叉上核 MT1 与 MT2 受体。\n【适应症】入睡困难型失眠障碍。\n【临床优势】生理性诱导睡眠，非管制药物，完全无成瘾依赖与反跳性失眠。"},
    {"id": "DRUG_MODAFINIL", "label": "莫达非尼 (Modafinil / 保卫达® / Provigil)", "category": "Drug", "description": "【药物分类】非兴奋剂类中枢促醒药。\n【药理机制】选择性弱阻断 DAT，激活下丘脑食欲素与组胺神经元促醒通路。\n【适应症】发作性睡病日间过度嗜睡 (EDS)、轮班工作睡眠障碍一线。\n【临床优势】强效促醒，不引起外周心血管交感过度兴奋，滥用潜能低。"},
    {"id": "DRUG_ARMODAFINIL", "label": "阿莫达非尼 (Armodafinil / Nuvigil)", "category": "Drug", "description": "【药物分类】长效单一 R-异构体中枢促醒药。\n【药理机制】选择性抑制 DAT 维持皮层多巴胺稳态。\n【适应症】发作性睡病日间过度嗜睡。\n【临床特点】消除半衰期更长，全天候平稳维持日间警觉性。"},
    {"id": "DRUG_PITOLISANT", "label": "替洛利生 (Pitolisant / 铧可思® / Wakix)", "category": "Drug", "description": "【药物分类】首创新机制 H3 组胺受体拮抗/反向激动剂。\n【药理机制】高选择性阻断突触前 H3 自身受体 (Ki=0.16nM)，脱抑制促进脑内组胺爆发释放。\n【适应症】发作性睡病成人及儿童日间过度嗜睡 (EDS) 或猝倒症。\n【临床突破】首个非中枢管制类促醒与抗猝倒药，显著改善日间嗜睡并减少猝倒发作。"},
    {"id": "DRUG_SODIUM_OXYBATE", "label": "羟丁酸钠 (Sodium Oxybate / Xyrem)", "category": "Drug", "description": "【药物分类】GABA-B / GHB 受体激动剂。\n【药理机制】激动 GABA-B 与 GHB 特异性受体，强化夜间深慢波睡眠。\n【适应症】发作性睡病猝倒症及日间过度嗜睡。\n【临床突破】发作性睡病猝倒特效药，重塑夜间睡眠架构从根源消除白天猝倒。"},

    # ADHD 药物
    {"id": "DRUG_LISDEXAMFETAMINE", "label": "赖右苯丙胺（利右苯丙胺） (Lisdexamfetamine / 维凡斯® / Vyvanse)", "category": "Drug", "description": "【药物分类】苯丙胺类前药中枢兴奋剂。\n【药理机制】经红细胞代谢水解平稳释放右苯丙胺，阻断并逆转 DAT、NET 与 VMAT2。\n【适应症】注意力缺陷多动障碍 (ADHD) 一线、成人中重度暴食障碍。\n【临床突破】14 小时全天候平稳疗效，前药机制彻底杜绝鼻吸与注射滥用可能。"},
    {"id": "DRUG_METHYLPHENIDATE", "label": "哌甲酯 (Methylphenidate / 专注达® / Concerta)", "category": "Drug", "description": "【药物分类】中枢兴奋剂。\n【药理机制】选择性阻断 DAT 与 NET 再摄取转运体。\n【适应症】儿童与成人注意力缺陷多动障碍 (ADHD) 一线。\n【临床特点】渗透泵控释剂型维持 12 小时平稳血药浓度，改善注意力与多动冲动。"},
    {"id": "DRUG_ATOMOXETINE", "label": "托莫西汀 (Atomoxetine / 择思达® / Strattera)", "category": "Drug", "description": "【药物分类】选择性去甲肾上腺素再摄取抑制剂 (NRI)。\n【药理机制】高选择性阻断 NET，在前额叶同步提升 NE 与 DA 水平。\n【适应症】ADHD 一线非兴奋剂治疗。\n【临床优势】非中枢兴奋剂，无滥用潜能与依赖风险，适合共病焦虑抽动者。"},
    {"id": "DRUG_GUANFACINE", "label": "胍法辛 (Guanfacine / 罗瓦西® / Intuniv)", "category": "Drug", "description": "【药物分类】选择性突触后 α2A 受体激动剂。\n【药理机制】高选择性激动前额叶突触后 α2A 受体，强化树突棘神经网络连接。\n【适应症】儿童与青少年 ADHD 非兴奋剂一线。\n【临床特点】直接增强前额叶执行控制网络，改善冲动攻击与注意力缺陷。"},
    {"id": "DRUG_VILOXAZINE", "label": "维洛沙嗪 (Viloxazine / Qelbree)", "category": "Drug", "description": "【药物分类】新型多靶点非兴奋剂 ADHD 治疗药。\n【药理机制】选择性抑制 NET 兼具 5-HT2B 拮抗与 5-HT7 激动。\n【适应症】儿童与成人 ADHD。\n【临床优势】起效较传统非兴奋剂更快，全面调谐前额叶注意网络，无成瘾依赖。"},

    # 痴呆与认知障碍
    {"id": "DRUG_DONEPEZIL", "label": "多奈哌齐 (Donepezil / 安理申® / Aricept)", "category": "Drug", "description": "【药物分类】高选择性可逆乙酰胆碱酯酶抑制剂 (AChEI)。\n【药理机制】特异性抑制 AChE 水解，提高脑内胆碱能传递水平。\n【适应症】轻、中、重度阿尔茨海默病认知损害一线。\n【临床优势】每日一次给药，显著改善患者认知、日常自理能力与行为。"},
    {"id": "DRUG_RIVASTIGMINE", "label": "卡巴拉汀 (Rivastigmine / 艾斯能® / Exelon)", "category": "Drug", "description": "【药物分类】双重胆碱酯酶抑制剂 (AChEI & BuChEI)。\n【药理机制】假性不可逆同时抑制 AChE 与丁酰胆碱酯酶 (BuChE)。\n【适应症】阿尔茨海默病及帕金森病痴呆 (PDD) 一线。\n【临床优势】透皮贴剂给药血药浓度极其平稳，极大减轻胃肠道恶心副反应。"},
    {"id": "DRUG_GALANTAMINE", "label": "加兰他敏 (Galantamine / 希普斯® / Reminyl)", "category": "Drug", "description": "【药物分类】AChE 抑制剂兼烟碱受体变构增强剂。\n【药理机制】竞争性抑制 AChE + 变构增强 α4β2 烟碱型乙酰胆碱受体敏感性。\n【适应症】轻中度阿尔茨海默病认知损害。\n【临床特点】双重协同机制放大内源性胆碱能神经信号。"},
    {"id": "DRUG_MEMANTINE", "label": "美金刚 (Memantine / 易倍申® / Ebixa / Namenda)", "category": "Drug", "description": "【药物分类】中等亲和力非竞争性 NMDA 受体拮抗剂。\n【药理机制】阻断病理性低浓度持续性谷氨酸兴奋毒性，保护残存突触结构，同时保留生理性 LTP 学习记忆信号。\n【适应症】中重度阿尔茨海默病一线。\n【临床优势】神经保护延缓痴呆进展，常与多奈哌齐联合增效。"},
    {"id": "DRUG_LECANEMAB", "label": "仑卡奈单抗 (Lecanemab / 乐意保® / Leqembi)", "category": "Drug", "description": "【药物分类】突破性抗 Aβ 疾病修饰单克隆抗体 (DMT)。\n【药理机制】特异性高亲和力结合并清除脑内最具毒性的 Aβ 可溶性原纤维。\n【适应症】早期阿尔茨海默病（轻度认知障碍 MCI 及轻度痴呆期）。\n【临床里程碑】全球三期临床证实减缓早期阿尔茨海默病认知衰退 27%，改变疾病病程。"},
    {"id": "DRUG_DONANEMAB", "label": "多奈单抗 (Donanemab / Kisunla)", "category": "Drug", "description": "【药物分类】靶向已沉积斑块的抗 Aβ 疾病修饰单抗。\n【药理机制】特异性结合脑内 N3pG-Aβ 淀粉样沉积斑块，驱动巨噬清除。\n【适应症】早期阿尔茨海默病。\n【临床突破】实现脑内淀粉样斑块深度清除，显著延缓临床痴呆进展。"},

    # 物质成瘾与运动障碍
    {"id": "DRUG_VARENICLINE", "label": "伐尼克兰 (Varenicline / 畅沛® / Champix)", "category": "Drug", "description": "【药物分类】α4β2 烟碱型乙酰胆碱受体高选择性部分激动剂。\n【药理机制】部分激动 α4β2（40-60%内在活性）适度释放多巴胺缓解戒断痛苦，同时竞争性阻断尼古丁结合消除吸烟欣快感。\n【适应症】烟草依赖戒烟指南首选一线药。\n【临床优势】显著提升长期戒烟成功率，戒烟疗效优于安非他酮与尼古丁贴片。"},
    {"id": "DRUG_NALTREXONE", "label": "纳曲酮 (Naltrexone / 维威妥® / Vivitrol / ReVia)", "category": "Drug", "description": "【药物分类】长效口服与长效注射纯 μ-阿片受体拮抗剂。\n【药理机制】阻断 μ-阿片受体，切断酒精与阿片刺激中脑 VTA 释放多巴胺的奖赏强化回路。\n【适应症】酒精使用障碍 (AUD) 戒酒、阿片类依赖戒断后防复吸。\n【临床优势】显著减少重度饮酒天数与复饮率。"},
    {"id": "DRUG_ACAMPROSATE", "label": "阿坎酸 (Acamprosate / 坎普拉® / Campral)", "category": "Drug", "description": "【药物分类】NMDA / GABA 神经传递平衡调节剂。\n【药理机制】抑制慢性酒精戒断引起的高谷氨酸兴奋毒性，增强 GABA 抑制。\n【适应症】酒精依赖完全戒断后的长期维持治疗。\n【临床优势】帮助维持长期戒酒状态，完全不经肝脏代谢（肾排泄），肝功能受损者安全。"},
    {"id": "DRUG_DISULFIRAM", "label": "双硫仑 (Disulfiram / 戒酒硫® / Antabuse)", "category": "Drug", "description": "【药物分类】乙醛脱氢酶 (ALDH) 不可逆抑制剂。\n【药理机制】抑制 ALDH 阻断酒精氧化代谢，导致体内乙醛急剧蓄积。\n【适应症】酒精依赖心理厌恶疗法。\n【临床特点】服药后饮酒迅速诱发剧烈面红、头痛、心悸、恶心胸闷厌恶反应，强制戒酒。"},
    {"id": "DRUG_BUPRENORPHINE", "label": "丁丙诺啡 (Buprenorphine / 塞宝松® / Suboxone)", "category": "Drug", "description": "【药物分类】μ-阿片受体部分激动剂与 κ-受体拮抗剂。\n【药理机制】慢解离高亲和力部分激动 μ 受体（内在活性低），拮抗 κ 受体。\n【适应症】阿片类物质使用障碍 (OUD) 替代维持治疗一线。\n【临床优势】具备呼吸抑制天花板效应，安全性极高，消除戒断症状且无剧烈欣快。"},
    {"id": "DRUG_NALOXONE", "label": "纳洛酮 (Naloxone / 纳洛酮® / Narcan)", "category": "Drug", "description": "【药物分类】纯 μ-阿片受体竞争性强效拮抗剂。\n【药理机制】超高亲和力竞争性置换结合于 μ 受体的外源性阿片分子。\n【适应症】急性阿片类药物中毒过量呼吸抑制急救特效解毒剂。\n【临床特点】脂溶性高迅速穿透血脑屏障，数分钟内逆转呼吸抑制抢救生命。"},
    {"id": "DRUG_VALBENAZINE", "label": "伐苯那嗪 (Valbenazine / 欣维妥® / Ingrezza)", "category": "Drug", "description": "【药物分类】高选择性囊泡单胺转运体 2 (VMAT2) 抑制剂。\n【药理机制】高选择性抑制 VMAT2，减少突触前多巴胺囊泡装载与释放，降低突触间隙多巴胺信号。\n【适应症】抗精神病药所致迟发性运动障碍 (TD)、亨廷顿舞蹈病。\n【临床突破】FDA 批准首个 TD 靶向特效治疗药，显著改善不自主口面部及肢体异常运动。"},
]

all_nodes = receptors + pathways + diseases + drug_classes + drugs

# ==========================================
# 6. 机制连线三元组 (Edges)
# ==========================================
edges_raw = [
    # --- 类别归属 (IS_A) ---
    ("DRUG_HALOPERIDOL", "CLS_FGA", "IS_A", "属于", "", 1.0),
    ("DRUG_CLOZAPINE", "CLS_SDA", "IS_A", "属于", "", 1.0),
    ("DRUG_OLANZAPINE", "CLS_SDA", "IS_A", "属于", "", 1.0),
    ("DRUG_RISPERIDONE", "CLS_SDA", "IS_A", "属于", "", 1.0),
    ("DRUG_QUETIAPINE", "CLS_SDA", "IS_A", "属于", "", 1.0),
    ("DRUG_LUMATEPERONE", "CLS_SDA", "IS_A", "属于", "新型5-HT2A高选择性SDA", 1.0),
    ("DRUG_ARIPIPRAZOLE", "CLS_D2_PARTIAL", "IS_A", "属于", "", 1.0),
    ("DRUG_BREXPIPRAZOLE", "CLS_D2_PARTIAL", "IS_A", "属于", "", 1.0),
    ("DRUG_CARIPRAZINE", "CLS_D2_PARTIAL", "IS_A", "属于", "", 1.0),
    ("DRUG_ULOTARONT", "CLS_TAAR1_AGONIST", "IS_A", "属于", "首创新机制TAAR1激动剂", 1.0),
    ("DRUG_PIMAVANSERIN", "CLS_5HT2A_INVERSE", "IS_A", "属于", "5-HT2A反向激动剂代表", 1.0),

    ("DRUG_FLUOXETINE", "CLS_SSRI", "IS_A", "属于", "", 1.0),
    ("DRUG_SERTRALINE", "CLS_SSRI", "IS_A", "属于", "", 1.0),
    ("DRUG_ESCITALOPRAM", "CLS_SSRI", "IS_A", "属于", "", 1.0),
    ("DRUG_FLUVOXAMINE", "CLS_SSRI", "IS_A", "属于", "", 1.0),
    ("DRUG_VENLAFAXINE", "CLS_SNRI", "IS_A", "属于", "", 1.0),
    ("DRUG_DULOXETINE", "CLS_SNRI", "IS_A", "属于", "", 1.0),
    ("DRUG_MIRTAZAPINE", "CLS_SNRI", "IS_A", "归类", "NaSSA单胺增强", 1.0),
    ("DRUG_TOLUDESVENLAFAXINE", "CLS_SNDRI", "IS_A", "属于", "中国首创1类SNDRI新药", 1.0),
    ("DRUG_BUPROPION", "CLS_NDRI", "IS_A", "属于", "NDRI代表药", 1.0),
    ("DRUG_VORTIOXETINE", "CLS_SMS", "IS_A", "属于", "", 1.0),
    ("DRUG_VILAZODONE", "CLS_SPARI", "IS_A", "属于", "", 1.0),
    ("DRUG_AGOMELATINE", "CLS_MASSA", "IS_A", "属于", "", 1.0),
    ("DRUG_AUVELITY", "CLS_DXM_BUP", "IS_A", "属于", "口服快速起效复方", 1.0),
    ("DRUG_ZURANOLONE", "CLS_GABAA_NEUROSTEROID_PAM", "IS_A", "属于", "口服神经类固醇新药", 1.0),
    ("DRUG_BREXANOLONE", "CLS_GABAA_NEUROSTEROID_PAM", "IS_A", "属于", "静脉神经类固醇", 1.0),
    ("DRUG_ESKETAMINE", "CLS_NMDA_MODULATOR", "IS_A", "属于", "", 1.0),
    ("DRUG_CLOMIPRAMINE", "CLS_TCA", "IS_A", "属于", "", 1.0),

    ("DRUG_LITHIUM", "CLS_MOOD_STABILIZER", "IS_A", "属于", "", 1.0),
    ("DRUG_VALPROATE", "CLS_MOOD_STABILIZER", "IS_A", "属于", "", 1.0),
    ("DRUG_CARBAMAZEPINE", "CLS_MOOD_STABILIZER", "IS_A", "属于", "", 1.0),
    ("DRUG_LAMOTRIGINE", "CLS_MOOD_STABILIZER", "IS_A", "属于", "", 1.0),

    ("DRUG_DIMDAZENIL", "CLS_GABAA_PARTIAL_PAM", "IS_A", "属于", "中国首创 1 类 GABA-A 部分变构催眠药", 1.0),
    ("DRUG_PREGABALIN", "CLS_VGCC_LIGAND", "IS_A", "属于", "", 1.0),
    ("DRUG_BUSPIRONE", "CLS_5HT1A_PARTIAL_ANXIOLYTIC", "IS_A", "属于", "", 1.0),
    ("DRUG_TANDOSPIRONE", "CLS_5HT1A_PARTIAL_ANXIOLYTIC", "IS_A", "属于", "", 1.0),
    ("DRUG_LORAZEPAM", "CLS_BZD", "IS_A", "属于", "", 1.0),
    ("DRUG_ALPRAZOLAM", "CLS_BZD", "IS_A", "属于", "", 1.0),
    ("DRUG_DIAZEPAM", "CLS_BZD", "IS_A", "属于", "", 1.0),
    ("DRUG_CLONAZEPAM", "CLS_BZD", "IS_A", "属于", "", 1.0),

    ("DRUG_FAZAMOREXANT", "CLS_DORA", "IS_A", "属于", "中国首款 1 类 DORA 双食欲素拮抗剂", 1.0),
    ("DRUG_VORNOREXANT", "CLS_DORA", "IS_A", "属于", "新一代超快解离 DORA 双食欲素拮抗剂", 1.0),
    ("DRUG_LEMBOREXANT", "CLS_DORA", "IS_A", "属于", "", 1.0),
    ("DRUG_DARIDOREXANT", "CLS_DORA", "IS_A", "属于", "", 1.0),
    ("DRUG_RAMELTEON", "CLS_MASSA", "IS_A", "属于", "褪黑素受体激动催眠", 1.0),
    ("DRUG_MODAFINIL", "CLS_WAKE_PROMOTING", "IS_A", "属于", "", 1.0),
    ("DRUG_ARMODAFINIL", "CLS_WAKE_PROMOTING", "IS_A", "属于", "", 1.0),
    ("DRUG_PITOLISANT", "CLS_H3_ANTAGONIST", "IS_A", "属于", "首创新机制H3组胺拮抗促醒", 1.0),
    ("DRUG_SODIUM_OXYBATE", "CLS_GABAB_GHB", "IS_A", "属于", "", 1.0),

    ("DRUG_LISDEXAMFETAMINE", "CLS_ADHD_STIMULANT", "IS_A", "属于", "前药中枢兴奋剂代表", 1.0),
    ("DRUG_METHYLPHENIDATE", "CLS_ADHD_STIMULANT", "IS_A", "属于", "", 1.0),
    ("DRUG_ATOMOXETINE", "CLS_ADHD_NON_STIMULANT", "IS_A", "属于", "", 1.0),
    ("DRUG_GUANFACINE", "CLS_ADHD_NON_STIMULANT", "IS_A", "属于", "", 1.0),
    ("DRUG_VILOXAZINE", "CLS_ADHD_NON_STIMULANT", "IS_A", "属于", "", 1.0),

    ("DRUG_DONEPEZIL", "CLS_ACHEI", "IS_A", "属于", "", 1.0),
    ("DRUG_RIVASTIGMINE", "CLS_ACHEI", "IS_A", "属于", "", 1.0),
    ("DRUG_GALANTAMINE", "CLS_ACHEI", "IS_A", "属于", "", 1.0),
    ("DRUG_MEMANTINE", "CLS_NMDA_MODULATOR", "IS_A", "属于", "", 1.0),
    ("DRUG_LECANEMAB", "CLS_ANTI_AMYLOID_MAB", "IS_A", "属于", "", 1.0),
    ("DRUG_DONANEMAB", "CLS_ANTI_AMYLOID_MAB", "IS_A", "属于", "", 1.0),

    ("DRUG_VARENICLINE", "CLS_ADDICTION_TREATMENT", "IS_A", "属于", "戒烟首选", 1.0),
    ("DRUG_NALTREXONE", "CLS_ADDICTION_TREATMENT", "IS_A", "属于", "戒酒戒毒", 1.0),
    ("DRUG_ACAMPROSATE", "CLS_ADDICTION_TREATMENT", "IS_A", "属于", "戒酒维持", 1.0),
    ("DRUG_DISULFIRAM", "CLS_ADDICTION_TREATMENT", "IS_A", "属于", "戒酒厌恶疗法", 1.0),
    ("DRUG_BUPRENORPHINE", "CLS_ADDICTION_TREATMENT", "IS_A", "属于", "阿片替代维持", 1.0),
    ("DRUG_NALOXONE", "CLS_ADDICTION_TREATMENT", "IS_A", "属于", "阿片急救解毒", 1.0),
    ("DRUG_VALBENAZINE", "CLS_VMAT2_INHIBITOR", "IS_A", "属于", "", 1.0),

    # --- 1. 精神分裂症与抗精神病药前沿机制 ---
    ("DRUG_HALOPERIDOL", "REC_D2", "ANTAGONIST", "强效阻断", "控制阳性症状", 2.2),
    ("DRUG_HALOPERIDOL", "REC_ALPHA1", "ANTAGONIST", "弱阻断", "轻度低血压", 1.2),
    ("DRUG_CLOZAPINE", "REC_5HT2A", "ANTAGONIST", "强效拮抗", "解除 DA 刹车", 2.0),
    ("DRUG_CLOZAPINE", "REC_D2", "ANTAGONIST", "快解离弱拮抗", "极低 EPS", 1.5),
    ("DRUG_CLOZAPINE", "REC_5HT1A", "PARTIAL_AGONIST", "部分激动", "促 DA 释放与抗抑郁", 1.2),
    ("DRUG_CLOZAPINE", "REC_H1", "ANTAGONIST", "强阻断", "镇静与食欲增加", 1.8),
    ("DRUG_CLOZAPINE", "REC_M1", "ANTAGONIST", "强阻断", "口干便秘", 1.8),
    ("DRUG_CLOZAPINE", "REC_ALPHA1", "ANTAGONIST", "强阻断", "体位性低血压", 1.8),
    ("DRUG_OLANZAPINE", "REC_5HT2A", "ANTAGONIST", "强效拮抗", "降低 EPS", 2.0),
    ("DRUG_OLANZAPINE", "REC_D2", "ANTAGONIST", "中强拮抗", "抗阳性症状", 1.8),
    ("DRUG_OLANZAPINE", "REC_5HT2C", "ANTAGONIST", "强效拮抗", "促前额叶 DA/NE 释放但增食欲", 1.8),
    ("DRUG_OLANZAPINE", "REC_H1", "ANTAGONIST", "强阻断", "体重增加与镇静", 2.0),
    ("DRUG_OLANZAPINE", "REC_M1", "ANTAGONIST", "中强阻断", "口干便秘", 1.5),
    ("DRUG_OLANZAPINE", "REC_ALPHA1", "ANTAGONIST", "中强阻断", "直立性低血压", 1.5),
    ("DRUG_RISPERIDONE", "REC_5HT2A", "ANTAGONIST", "极高亲和力拮抗", "非典型抗精神病特征", 2.0),
    ("DRUG_RISPERIDONE", "REC_D2", "ANTAGONIST", "高亲和力拮抗", "控制阳性症状", 2.0),
    ("DRUG_RISPERIDONE", "REC_ALPHA1", "ANTAGONIST", "强阻断", "体位性低血压", 1.8),
    ("DRUG_QUETIAPINE", "REC_D2", "ANTAGONIST", "快解离弱拮抗", "极低 EPS", 1.5),
    ("DRUG_QUETIAPINE", "REC_5HT2A", "ANTAGONIST", "中强拮抗", "抗精神病", 1.8),
    ("DRUG_QUETIAPINE", "REC_H1", "ANTAGONIST", "强阻断", "镇静助眠", 2.0),
    ("DRUG_QUETIAPINE", "REC_ALPHA1", "ANTAGONIST", "强阻断", "直立性低血压", 1.8),
    ("DRUG_QUETIAPINE", "REC_NET", "INHIBITS", "去甲基代谢物强抑制", "抗双相抑郁", 2.0),
    ("DRUG_QUETIAPINE", "REC_5HT1A", "PARTIAL_AGONIST", "部分激动", "抗焦虑抗抑郁", 1.5),
    ("DRUG_ARIPIPRAZOLE", "REC_D2", "PARTIAL_AGONIST", "部分激动", "多巴胺系统稳定器", 2.0),
    ("DRUG_ARIPIPRAZOLE", "REC_5HT1A", "PARTIAL_AGONIST", "部分激动", "抗焦虑抗抑郁", 1.5),
    ("DRUG_ARIPIPRAZOLE", "REC_5HT2A", "ANTAGONIST", "强效拮抗", "促皮质 DA 释放", 1.8),
    ("DRUG_BREXPIPRAZOLE", "REC_D2", "PARTIAL_AGONIST", "D2部分激动 (低内在活性)", "静坐不能风险极低", 2.0),
    ("DRUG_BREXPIPRAZOLE", "REC_5HT1A", "PARTIAL_AGONIST", "强效5-HT1A部分激动", "抑郁障碍强效增效", 2.0),
    ("DRUG_BREXPIPRAZOLE", "REC_5HT2A", "ANTAGONIST", "强效拮抗", "改善心境与睡眠", 1.8),
    ("DRUG_CARIPRAZINE", "REC_D3", "PARTIAL_AGONIST", "高选择性D3部分激动 (Ki=0.085nM)", "改善阴性症状与认知缺陷", 2.2),
    ("DRUG_CARIPRAZINE", "REC_D2", "PARTIAL_AGONIST", "D2部分激动", "抗阳性与抗躁狂", 1.8),
    ("DRUG_CARIPRAZINE", "REC_5HT1A", "PARTIAL_AGONIST", "5-HT1A部分激动", "抗双相抑郁", 1.5),
    # 卢美哌隆 Lumateperone
    ("DRUG_LUMATEPERONE", "REC_5HT2A", "ANTAGONIST", "超高选择性拮抗 (Ki=0.54nM)", "比D2高60倍亲和力", 2.2),
    ("DRUG_LUMATEPERONE", "REC_D2", "MODULATES", "突触后特异性功能调谐", "改善中脑皮质低多巴胺且不引发EPS", 2.0),
    ("DRUG_LUMATEPERONE", "REC_SERT", "INHIBITS", "抑制 SERT", "抗双相抑郁与心境改善", 2.0),
    ("DRUG_LUMATEPERONE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "治疗阳性与阴性症状", "极佳代谢安全性", 2.0),
    ("DRUG_LUMATEPERONE", "DIS_BIPOLAR_DEP", "TREATS", "FDA批准双相抑郁一线", "单药或联合锂/丙戊酸", 2.2),
    # 匹莫范色林 Pimavanserin
    ("DRUG_PIMAVANSERIN", "REC_5HT2A_INVERSE", "INVERSE_AGONIST", "强效反向激动 5-HT2A", "下调过度神经放电", 2.2),
    ("DRUG_PIMAVANSERIN", "DIS_PDP", "TREATS", "FDA批准帕金森精神病一线", "不阻断D2因此不恶化帕金森运动障碍", 2.4),
    # 乌洛他隆 Ulotaront
    ("DRUG_ULOTARONT", "REC_TAAR1", "AGONIST", "全激动 TAAR1", "突触前负反馈调谐多巴胺放电", 2.4),
    ("DRUG_ULOTARONT", "REC_5HT1A", "AGONIST", "激动 5-HT1A", "改善情绪与突触可塑性", 2.0),
    ("REC_TAAR1", "PATH_MESOLIMBIC", "MODULATES", "突触前抑制多巴胺过度放电", "抗精神分裂症阳性症状", 2.2),
    ("REC_TAAR1", "PATH_MESOCORTICAL", "MODULATES", "优化前额叶谷氨酸/多巴胺平衡", "显著改善阴性症状与认知", 2.2),
    ("DRUG_ULOTARONT", "DIS_SCHIZOPHRENIA_POS", "TREATS", "首创新靶点治疗", "完全无EPS、代谢及高催乳素", 2.4),
    ("DRUG_ULOTARONT", "DIS_SCHIZOPHRENIA_NEG", "TREATS", "显著改善阴性症状", "突破传统药物瓶颈", 2.2),

    # --- 2. 抑郁障碍、难治抑郁 (TRD)、MDSI 及新型抗抑郁药 ---
    ("DRUG_TOLUDESVENLAFAXINE", "REC_SERT", "INHIBITS", "强效抑制 5-HT 再摄取", "提升 5-HT 改善心境", 2.2),
    ("DRUG_TOLUDESVENLAFAXINE", "REC_NET", "INHIBITS", "强效抑制 NE 再摄取", "提升 NE 增强精力与警觉", 2.2),
    ("DRUG_TOLUDESVENLAFAXINE", "REC_DAT", "INHIBITS", "抑制 DA 再摄取", "提升 DA 改善快感缺失与动力", 2.2),
    ("DRUG_TOLUDESVENLAFAXINE", "PATH_PFC_CIRCUITS", "MODULATES", "三重单胺协同调谐", "同步增强前额叶与边缘系统 5-HT/NE/DA 信号", 2.2),
    ("DRUG_TOLUDESVENLAFAXINE", "DIS_MDD", "TREATS", "突破性一线抗抑郁", "显著改善快感缺失 (Anhedonia) 与疲劳", 2.4),
    ("DRUG_TOLUDESVENLAFAXINE", "DIS_TRD", "TREATS", "难治性抑郁全新选择", "突破单/双通道抵抗", 2.2),

    ("DRUG_BUPROPION", "REC_DAT", "INHIBITS", "抑制 DAT", "增加多巴胺奖赏传递与动力", 2.2),
    ("DRUG_BUPROPION", "REC_NET", "INHIBITS", "抑制 NET", "增加去甲肾上腺素提升精力与专注", 2.2),
    ("DRUG_BUPROPION", "REC_NACHR_ALPHA4BETA2", "ANTAGONIST", "非竞争性拮抗烟碱受体", "辅助戒烟机制", 2.0),
    ("DRUG_BUPROPION", "DIS_MDD", "TREATS", "一线抗抑郁", "改善嗜睡、疲乏与快感缺失，无性功能副反应", 2.2),
    ("DRUG_BUPROPION", "DIS_TOBACCO", "TREATS", "一线戒烟药", "缓解戒烟戒断症状与渴求", 2.0),

    # Auvelity
    ("DRUG_AUVELITY", "REC_NMDA", "BLOCKER", "非竞争性阻断 NMDA", "右美沙芬成分", 2.2),
    ("DRUG_AUVELITY", "REC_SIGMA1", "AGONIST", "激动 Sigma-1 受体", "促进神经保护与突触再生", 2.0),
    ("DRUG_AUVELITY", "REC_NET", "INHIBITS", "抑制 NET/DAT", "安非他酮成分协同", 2.0),
    ("DRUG_AUVELITY", "PATH_HIPPOCAMPAL_PLASTICITY", "MODULATES", "快速驱动突触结构重塑", "1周内快速起效", 2.2),
    ("DRUG_AUVELITY", "DIS_MDD", "TREATS", "FDA批准首个口服快速抗抑郁药", "打破4~6周起效延迟", 2.4),
    ("DRUG_AUVELITY", "DIS_TRD", "TREATS", "难治性抑郁有效方案", "多靶点快速突破", 2.2),

    # 神经类固醇 Zuranolone & Brexanolone (产后抑郁 PPD)
    ("DRUG_ZURANOLONE", "REC_GABAA_NEUROSTEROID", "PAM", "强效正向变构调节 δ 亚基", "快速重建脑内紧张性抑制", 2.4),
    ("DRUG_BREXANOLONE", "REC_GABAA_NEUROSTEROID", "PAM", "激活突触外 GABA-A 受体", "重塑产后崩解的神经抑制平衡", 2.2),
    ("REC_GABAA_NEUROSTEROID", "PATH_AMYGDALA_CIRCUITS", "MODULATES", "平息过度放电", "迅速平复产后焦虑与绝望", 2.2),
    ("DRUG_ZURANOLONE", "DIS_PPD", "TREATS", "FDA批准首个口服产后抑郁药", "14天疗程快速且持久治愈", 2.4),
    ("DRUG_ZURANOLONE", "DIS_MDD", "TREATS", "重度抑郁障碍快速缓解", "快速改善重度抑郁心境", 2.2),
    ("DRUG_BREXANOLONE", "DIS_PPD", "TREATS", "静脉滴注特异性产后抑郁药", "60小时快速逆转重度产后抑郁", 2.2),

    # 艾司氯胺酮突触再生链
    ("DRUG_ESKETAMINE", "REC_NMDA", "BLOCKER", "非竞争性瞬时阻滞", "阻断 GABA 抑制神经元 NMDA", 2.2),
    ("REC_NMDA", "REC_AMPA", "MODULATES", "谷氨酸脱抑制爆发", "瞬间激活突触后 AMPA 受体", 2.2),
    ("REC_AMPA", "REC_MTORC1", "MODULATES", "触发钙内流与激酶级联", "开启 mTORC1 突触蛋白翻译总开关", 2.2),
    ("REC_MTORC1", "REC_BDNF_TRKB", "MODULATES", "驱动 BDNF/TrkB 表达与释放", "PSD-95与GluA1快速合成", 2.2),
    ("REC_BDNF_TRKB", "PATH_HIPPOCAMPAL_PLASTICITY", "MODULATES", "驱动树突棘新生与突触修复", "数小时内重建海马-前额叶连接", 2.2),
    ("PATH_HIPPOCAMPAL_PLASTICITY", "DIS_MDD", "TREATS", "抗抑郁结构根源修复", "逆转抑郁突触萎缩", 2.2),
    ("PATH_HIPPOCAMPAL_PLASTICITY", "DIS_MDSI", "TREATS", "数小时内阻断急性自杀冲动", "修复前额叶自控网络", 2.2),
    ("PATH_HIPPOCAMPAL_PLASTICITY", "DIS_TRD", "TREATS", "打破慢性难治僵局", "重建萎缩突触连接", 2.2),
    ("DRUG_ESKETAMINE", "DIS_MDSI", "TREATS", "FDA/NMPA 首获批急性自杀干预药", "4~24小时快速阻断自杀危机", 2.4),
    ("DRUG_ESKETAMINE", "DIS_TRD", "TREATS", "FDA/NMPA 批准难治抑郁一线", "突触再生全新机制", 2.4),

    # 阿戈美拉汀与 SCN
    ("DRUG_AGOMELATINE", "REC_MT1_MT2", "AGONIST", "强效激动 MT1/MT2", "重塑视交叉上核生物钟", 2.2),
    ("DRUG_AGOMELATINE", "REC_5HT2C", "ANTAGONIST", "选择性拮抗 5-HT2C", "脱抑制促进前额叶 DA/NE 释放", 2.2),
    ("DRUG_AGOMELATINE", "PATH_CIRCADIAN_SCN", "MODULATES", "重调昼夜节律", "恢复慢波睡眠与情绪节律", 2.2),
    ("DRUG_AGOMELATINE", "PATH_PFC_CIRCUITS", "MODULATES", "协同提升前额叶 DA/NE", "改善认知动机与心境", 2.0),
    ("DRUG_AGOMELATINE", "DIS_MDD", "TREATS", "一线抗抑郁", "重塑节律且无性功能副作用", 2.2),
    ("DRUG_AGOMELATINE", "DIS_INSOMNIA", "TREATS", "改善睡眠时相", "促进生理性入睡与节律同步", 2.0),

    # 伏硫西汀 & 维拉佐酮
    ("DRUG_VORTIOXETINE", "REC_SERT", "INHIBITS", "抑制 SERT", "抗抑郁", 2.0),
    ("DRUG_VORTIOXETINE", "REC_5HT1A", "AGONIST", "全激动 5-HT1A", "促进海马神经发生与 BDNF", 2.0),
    ("DRUG_VORTIOXETINE", "REC_5HT1B_1D", "PARTIAL_AGONIST", "自身受体调节", "促单胺释放", 1.5),
    ("DRUG_VORTIOXETINE", "REC_5HT3", "ANTAGONIST", "强效拮抗 5-HT3", "促进乙酰胆碱释放强化 LTP", 2.2),
    ("DRUG_VORTIOXETINE", "REC_5HT7", "ANTAGONIST", "强效拮抗 5-HT7", "重塑前额叶突触改善认知迟滞", 2.2),
    ("DRUG_VORTIOXETINE", "PATH_HIPPOCAMPAL_PLASTICITY", "MODULATES", "突触结构可塑性重塑", "直接增强海马树突分支", 2.2),
    ("DRUG_VORTIOXETINE", "DIS_MDD", "TREATS", "一线多模式抗抑郁", "显著改善工作记忆与执行认知障碍", 2.2),
    ("DRUG_VILAZODONE", "REC_SERT", "INHIBITS", "抑制 SERT", "抗抑郁", 2.0),
    ("DRUG_VILAZODONE", "REC_5HT1A", "PARTIAL_AGONIST", "高亲和力部分激动", "快速抗抑郁且较少性功能副反应", 2.0),
    ("DRUG_VILAZODONE", "DIS_MDD", "TREATS", "一线抗抑郁", "低性功能副反应", 2.0),

    # 经典 SSRI / SNRI
    ("DRUG_FLUOXETINE", "REC_SERT", "INHIBITS", "强效抑制", "增加 5-HT", 2.0),
    ("DRUG_FLUOXETINE", "REC_5HT2C", "ANTAGONIST", "拮抗受体", "增加前额叶 DA/NE", 1.8),
    ("DRUG_SERTRALINE", "REC_SERT", "INHIBITS", "强效抑制", "抗抑郁", 2.0),
    ("DRUG_SERTRALINE", "REC_DAT", "INHIBITS", "弱抑制", "增加动机与精力", 1.5),
    ("DRUG_SERTRALINE", "REC_SIGMA1", "AGONIST", "激动 Sigma-1", "突触重塑", 2.0),
    ("DRUG_ESCITALOPRAM", "REC_SERT", "INHIBITS", "纯变构抑制", "高特异性抗抑郁抗焦虑", 2.0),
    ("DRUG_VENLAFAXINE", "REC_SERT", "INHIBITS", "强效抑制", "抗抑郁", 2.0),
    ("DRUG_VENLAFAXINE", "REC_NET", "INHIBITS", "中高剂量抑制", "提升精力与警觉", 1.8),
    ("DRUG_DULOXETINE", "REC_SERT", "INHIBITS", "强效抑制", "抗抑郁", 2.0),
    ("DRUG_DULOXETINE", "REC_NET", "INHIBITS", "强效抑制", "激活下行镇痛通路", 2.0),
    ("DRUG_MIRTAZAPINE", "REC_ALPHA2A", "ANTAGONIST", "阻断自身受体", "脱抑制促进 5-HT/NE 释放", 2.0),
    ("DRUG_MIRTAZAPINE", "REC_5HT2A", "ANTAGONIST", "阻断受体", "消除性功能副作用", 1.5),
    ("DRUG_MIRTAZAPINE", "REC_5HT2C", "ANTAGONIST", "阻断受体", "抗抑郁并增进食欲", 1.8),
    ("DRUG_MIRTAZAPINE", "REC_H1", "ANTAGONIST", "强阻断", "助眠镇静", 2.0),

    # --- 3. 焦虑、创伤应激 (PTSD) 与强迫障碍 (OCD) ---
    ("DRUG_FLUVOXAMINE", "REC_SERT", "INHIBITS", "强效抑制 SERT", "提升突触间隙 5-HT", 2.2),
    ("DRUG_FLUVOXAMINE", "REC_SIGMA1", "AGONIST", "超强亲和力激动 Sigma-1 (Ki=36nM)", "抗炎及突触重塑", 2.4),
    ("DRUG_FLUVOXAMINE", "PATH_CSTC_LOOPS", "MODULATES", "调谐皮质-纹状体环路过度兴奋", "抑制强迫性思维反刍与仪式动作", 2.4),
    ("DRUG_FLUVOXAMINE", "DIS_OCD", "TREATS", "指南首选一线治疗", "强迫障碍特效药", 2.4),
    ("DRUG_CLOMIPRAMINE", "REC_SERT", "INHIBITS", "极强效抑制 SERT", "强效提升 5-HT", 2.2),
    ("DRUG_CLOMIPRAMINE", "PATH_CSTC_LOOPS", "MODULATES", "调控 CSTC 环路", "缓解难治性强迫观念", 2.2),
    ("DRUG_CLOMIPRAMINE", "DIS_OCD", "TREATS", "经典二线特效治疗", "强迫障碍", 2.2),
    ("PATH_CSTC_LOOPS", "DIS_OCD", "CORRELATED_WITH", "环路过度激活驱动", "强迫观念与刻板行为生化基础", 2.2),

    ("DRUG_PROPRANOLOL", "REC_BETA_ADRENERGIC", "BLOCKER", "非选择性阻断中枢与外周 β 受体", "阻断肾上腺素能激增", 2.2),
    ("DRUG_PROPRANOLOL", "PATH_FEAR_EXTINCTION", "MODULATES", "阻断杏仁核恐惧记忆再巩固", "促进创伤恐惧消退", 2.2),
    ("DRUG_PROPRANOLOL", "DIS_PTSD", "TREATS", "创伤记忆再暴露辅助治疗", "降低创伤引发的剧烈自主神经过度唤醒", 2.2),
    ("DRUG_PROPRANOLOL", "DIS_SAD", "TREATS", "社交焦虑表演型", "按需阻断心悸手抖出汗", 2.2),
    ("DRUG_PRAZOSIN", "REC_ALPHA1", "ANTAGONIST", "高选择性阻断中枢 α1 受体", "抑制蓝斑核过度放电", 2.2),
    ("DRUG_PRAZOSIN", "PATH_FEAR_EXTINCTION", "MODULATES", "平息夜间蓝斑核肾上腺素风暴", "减少创伤噩梦与觉醒", 2.2),
    ("DRUG_PRAZOSIN", "DIS_PTSD", "TREATS", "PTSD 噩梦特效药", "显著减少创伤相关噩梦并改善睡眠", 2.4),
    ("PATH_FEAR_EXTINCTION", "DIS_PTSD", "CORRELATED_WITH", "恐惧消退损伤驱动", "PTSD 创伤后病理基础", 2.0),

    ("DRUG_BUSPIRONE", "REC_5HT1A", "PARTIAL_AGONIST", "选择性 5-HT1A 部分激动", "自身受体脱敏促 5-HT 平衡", 2.2),
    ("DRUG_BUSPIRONE", "PATH_AMYGDALA_CIRCUITS", "MODULATES", "降低杏仁核焦虑放电", "平稳抗焦虑", 2.0),
    ("DRUG_BUSPIRONE", "DIS_GAD", "TREATS", "指南推荐一线抗焦虑", "无镇静、无肌松、无成瘾", 2.2),
    ("DRUG_TANDOSPIRONE", "REC_5HT1A", "PARTIAL_AGONIST", "高亲和力 5-HT1A 部分激动", "抗焦虑兼调节自主神经", 2.2),
    ("DRUG_TANDOSPIRONE", "DIS_GAD", "TREATS", "抗焦虑一线", "改善伴随的自主神经失调躯体症状", 2.2),

    # 普瑞巴林、地达西尼 (京诺宁®) & BZD 类
    ("DRUG_DIMDAZENIL", "REC_GABAA_ALPHA1_PARTIAL", "PAM", "高选择性部分正向变构调节 (pPAM)", "适度促进 Cl- 内流产生精准促眠", 2.4),
    ("DRUG_DIMDAZENIL", "PATH_VLPO_SLEEP_SWITCH", "MODULATES", "温和激活中枢睡眠开关", "生理性缩短入睡潜伏期并延长总睡眠", 2.4),
    ("DRUG_DIMDAZENIL", "DIS_INSOMNIA", "TREATS", "中国首创 1 类新药一线催眠", "无肌无力、无宿醉嗜睡、无反跳依赖", 2.4),
    ("REC_GABAA_ALPHA1_PARTIAL", "PATH_VLPO_SLEEP_SWITCH", "MODULATES", "精准中枢镇静催眠调控", "介导生理性入睡", 2.2),

    ("DRUG_PREGABALIN", "REC_ALPHA2DELTA", "BLOCKER", "特异性结合 α2δ 亚基", "抑制突触前钙内流与兴奋性递质释放", 2.2),
    ("DRUG_PREGABALIN", "PATH_AMYGDALA_CIRCUITS", "MODULATES", "平息杏仁核恐惧环路过度兴奋", "快速抗焦虑", 2.2),
    ("DRUG_PREGABALIN", "PATH_PAIN_PATHWAY", "MODULATES", "减少脊髓后角钙内流", "降低痛觉敏化", 2.2),
    ("DRUG_PREGABALIN", "DIS_GAD", "TREATS", "欧洲指南一线", "快速缓解广泛性焦虑", 2.2),
    ("DRUG_PREGABALIN", "DIS_NEURO_PAIN", "TREATS", "一线治疗", "糖尿病周围神经痛与纤维肌痛", 2.2),

    ("DRUG_LORAZEPAM", "REC_GABAA", "PAM", "正向变构调节", "抗焦虑与镇静", 2.0),
    ("DRUG_ALPRAZOLAM", "REC_GABAA", "PAM", "强效调节", "终止惊恐发作", 2.0),
    ("DRUG_DIAZEPAM", "REC_GABAA", "PAM", "广谱调节", "抗焦虑肌松", 2.0),
    ("DRUG_CLONAZEPAM", "REC_GABAA", "PAM", "高亲和力调节", "长效抗惊恐", 2.0),
    ("DRUG_LORAZEPAM", "DIS_GAD", "TREATS", "快速缓解", "急性焦虑发作", 1.8),
    ("DRUG_ALPRAZOLAM", "DIS_PANIC", "TREATS", "强效控制", "惊恐发作与惊恐障碍", 2.0),
    ("DRUG_CLONAZEPAM", "DIS_PANIC", "TREATS", "长效维持", "惊恐障碍与焦虑", 2.0),

    # --- 4. 双相障碍与心境稳定剂 ---
    ("DRUG_LITHIUM", "REC_GSK3B", "BLOCKER", "直接竞争性抑制", "抑制 GSK-3β 磷酸化防止突触退化", 2.2),
    ("DRUG_VALPROATE", "REC_GSK3B", "BLOCKER", "间接抑制", "通过 Akt 激活抑制 GSK-3β", 2.0),
    ("DRUG_VALPROATE", "REC_VGSC", "BLOCKER", "抑制钠通道", "抗躁狂", 1.8),
    ("DRUG_VALPROATE", "REC_GABAA", "PAM", "增强 GABA 合成与代谢抑制", "中枢抑制抗躁狂", 1.8),
    ("DRUG_CARBAMAZEPINE", "REC_VGSC", "BLOCKER", "阻滞使用依赖性钠通道", "抑制高频病理性放电", 2.2),
    ("DRUG_LAMOTRIGINE", "REC_VGSC", "BLOCKER", "抑制钠通道", "减少谷氨酸释放，预防双相抑郁", 2.0),
    ("REC_GSK3B", "REC_BDNF_TRKB", "MODULATES", "激活 Wnt 与 BDNF 转录", "解除对 β-catenin 降解刹车", 2.2),
    ("DRUG_LITHIUM", "DIS_BIPOLAR_MANIA", "TREATS", "经典一线", "双相躁狂及长期预防复发", 2.2),
    ("DRUG_LITHIUM", "DIS_MDSI", "TREATS", "经典长期防自杀", "循证证实显著降低自杀率", 2.2),
    ("DRUG_LITHIUM", "DIS_TRD", "TREATS", "经典增效方案", "打破难治状态", 2.2),
    ("DRUG_VALPROATE", "DIS_BIPOLAR_MANIA", "TREATS", "一线治疗", "急性躁狂发作", 2.0),
    ("DRUG_CARBAMAZEPINE", "DIS_BIPOLAR_MANIA", "TREATS", "经典一线", "双相躁狂发作", 2.0),
    ("DRUG_LAMOTRIGINE", "DIS_BIPOLAR_DEP", "TREATS", "一线预防", "双相抑郁复发预防", 2.2),

    # --- 5. 睡眠-觉醒障碍、前沿 DORA 四大药与促醒系统 (发作性睡病) ---
    # 法赞雷生 Fazamorexant
    ("DRUG_FAZAMOREXANT", "REC_OX1R_OX2R", "ANTAGONIST", "双重高亲和力阻断 OX1R/OX2R", "特异性关闭下丘脑促觉醒信号", 2.4),
    ("DRUG_FAZAMOREXANT", "PATH_HYPOTHALAMIC_AROUSAL", "MODULATES", "重塑生理性睡眠觉醒平衡", "显著缩短入睡潜伏期并延长总睡眠", 2.4),
    ("DRUG_FAZAMOREXANT", "DIS_INSOMNIA", "TREATS", "中国首个自主研发 1 类 DORA 催眠药", "改善入睡与睡眠维持困难且无耐受成瘾", 2.4),

    # 沃诺雷生 Vornorexant (Vorzzz)
    ("DRUG_VORNOREXANT", "REC_OX1R_OX2R", "ANTAGONIST", "超快解离阻断 OX1R/OX2R", "快速促进入睡且血药浓度迅速清除", 2.4),
    ("DRUG_VORNOREXANT", "PATH_HYPOTHALAMIC_AROUSAL", "MODULATES", "高效诱导生理性睡眠", "次日清晨零残留嗜睡", 2.4),
    ("DRUG_VORNOREXANT", "DIS_INSOMNIA", "TREATS", "新一代短半衰期 DORA 一线催眠", "改善入睡与睡眠维持同时提升日间精力", 2.4),

    ("DRUG_LEMBOREXANT", "REC_OX1R_OX2R", "ANTAGONIST", "强效双重阻断", "生理性促进入睡与睡眠维持", 2.2),
    ("DRUG_DARIDOREXANT", "REC_OX1R_OX2R", "ANTAGONIST", "优化半衰期双重阻断", "改善睡眠同时提升日间精力", 2.2),
    ("DRUG_RAMELTEON", "REC_MT1_MT2", "AGONIST", "高亲和力激动 MT1/MT2", "诱导睡眠时相转换", 2.2),
    ("REC_OX1R_OX2R", "PATH_HYPOTHALAMIC_AROUSAL", "MODULATES", "维持觉醒状态", "食欲素过度放电导致失眠", 1.8),
    ("DRUG_LEMBOREXANT", "DIS_INSOMNIA", "TREATS", "新一代一线催眠", "改善入睡与睡眠维持且无宿醉成瘾", 2.2),
    ("DRUG_DARIDOREXANT", "DIS_INSOMNIA", "TREATS", "一线催眠", "改善夜间睡眠与日间精力", 2.2),
    ("DRUG_RAMELTEON", "DIS_INSOMNIA", "TREATS", "入睡困难催眠", "无耐受成瘾", 2.0),

    # 促醒三剑客: 莫达非尼, 替洛利生 (铧可思®), 羟丁酸钠 -> 发作性睡病 Narcolepsy
    ("DRUG_MODAFINIL", "REC_DAT", "INHIBITS", "选择性微弱阻断 DAT", "平稳提升皮层多巴胺", 2.0),
    ("DRUG_MODAFINIL", "PATH_HYPOTHALAMIC_AROUSAL", "MODULATES", "激活食欲素与下丘脑组胺神经元", "强效促醒", 2.2),
    ("DRUG_MODAFINIL", "DIS_NARCOLEPSY", "TREATS", "指南一线促醒药", "消除日间不可抗拒嗜睡", 2.4),
    ("DRUG_ARMODAFINIL", "REC_DAT", "INHIBITS", "长效平稳抑制 DAT", "持久维持警觉", 2.0),
    ("DRUG_ARMODAFINIL", "DIS_NARCOLEPSY", "TREATS", "长效促醒", "改善日间嗜睡", 2.2),

    # 替洛利生 Pitolisant (铧可思®)
    ("DRUG_PITOLISANT", "REC_HISTAMINE_H3", "ANTAGONIST", "高选择性 H3 拮抗/反向激动 (Ki=0.16nM)", "解除突触前组胺负反馈", 2.4),
    ("REC_HISTAMINE_H3", "PATH_TMN_HISTAMINE_AROUSAL", "MODULATES", "促进结节乳头体核组胺爆发释放", "驱动全脑皮层觉醒", 2.2),
    ("DRUG_PITOLISANT", "DIS_NARCOLEPSY", "TREATS", "首创非管制促醒与抗猝倒药", "显著改善日间嗜睡与猝倒发作", 2.4),

    ("DRUG_SODIUM_OXYBATE", "REC_GHB_GABAB", "AGONIST", "激动 GABA-B 与 GHB 受体", "巩固夜间深慢波睡眠", 2.2),
    ("REC_GHB_GABAB", "PATH_VLPO_SLEEP_SWITCH", "MODULATES", "强化夜间主动睡眠中枢", "减少白天异位 REM 猝倒发作", 2.2),
    ("DRUG_SODIUM_OXYBATE", "DIS_NARCOLEPSY", "TREATS", "发作性睡病猝倒特效药", "唯一同时解决夜间睡眠紊乱与白天猝倒", 2.4),
    ("PATH_HYPOTHALAMIC_AROUSAL", "DIS_NARCOLEPSY", "CORRELATED_WITH", "食欲素神经元退化驱动", "发作性睡病病理根源", 2.0),

    # --- 6. ADHD 与前额叶执行功能网络 ---
    ("DRUG_LISDEXAMFETAMINE", "REC_DAT", "INHIBITS", "阻断并逆转 DAT", "强效提升突触间隙 DA", 2.2),
    ("DRUG_LISDEXAMFETAMINE", "REC_NET", "INHIBITS", "阻断并逆转 NET", "强效提升前额叶 NE", 2.2),
    ("DRUG_LISDEXAMFETAMINE", "REC_VMAT2", "MODULATES", "促进囊泡单胺外排", "逆转 VMAT2 促进胞浆单胺释放", 2.0),
    ("DRUG_LISDEXAMFETAMINE", "PATH_PFC_CIRCUITS", "MODULATES", "最佳化 DA/NE 神经调节", "使前额叶锥体神经元调谐至最佳信噪比", 2.2),
    ("DRUG_LISDEXAMFETAMINE", "DIS_ADHD", "TREATS", "一线平稳长效治疗", "全天候改善注意力、工作记忆与多动冲动", 2.4),
    ("DRUG_LISDEXAMFETAMINE", "SE_ADDICTION_TOLERANCE", "CAUSES", "极低滥用倾向 (前药)", "需经红细胞酶解，静脉或鼻吸无效", 1.2),

    ("DRUG_METHYLPHENIDATE", "REC_DAT", "INHIBITS", "阻断再摄取泵", "增加前额叶 DA", 2.0),
    ("DRUG_METHYLPHENIDATE", "REC_NET", "INHIBITS", "阻断再摄取泵", "增加前额叶 NE", 2.0),
    ("DRUG_ATOMOXETINE", "REC_NET", "INHIBITS", "高选择性阻断", "前额叶同时提升 NE/DA", 2.0),
    ("DRUG_GUANFACINE", "REC_ALPHA2A", "AGONIST", "高选择性激动", "强化前额叶树突棘连接", 2.0),
    ("DRUG_VILOXAZINE", "REC_NET", "INHIBITS", "高选择性抑制 NET", "前额叶提升 NE 与 DA", 2.2),
    ("DRUG_VILOXAZINE", "REC_5HT7", "AGONIST", "激动 5-HT7 受体", "促进前额叶注意力网络连接", 2.0),
    ("DRUG_VILOXAZINE", "DIS_ADHD", "TREATS", "新型非兴奋剂一线", "改善注意缺陷与情绪调控，无滥用风险", 2.2),
    ("DRUG_METHYLPHENIDATE", "DIS_ADHD", "TREATS", "一线兴奋剂", "改善注意力与多动冲动", 2.0),
    ("DRUG_ATOMOXETINE", "DIS_ADHD", "TREATS", "一线非兴奋剂", "改善注意力与执行功能", 2.0),
    ("DRUG_GUANFACINE", "DIS_ADHD", "TREATS", "非兴奋剂", "强化前额叶网络连接", 2.0),

    # --- 7. 痴呆、阿尔茨海默病与认知功能 ---
    ("DRUG_DONEPEZIL", "REC_ACHE", "INHIBITS", "高选择性可逆抑制 AChE", "抑制乙酰胆碱水解", 2.2),
    ("DRUG_RIVASTIGMINE", "REC_ACHE", "INHIBITS", "双重抑制 AChE 与 BuChE", "强效提升脑内乙酰胆碱", 2.2),
    ("DRUG_GALANTAMINE", "REC_ACHE", "INHIBITS", "抑制 AChE", "增加乙酰胆碱浓度", 2.0),
    ("DRUG_GALANTAMINE", "REC_NACHR_ALPHA4BETA2", "MODULATES", "烟碱受体变构增敏调节", "促进神经递质协同释放", 2.2),
    ("REC_ACHE", "PATH_BASAL_FOREBRAIN_ACH", "MODULATES", "延缓胆碱能神经元退化", "改善皮层注意力与记忆提取", 2.2),
    ("PATH_BASAL_FOREBRAIN_ACH", "DIS_ALZHEIMER", "CORRELATED_WITH", "胆碱能丢失导致", "记忆力衰退与认知缺陷生化基础", 2.2),
    ("DRUG_DONEPEZIL", "DIS_ALZHEIMER", "TREATS", "指南一线治疗", "轻中重度阿尔茨海默病认知改善", 2.2),
    ("DRUG_RIVASTIGMINE", "DIS_ALZHEIMER", "TREATS", "一线治疗", "阿尔茨海默病及帕金森痴呆认知改善", 2.2),
    ("DRUG_GALANTAMINE", "DIS_ALZHEIMER", "TREATS", "一线治疗", "轻中度阿尔茨海默病认知改善", 2.0),
    ("DRUG_MEMANTINE", "REC_NMDA", "BLOCKER", "中等亲和力非竞争性拮抗", "减少病理性谷氨酸兴奋毒性，保护残存突触", 2.2),
    ("DRUG_MEMANTINE", "DIS_ALZHEIMER", "TREATS", "中重度阿尔茨海默病一线", "保护神经元延缓功能衰退", 2.2),

    ("DRUG_LECANEMAB", "REC_AMYLOID_BETA", "ANTAGONIST", "特异性高亲和力结合 Aβ 可溶性原纤维", "促进脑内淀粉样蛋白清除", 2.4),
    ("DRUG_DONANEMAB", "REC_AMYLOID_BETA", "ANTAGONIST", "高特异性结合 N3pG-Aβ 淀粉样沉积斑块", "深度清除脑内 Aβ 沉积斑块", 2.4),
    ("REC_AMYLOID_BETA", "PATH_HIPPOCAMPAL_PLASTICITY", "MODULATES", "Aβ 寡聚体毒性损伤突触棘", "导致海马与皮层突触丢失及 Tau 缠结", 2.2),
    ("DRUG_LECANEMAB", "DIS_ALZHEIMER", "TREATS", "FDA/NMPA 批准疾病修饰疗法 (DMT)", "靶向清除 Aβ 显著减缓早期阿尔茨海默病病程", 2.4),
    ("DRUG_DONANEMAB", "DIS_ALZHEIMER", "TREATS", "靶向斑块疾病修饰疗法", "清除脑斑块并显著延缓痴呆进展", 2.4),

    # --- 8. 物质成瘾与戒断 (酒精, 尼古丁, 阿片) ---
    ("DRUG_VARENICLINE", "REC_NACHR_ALPHA4BETA2", "PARTIAL_AGONIST", "高选择性 α4β2 部分激动 (40-60%内在活性)", "适度释放多巴胺缓解戒断痛苦", 2.4),
    ("REC_NACHR_ALPHA4BETA2", "PATH_VTA_NACC_REWARD", "MODULATES", "竞争性阻断尼古丁与受体结合", "消除抽烟带来的强化欣快感", 2.2),
    ("DRUG_VARENICLINE", "DIS_TOBACCO", "TREATS", "指南一线首选戒烟药", "显著提高长期戒烟成功率", 2.4),

    ("DRUG_NALTREXONE", "REC_MU_OPIOID", "ANTAGONIST", "强效竞争性阻断 μ-阿片受体", "切断饮酒触发的多巴胺奖赏回路", 2.4),
    ("REC_MU_OPIOID", "PATH_VTA_NACC_REWARD", "MODULATES", "阻断内源性阿片肽对 VTA 多巴胺释放的促进", "消除饮酒欣快感并降低渴求", 2.2),
    ("DRUG_NALTREXONE", "DIS_AUD", "TREATS", "FDA 批准一线戒酒药", "显著减少重度饮酒天数与复饮率", 2.4),
    ("DRUG_NALTREXONE", "DIS_OUD", "TREATS", "阿片完全戒断后防复吸维持", "阻断阿片类物质效应", 2.2),

    ("DRUG_ACAMPROSATE", "REC_NMDA", "MODULATES", "调节 NMDA 谷氨酸受体", "平息戒酒后高谷氨酸过度兴奋性状态", 2.2),
    ("DRUG_ACAMPROSATE", "DIS_AUD", "TREATS", "FDA 批准戒酒维持药", "维持长期戒断状态，消除戒断躯体不适", 2.2),

    ("DRUG_DISULFIRAM", "REC_ALDH", "BLOCKER", "不可逆抑制乙醛脱氢酶", "阻断酒精正常氧化代谢", 2.2),
    ("DRUG_DISULFIRAM", "DIS_AUD", "TREATS", "戒酒厌恶疗法", "饮酒后乙醛剧烈蓄积引发面红恶心强制戒酒", 2.2),

    ("DRUG_BUPRENORPHINE", "REC_MU_OPIOID", "PARTIAL_AGONIST", "高亲和力慢解离 μ 受体部分激动", "消除戒断症状且无过度欣快", 2.4),
    ("DRUG_BUPRENORPHINE", "REC_KAPPA_OPIOID", "ANTAGONIST", "拮抗 κ-阿片受体", "消除戒断烦躁负性情绪与抗抑郁", 2.2),
    ("DRUG_BUPRENORPHINE", "DIS_OUD", "TREATS", "阿片替代维持一线药", "具有呼吸抑制天花板效应，安全性极佳", 2.4),

    ("DRUG_NALOXONE", "REC_MU_OPIOID", "ANTAGONIST", "纯竞争性强效拮抗 μ 受体", "快速置换外源性阿片分子", 2.4),
    ("DRUG_NALOXONE", "DIS_OUD", "TREATS", "阿片过量中毒急救特效解毒剂", "数分钟内逆转呼吸抑制抢救生命", 2.4),
    ("PATH_VTA_NACC_REWARD", "DIS_AUD", "CORRELATED_WITH", "多巴胺强化失调驱动", "酒精成瘾病理机制", 2.0),
    ("PATH_VTA_NACC_REWARD", "DIS_OUD", "CORRELATED_WITH", "阿片受体脱敏与奖赏失控", "阿片成瘾病理机制", 2.0),
    ("PATH_VTA_NACC_REWARD", "DIS_TOBACCO", "CORRELATED_WITH", "尼古丁多巴胺脉冲强化", "烟草依赖病理机制", 2.0),

    # --- 9. 慢性疼痛与下行镇痛网络 ---
    ("DRUG_DULOXETINE", "DIS_NEURO_PAIN", "TREATS", "一线治疗", "周围神经病理性疼痛与纤维肌痛", 2.2),
    ("REC_NET", "PATH_PAIN_PATHWAY", "MODULATES", "强化下行 NE 抑制", "增强内源性下行镇痛", 1.8),
    ("PATH_PAIN_PATHWAY", "DIS_NEURO_PAIN", "CORRELATED_WITH", "下行镇痛受损驱动", "神经病理性疼痛与中枢敏化", 2.0),

    # --- 10. 迟发性运动障碍 (TD) ---
    ("DRUG_VALBENAZINE", "REC_VMAT2", "INHIBITS", "高选择性抑制 VMAT2", "减少突触前多巴胺囊泡装载与释放", 2.2),
    ("REC_VMAT2", "PATH_NIGROSTRIATAL", "MODULATES", "调节黑质纹状体多巴胺释放", "改善迟发性运动障碍不自主运动", 2.2),
    ("DRUG_VALBENAZINE", "DIS_TD", "TREATS", "FDA 首选治疗", "迟发性运动障碍 (TD)", 2.4),
    ("PATH_NIGROSTRIATAL", "DIS_TD", "CORRELATED_WITH", "长期 D2 阻断受体超敏导致", "迟发性运动障碍", 2.0),

    # --- 基础通路与疾病关联 ---
    ("REC_D2", "PATH_MESOLIMBIC", "MODULATES", "介导", "D2过度激活导致幻觉妄想", 1.0),
    ("REC_D3", "PATH_MESOCORTICAL", "MODULATES", "促进认知与动机", "D3部分激动改善前额叶功能", 1.0),
    ("REC_5HT2A", "PATH_MESOCORTICAL", "MODULATES", "刹车调控", "5-HT2A拮抗脱抑制增加皮质DA释放", 1.0),
    ("REC_5HT2C", "PATH_PFC_CIRCUITS", "MODULATES", "脱抑制调控", "5-HT2C拮抗增加前额叶DA/NE释放", 1.0),
    ("REC_5HT3", "PATH_PFC_CIRCUITS", "MODULATES", "促进乙酰胆碱与单胺释放", "显著增强认知与工作记忆", 1.0),
    ("REC_5HT7", "PATH_PFC_CIRCUITS", "MODULATES", "增强突触可塑性与LTP", "改善抑郁相关认知迟滞", 1.0),
    ("REC_D2", "PATH_NIGROSTRIATAL", "MODULATES", "运动协调", "D2占有率>80%导致EPS", 1.0),
    ("REC_D2", "PATH_TUBEROINFUNDIBULAR", "MODULATES", "内分泌调节", "D2阻断引发催乳素升高", 1.0),
    ("REC_GABAA", "PATH_AMYGDALA_CIRCUITS", "MODULATES", "中枢刹车抑制", "增强 GABA-A 降低杏仁核过度放电", 1.0),
    ("REC_DAT", "PATH_PFC_CIRCUITS", "MODULATES", "多巴胺清除", "调控注意聚焦", 1.0),
    ("REC_D1", "PATH_PFC_CIRCUITS", "MODULATES", "倒 U 型信号调谐", "适度 D1 激活提升工作记忆信噪比", 1.0),
    ("REC_ALPHA2A", "PATH_PFC_CIRCUITS", "MODULATES", "增强信号信噪比", "强化前额叶锥体细胞连接", 1.0),
    ("REC_NMDA", "PATH_PFC_CIRCUITS", "MODULATES", "突触可塑性与兴奋毒性", "艾司氯胺酮/美金刚调控认知与抑郁", 1.0),

    ("PATH_MESOLIMBIC", "DIS_SCHIZOPHRENIA_POS", "CORRELATED_WITH", "驱动", "阳性症状生化根源", 1.0),
    ("PATH_MESOCORTICAL", "DIS_SCHIZOPHRENIA_NEG", "CORRELATED_WITH", "关联", "皮质功能不足致阴性/认知损害", 1.0),
    ("PATH_NIGROSTRIATAL", "SE_EPS", "CORRELATED_WITH", "诱发", "锥体外系运动障碍", 1.0),
    ("PATH_TUBEROINFUNDIBULAR", "SE_HYPERPROLACTIN", "CORRELATED_WITH", "诱发", "高催乳素血症与溢乳", 1.0),
    ("PATH_AMYGDALA_CIRCUITS", "DIS_GAD", "CORRELATED_WITH", "驱动", "广泛性焦虑的核心环路", 1.0),
    ("PATH_AMYGDALA_CIRCUITS", "DIS_PANIC", "CORRELATED_WITH", "驱动", "惊恐发作核心环路", 1.0),
    ("PATH_AMYGDALA_CIRCUITS", "DIS_SAD", "CORRELATED_WITH", "驱动", "社交恐惧核心中枢", 1.0),
    ("PATH_PFC_CIRCUITS", "DIS_ADHD", "CORRELATED_WITH", "功能低下介导", "注意缺陷与多动冲动", 1.0),
    ("PATH_PFC_CIRCUITS", "DIS_MDD", "CORRELATED_WITH", "调控受损介导", "执行迟滞与情绪调节障碍", 1.0),
    ("PATH_HYPOTHALAMIC_AROUSAL", "DIS_INSOMNIA", "CORRELATED_WITH", "过度激活驱动", "入睡困难与睡眠维持障碍", 1.0),

    # 不良反应诱发连接
    ("REC_M1", "SE_ANTICHOLINERGIC", "MODULATES", "诱发", "口干、视物模糊、便秘与嗜睡", 1.0),
    ("REC_ALPHA1", "SE_ORTHOSTATIC_HYPOTENSION", "MODULATES", "诱发", "直立性低血压与头晕", 1.0),
    ("REC_H1", "SE_SEDATION", "MODULATES", "诱发", "嗜睡镇静", 1.0),
    ("REC_5HT2C", "SE_METABOLIC", "MODULATES", "诱发", "食欲大增与代谢体重上升", 1.0),
    ("DRUG_HALOPERIDOL", "SE_EPS", "CAUSES", "极高风险", "急性肌张力障碍/静坐不能/类帕金森", 1.0),
    ("DRUG_HALOPERIDOL", "SE_HYPERPROLACTIN", "CAUSES", "极高风险", "催乳素显著上升", 1.0),
    ("DRUG_CLOZAPINE", "SE_METABOLIC", "CAUSES", "显著增加", "胰岛素抵抗与体重增加", 1.0),
    ("DRUG_CLOZAPINE", "SE_ANTICHOLINERGIC", "CAUSES", "显著口干便秘", "强抗胆碱能效应", 1.0),
    ("DRUG_CLOZAPINE", "SE_ORTHOSTATIC_HYPOTENSION", "CAUSES", "高风险", "强 α1 阻断", 1.0),
    ("DRUG_OLANZAPINE", "SE_METABOLIC", "CAUSES", "显著增加", "代谢综合征与体重增加", 1.0),
    ("DRUG_OLANZAPINE", "SE_SEDATION", "CAUSES", "镇静嗜睡", "H1强阻断", 1.0),
    ("DRUG_RISPERIDONE", "SE_EPS", "CAUSES", "高剂量诱发", "锥体外系反应", 1.0),
    ("DRUG_RISPERIDONE", "SE_HYPERPROLACTIN", "CAUSES", "高风险", "催乳素显著上升", 1.0),
    ("DRUG_RISPERIDONE", "SE_ORTHOSTATIC_HYPOTENSION", "CAUSES", "低血压", "α1 阻断", 1.0),
    ("DRUG_QUETIAPINE", "SE_SEDATION", "CAUSES", "镇静嗜睡", "强 H1 阻断", 1.0),
    ("DRUG_QUETIAPINE", "SE_ORTHOSTATIC_HYPOTENSION", "CAUSES", "头晕低血压", "强 α1 阻断", 1.0),
    ("DRUG_MIRTAZAPINE", "SE_SEDATION", "CAUSES", "嗜睡助眠", "强 H1 阻断", 1.0),
    ("DRUG_MIRTAZAPINE", "SE_METABOLIC", "CAUSES", "食欲与体重增加", "5-HT2C/H1阻断", 1.0),
    ("DRUG_LORAZEPAM", "SE_SEDATION", "CAUSES", "镇静嗜睡", "中枢抑制", 1.0),
    ("DRUG_LORAZEPAM", "SE_ADDICTION_TOLERANCE", "CAUSES", "耐受依赖", "建议短期使用", 1.0),
    ("DRUG_ALPRAZOLAM", "SE_ADDICTION_TOLERANCE", "CAUSES", "依赖风险", "反跳与戒断", 1.0),
    ("DRUG_DIAZEPAM", "SE_SEDATION", "CAUSES", "镇静与肌松", "日间残留嗜睡", 1.0),

    # 临床治疗常规连线
    ("DRUG_FLUOXETINE", "DIS_MDD", "TREATS", "一线治疗", "抑郁障碍", 1.0),
    ("DRUG_SERTRALINE", "DIS_MDD", "TREATS", "治疗", "抑郁障碍", 1.0),
    ("DRUG_SERTRALINE", "DIS_GAD", "TREATS", "治疗", "广泛性焦虑障碍", 1.0),
    ("DRUG_SERTRALINE", "DIS_PTSD", "TREATS", "一线治疗", "创伤后应激障碍", 1.0),
    ("DRUG_ESCITALOPRAM", "DIS_MDD", "TREATS", "一线治疗", "抑郁障碍", 1.0),
    ("DRUG_ESCITALOPRAM", "DIS_GAD", "TREATS", "一线治疗", "广泛性焦虑障碍", 1.0),
    ("DRUG_VENLAFAXINE", "DIS_MDD", "TREATS", "一线治疗", "抑郁障碍", 1.0),
    ("DRUG_VENLAFAXINE", "DIS_GAD", "TREATS", "一线治疗", "广泛性焦虑障碍", 1.0),
    ("DRUG_DULOXETINE", "DIS_MDD", "TREATS", "治疗", "抑郁伴躯体疼痛", 1.0),
    ("DRUG_MIRTAZAPINE", "DIS_MDD", "TREATS", "治疗", "伴失眠与食欲不振抑郁障碍", 1.0),
    ("DRUG_CLOZAPINE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "黄金标准", "难治性精神分裂症一线", 1.0),
    ("DRUG_OLANZAPINE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "一线治疗", "精神分裂症", 1.0),
    ("DRUG_OLANZAPINE", "DIS_BIPOLAR_MANIA", "TREATS", "一线治疗", "双相躁狂发作", 1.0),
    ("DRUG_RISPERIDONE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "一线治疗", "精神分裂症", 1.0),
    ("DRUG_QUETIAPINE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "治疗", "精神分裂症", 1.0),
    ("DRUG_QUETIAPINE", "DIS_BIPOLAR_MANIA", "TREATS", "一线治疗", "双相躁狂发作", 1.0),
    ("DRUG_QUETIAPINE", "DIS_BIPOLAR_DEP", "TREATS", "一线治疗", "双相抑郁发作 (单药获批)", 1.0),
    ("DRUG_QUETIAPINE", "DIS_MDD", "TREATS", "增效治疗", "难治性抑郁障碍辅助增效", 1.0),
    ("DRUG_ARIPIPRAZOLE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "治疗", "精神分裂症", 1.0),
    ("DRUG_ARIPIPRAZOLE", "DIS_BIPOLAR_MANIA", "TREATS", "治疗", "双相躁狂", 1.0),
    ("DRUG_ARIPIPRAZOLE", "DIS_MDD", "TREATS", "首选增效", "抑郁障碍辅助增效", 1.0),
    ("DRUG_BREXPIPRAZOLE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "一线治疗", "精神分裂症", 1.0),
    ("DRUG_BREXPIPRAZOLE", "DIS_MDD", "TREATS", "首选增效治疗", "抑郁障碍增效 (FDA批准)", 1.0),
    ("DRUG_BREXPIPRAZOLE", "DIS_TRD", "TREATS", "首选增效方案", "SDAM 机制一线增效", 2.2),
    ("DRUG_CARIPRAZINE", "DIS_SCHIZOPHRENIA_POS", "TREATS", "治疗", "精神分裂症阳性症状", 1.0),
    ("DRUG_CARIPRAZINE", "DIS_SCHIZOPHRENIA_NEG", "TREATS", "优势治疗", "基于 D3 机制显著改善阴性症状", 1.0),
    ("DRUG_CARIPRAZINE", "DIS_BIPOLAR_DEP", "TREATS", "一线治疗", "双相 I 型抑郁发作", 1.0),
    ("DRUG_CARIPRAZINE", "DIS_BIPOLAR_MANIA", "TREATS", "治疗", "双相躁狂发作", 1.0),

    ("DIS_MDD", "DIS_TRD", "CORRELATED_WITH", "慢性难治进展", "重度抑郁障碍发展为难治性抑郁", 2.0),
    ("DIS_MDD", "DIS_MDSI", "CORRELATED_WITH", "急性高危表型", "重度抑郁发作伴随急性自杀危机", 2.0),
    ("DIS_MDD", "DIS_PPD", "CORRELATED_WITH", "特异期发作", "围产期神经类固醇剧变引发", 2.0),
]

formatted_edges = [
    {"source": s, "target": t, "relationship": r, "label": l, "description": d, "weight": w}
    for s, t, r, l, d, w in edges_raw
]

# 查验孤立节点
all_node_ids = {n["id"] for n in all_nodes}
edge_nodes = set()
for e in formatted_edges:
    if e["source"] not in all_node_ids:
        print(f"Warning: Source not found: {e['source']}")
    if e["target"] not in all_node_ids:
        print(f"Warning: Target not found: {e['target']}")
    edge_nodes.add(e["source"])
    edge_nodes.add(e["target"])

isolated = all_node_ids - edge_nodes
if isolated:
    print(f"Error: Isolated nodes found: {isolated}")
else:
    print(f"All {len(all_nodes)} nodes are 100% connected! Total edges: {len(formatted_edges)}")

data = {"nodes": all_nodes, "edges": formatted_edges}
TARGET_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK! Full Comprehensive Graph successfully written to: {TARGET_JSON}")
