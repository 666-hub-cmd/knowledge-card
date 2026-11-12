# knowledge-card · 设计规范与调研记录

## 一、外部调研结论（2026-11-12，遵守「先调研开源生态再动手」铁律）

| 项目 | 结论 | 借鉴点 |
|---|---|---|
| emckenna/flash-cards (MIT) | 仅参考 | Markdown 结构化输入、一卡一概念 |
| alextanhongpin/go-flashcard | 仅参考 | AI 自动生成问答的思路 |
| lukas-brg/carddown (MIT) | 仅参考 | Markdown → 独立单页 HTML 的组装思路 |
| MarkoSagadin/Markdown2Anki (GPL) | 仅参考 | 图片自动导入、多主题 CSS 组织 |

共性结论：开源生态全是 **Anki/翻转问答卡**方向（背诵复习），没有「知识参考卡 · 手账排版 · 对比图批注 · 单页 HTML 交付」的同类项目 → 样式与组装逻辑自研，仅借鉴上述原则。不直接复制任何一方代码。

## 二、Handbook（手账风 · 默认）设计令牌

CSS 变量（见 assets/handbook-template.html）：

- 纸面 `--paper:#f7f1e3`，页外背景 `#e8e0cf` + 圆点网格 22px，页内网格 26px
- 墨色 `--ink:#3b3428`，弱化 `--ink-soft:#6b6250`
- 强调色：红 `#c0392b`（印章/VS/箭头）、蓝 `#3b6ea5`（页边批注）、绿 `#4a7c4e`（建议块）
- 荧光笔四色：y 黄 / p 粉 / g 绿 / b 蓝，用法 `<span class="hl y">…</span>`
- 字体栈：Kaiti SC / KaiTi / STKaiti / DFKai-SB / Noto Serif SC

## 三、元素清单（WorkBuddy 手写扩展组件时照此复用）

1. **装订孔** `.page::before` 左侧径向渐变竖排
2. **和纸胶带** `.tape` 半透明条纹渐变 + 旋转 ±2~5°，三种配色轮换
3. **印章** `.stamp` 双线红框 + 7° 旋转 + letter-spacing 6px；示例页必带「示 例」
4. **胶片边框** `.film` 黑底 + 上下齿孔（repeating-linear-gradient）+ frame-label 编号 №xx/xx
5. **参数对照条** `.params` 左右虚线框 + 旋转「VS」
6. **页边批注** `.margin-doodle` 蓝字 4° 旋转 + 红色 ⤶ 箭头，≤120px，移动端隐藏
7. **建议清单** `.tips` 绿色左边条 + ☐ 复选前缀
8. **小抄区** `.cheat` 虚线分隔 + 可选 SVG 图解

## 四、配图决策规则（成本开关）

| 内容性质 | 配图方式 | 成本 |
|---|---|---|
| 抽象概念 / 流程 / 关系 / 分类 | 内联 SVG 或纯排版（.svgwrap） | 0 积分 |
| 真实视觉对比：摄影参数、前后效果、产品质感、带货场景 | ImageGen 生成左右对比 diptych（1536x1024，一次一张） | 5-10 积分/张 |

铁律：凡走 ImageGen，**先报「张数 × 单价」等用户点头**，绝不默默生成。生成后用 PIL 压到 ≤1200px / JPEG q82（脚本自动做）再 base64 内嵌，单页控制在 1.5MB 内。

diptych 提示词要点（验证有效）：`side-by-side comparison diptych, split into two equal vertical halves with a thin white divider. SAME scene in both halves: … LEFT HALF: … RIGHT HALF: … consistent framing and composition across both halves, only X differs`——强调 same scene / consistent composition，否则两边构图对不上。

## 五、风格变体（用户可指定触发词切换）

- **handbook（默认）**：本文档全部令牌，脚本 + 内置模板直出，已实测。
- **minimal-card**：白底卡片网格、单一强调色、无装饰元素；保留胶片框可换为细边框图卡。改造方式：复制 handbook 模板，替换 `:root` 变量与 .tape/.stamp/.film 相关 CSS，卡片 HTML 结构不变（build_card.py `--template` 直接喂）。
- **collage（杂志拼贴）**：大号无衬线标题、撕纸边、旋转错位卡片、更大胆的撞色；卡片结构不变，只改皮肤。
- 新风格落地路径：写模板 HTML（保留 {{TITLE}}/{{CARDS}} 等占位符）→ build_card.py --template 挂载 → 实测一张再交付。

## 六、JSON Spec 完整字段

见 scripts/build_card.py 文件头 docstring（权威版本）。要点：
- 卡片字段全部可选（除 title），缺什么跳过什么，不渲染空块
- 图片字段 image 与 svg 二选一
- 高亮 HTML 直接写在 `*_html` 字段里，脚本不转义这些字段（其余文本自动转义）
