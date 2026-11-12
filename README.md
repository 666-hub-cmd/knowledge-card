# knowledge-card · 手账知识卡工厂

把任意资料（粘贴文字 / md / docx / pdf / xlsx…）整理成**手账风格知识卡单页 HTML**：
紧凑分区 · 荧光笔重点批注 · 胶片边框对比图 · 参数标注 · 建议清单，图片 base64 内嵌、双击即开、离线可用。

> 一句话：给「知识沉淀」一个愿意被打开的样子。

## 效果示例

| 手账知识卡（摄影入门示例） |
|---|
| ![screenshot](docs/screenshot.png) |
| ▲ 三张 AI 对比图（光圈虚实 / 快门动静 / ISO 噪点）+ 曝光三角小抄 |

（截图待补：跑一遍示例后截取页面顶部即可）

## 特性

- **单文件交付**：所有图片压缩后 base64 内嵌，一个 HTML 走天下
- **确定性组装**：`build_card.py` 读 JSON spec 渲染，不靠模型手写整页 HTML，跑 100 次排版不走样
- **配图成本可控**：抽象概念走内联 SVG（0 成本），真实视觉对比才调生图（每张 5-10 积分级成本），策略内置于 SKILL.md
- **换肤不换骨架**：内置 handbook（手账）/ minimal-card（简约）/ collage（杂志拼贴）三种风格，卡片结构统一，模板替换即可
- **一卡一概念**：每张卡片 = 一句话总结 + 对比图/图解 + 参数对照 + 批注 + 可执行建议

## 安装（WorkBuddy）

把本目录拷到 `~/.workbuddy/skills/knowledge-card/`，重启会话即可。
触发词：知识卡、手账知识卡、把资料整理成卡片。

## 快速上手

1. 写一份 spec.json（字段见 `scripts/build_card.py` 文件头 docstring）：

```json
{
  "title": "📷 主题名 · 知识手账",
  "subtitle": "一句话副标题",
  "stamp": "示 例",
  "cards": [{
    "title": "概念名 —— 副题",
    "oneliner_html": "一句话总结，<span class=\"hl y\">重点用荧光笔</span>",
    "svg": "<svg>…图解…</svg>",
    "params": {"left_b": "A", "left_desc": "…", "right_b": "B", "right_desc": "…"},
    "note_html": "为什么会这样…",
    "tips": ["可执行建议 1", "建议 2"]
  }]
}
```

2. 组装：

```bash
python scripts/build_card.py spec.json --out my_card.html
```

3. 完成。图片字段填本地路径会自动压缩并内嵌；不填图填 `svg` 则零成本图解。

## 目录结构

```
knowledge-card/
├── SKILL.md                      # Agent 使用说明（触发词/决策树/成本铁律）
├── scripts/build_card.py         # 组装器（spec + 图片 → 单页 HTML）
├── assets/handbook-template.html # 手账风页面骨架（全部 CSS）
└── references/design-spec.md     # 设计令牌 / 元素清单 / 对比图提示词模板 / 风格改造路径
```

## 适用与不适用

✅ 个人知识沉淀、读书笔记、教程卡片、产品说明、团队 SOP 展示
❌ 需要背诵复习的场景 → 请用 Anki / 翻转问答卡类工具（开源调研见 design-spec.md）

## License

MIT（见 LICENSE）

## Roadmap

- [ ] minimal-card / collage 模板实体化（当前为改造路径文档）
- [ ] Markdown 转入 → 自动生成 spec.json
- [ ] 深色手账（牛皮纸）主题
