# Design QA

## 比较目标与证据

- Source visual truth（改造前基线）:
  - `output/design-audit/2026-09-02/01-baseline-desktop.png`
  - `output/design-audit/2026-09-02/02-baseline-mobile.png`
- Rendered implementation（最终构建）:
  - `output/design-audit/2026-09-02/21-redesign-desktop-final.png`
  - `output/design-audit/2026-09-02/20-redesign-mobile-final.png`
  - `output/design-audit/2026-09-02/22-redesign-mobile-open-final.png`
- Full-view comparison evidence:
  - `output/design-audit/2026-09-02/comparison-desktop.png`
  - `output/design-audit/2026-09-02/comparison-mobile.png`
- Focused region comparison evidence:
  - `output/design-audit/2026-09-02/comparison-desktop-sidebar.png`
- Route: `http://127.0.0.1:4173/`
- Theme/state: 深色主题；桌面端为默认“艾司氯胺酮单点级联探索”；移动端比较默认折叠状态，并另查展开状态。
- Desktop viewport: `1440 × 1000 CSS px`；source 与 implementation 均为 `1440 × 1000 px`；`deviceScaleFactor = 1`，无需密度归一化。
- Mobile viewport: `390 × 844 CSS px`；source 与 implementation 均为 `390 × 844 px`；`deviceScaleFactor = 1`，无需密度归一化。
- 说明：这是现有产品的主动重设计，不以逐像素复刻旧页面为目标；比较判断的是核心内容保留、信息层级、可读性、响应式和交互质量是否得到提升。

## Findings

- 未发现仍需处理的 P0、P1 或 P2 视觉/交互问题。
- [P3] 3D 依赖仍由外部 CDN 加载，浏览器控制台会出现 Three.js 旧式脚本与多实例警告；当前无运行错误，主流程正常。后续可改为锁定版本的本地 ESM 打包，以提升离线能力并消除警告。

## 必查保真面

- Fonts and typography: 标题、正文和数据文案已拆分为稳健的系统字体栈；中文回退覆盖 `Noto Sans SC`、`PingFang SC`、`Microsoft YaHei`，字重、行高与小字号密度在桌面及移动端均可读。MyFonts 未找到可直接采用且适配当前中文界面的匹配字体，因此未引入商业字体依赖。
- Spacing and layout rhythm: 桌面侧栏由 480px 收敛至 420px，段落、筛选器、布局按钮和详情卡形成稳定节奏；移动端改为图谱优先、按需打开的底部面板，390/768/1024/1440px 均无控件遮挡或主任务阻断。
- Colors and visual tokens: 将高饱和霓虹收敛为深海军蓝底、低亮度边界和受控青蓝强调色；选中态、分类色和焦点环具有一致语义，并保留足够对比度。
- Image quality and asset fidelity: 沿用真实项目资产，没有用 CSS/内联 SVG/占位图伪造可见素材；移除了“赖右苯丙胺错误复用右哌甲酯结构式”的映射，缺少专属素材时回退为中性分类图。
- Copy and content: 保留 187 个节点、384 条关系与全部关系说明；搜索、空结果、模式状态和移动面板文案已校正；“卢美哌隆”术语保持一致，未出现旧称误写。
- Icons and controls: 核心图标继续使用现有真实资源；点击式 `div/span` 已改为原生按钮，选中态与 `aria-pressed` 同步。
- Accessibility and motion: 提供可折叠节点/关系文本等价视图、真实搜索标签、状态播报、详情焦点返回、Escape 关闭、移动端 inert 管理、可见 focus ring、forced-colors 回退与 reduced-motion 分支。reduced-motion 下连线粒子为 0、动画时长约为 0。

## 比较与修正历史

### Pass 1 — 基线审计

- [P1] 旧移动布局固定显示宽侧栏，390px 下图谱主体无法正常到达。
  - Fix: 在 900px 以下采用图谱优先布局；探索面板改为可开合底部面板，关闭时设置 `inert` 与 `aria-hidden`。
  - Post-fix evidence: `04-redesign-mobile-closed-v1.png`、`05-redesign-mobile-open-v1.png`。
- [P2] 旧桌面节点标牌过大，左右边缘存在明显截断，疾病节点标签互相压叠。
  - Fix: 收紧 SpriteText 尺寸，按可用画布宽度调整相机距离，增加力导向间距，并将较长疾病标签置于节点上方。
  - Post-fix evidence: `12-redesign-desktop-final.png`。
- [P2] 专题、类别、布局与关闭等控件依赖不可聚焦的 `div/span`，搜索每次输入即触发相机移动，状态缺失。
  - Fix: 改用原生按钮与显式搜索提交；同步选中状态，增加成功/失败播报和文本等价视图。
  - Post-fix evidence: 浏览器可访问树与交互测试通过。

### Pass 2 — 响应式与焦点复核

- [P2] 第一版移动端关闭面板后标签仍接近边缘，展开面板后键盘焦点没有进入面板。
  - Fix: 将相机距离改为按画布宽度计算并设安全上限；用户主动展开时将焦点移至搜索框，折叠前将焦点移回面板开关。
  - Post-fix evidence: `20-redesign-mobile-final.png`、`22-redesign-mobile-open-final.png`。
- [P2] 搜索定位后 Escape 的返回焦点可能落在无 ID 的提交按钮，动态详情链接重建时也可能失去原触发项。
  - Fix: 搜索路径显式记录 `search-input`；动态节点按钮增加稳定 `data-node-id`，断开时优先聚焦重建后的同一节点，并用 `scrollIntoView({ block: 'nearest' })` 保持可见；移动端 inert 状态回退至图谱主区域。
  - Post-fix evidence: 实测搜索 Escape 后活动元素为 `search-input`；动态重建后返回 `DIS_MDSI` 的同名节点按钮，按钮仍在侧栏可视区域内。
- [P2] 全景模式的 384 条关系使用内部滚动区域，但列表本身不可聚焦，纯键盘无法稳定滚动完整证据。
  - Fix: 为关系列表增加 `tabindex="0"`，沿用统一 `focus-visible` 样式并保留 `aria-labelledby`。
  - Post-fix evidence: 关系列表可被键盘聚焦并独立滚动。

### Pass 3 — 最终同屏比较

- 桌面 full-view、桌面侧栏 focused region、移动端 full-view 已分别在同一比较图中审阅。
- 最终桌面标签完整，侧栏层级清楚；移动端默认可直接看到图谱，面板打开后搜索框焦点环清晰。
- 未发现新的 P0/P1/P2 差异，因此无需继续视觉修正。

## Primary interactions tested

- 搜索成功与无结果反馈。
- Escape 关闭详情并返回搜索框。
- 六类实体筛选及筛选计数。
- 自由星群、同心分层、机制柱阵三种布局。
- 187 节点 / 384 关系全景模式。
- 自动巡航开/关状态。
- 移动探索面板展开、折叠、`inert` 与焦点迁移。
- reduced-motion 模式下粒子与过渡抑制。
- 可访问节点列表与完整关系证据列表。
- 浏览器 console errors: `0`；仅保留前述非阻断 Three.js warnings。

## Implementation Checklist

- [x] 修正桌面信息层级、色彩与标签尺度。
- [x] 完成移动端图谱优先响应式布局。
- [x] 完成键盘、读屏、焦点、减弱动效和高对比模式支持。
- [x] 统一生成器、根目录、docs、dist、dist_lite 与 ZIP 产物。
- [x] 发布资产按页面引用严格白名单打包。

final result: passed
