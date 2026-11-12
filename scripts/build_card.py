# -*- coding: utf-8 -*-
"""knowledge-card · 手账风格知识卡组装脚本

用法:
    python build_card.py spec.json --out 输出.html [--template 模板.html]

spec.json 结构 (所有字段除 cards 外均可省略):
{
  "title": "页面主标题",
  "subtitle": "副标题一句话",
  "date": "2026-11-12",            // 省略则自动取今天
  "tags": "标签文本",               // 拼进日期行
  "stamp": "示 例",                 // 省略则不渲染印章；正式交付可留空
  "stamp_note": "↖ 说明文字",
  "film_label": "KODAK COLORPLUS 200 · 35mm",  // 胶片框左下标注, 可省
  "cheat": {"title": "小抄标题", "lines": ["<b>xx</b>：yy", ...], "svg": "<svg...>"},
  "foot": "页脚文字",
  "cards": [{
      "title": "卡片标题",
      "oneliner_html": "一句话总结, 可含 <span class=\"hl y\">高亮</span>",
      "image": "图片路径(可选, 与 svg 二选一)",
      "svg": "<svg...>(可选)",
      "image_alt": "alt 文本",
      "params": {"left_b": "f/1.8", "left_desc": "说明", "right_b": "f/11", "right_desc": "说明"},
      "doodle": "页边手写批注(可选)",
      "note_html": "✏️ 批注段落, 可含高亮",
      "tips": ["建议1", "建议2"]
  }]
}
"""
import argparse, base64, datetime, html, io, json, os, sys

try:
    from PIL import Image
except ImportError:
    PIL_OK = False
else:
    PIL_OK = True

TAPE_COMBOS = [("", ""), ("t2", ""), ("t3", ""), ("", "t2"), ("t3", "t2"), ("", "t3")]


def image_to_b64(path: str) -> str:
    if not PIL_OK:
        raise SystemExit("需要 Pillow: pip install pillow")
    if not os.path.isfile(path):
        raise SystemExit(f"图片不存在: {path}")
    im = Image.open(path).convert("RGB")
    im.thumbnail((1200, 800))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def render_media(card: dict, film_label: str, idx: int, total: int) -> str:
    no = f"№ {idx:02d} / {total:02d}"
    if card.get("image"):
        src = "data:image/jpeg;base64," + image_to_b64(card["image"])
        alt = html.escape(card.get("image_alt") or card.get("title", ""))
        mid = f'<img src="{src}" alt="{alt}">'
    elif card.get("svg"):
        mid = f'<div class="svgwrap">{card["svg"]}</div>'
    else:
        return ""
    return (
        '<div class="film">\n      <div class="holes"></div>\n'
        f"      {mid}\n"
        f'      <div class="frame-label"><span>{html.escape(film_label)}</span><span>{no}</span></div>\n'
        '      <div class="holes"></div>\n    </div>'
    )


def render_params(p: dict) -> str:
    if not p:
        return ""
    return (
        '<div class="params">\n'
        f'      <div class="p"><b>{html.escape(p.get("left_b",""))}</b> {html.escape(p.get("left_desc",""))}</div>\n'
        '      <div class="vs">VS</div>\n'
        f'      <div class="p"><b>{html.escape(p.get("right_b",""))}</b> {html.escape(p.get("right_desc",""))}</div>\n'
        "    </div>"
    )


def render_card(card: dict, idx: int, total: int, film_label: str) -> str:
    no = idx + 1
    tape_a, tape_b = TAPE_COMBOS[idx % len(TAPE_COMBOS)]
    parts = [f'  <div class="card">']
    if tape_a:
        parts.append(f'    <div class="tape {tape_a}"></div>')
    if tape_b:
        parts.append(f'    <div class="tape {tape_b}"></div>')
    parts.append(f'    <h2><span class="no">{no}</span>{html.escape(card.get("title",""))}</h2>')
    if card.get("oneliner_html"):
        parts.append(f'    <div class="oneliner">一句话：{card["oneliner_html"]}</div>')
    media = render_media(card, card.get("film_label") or film_label, idx + 1, total)
    if media:
        parts.append("    " + media)
    parts.append("    " + render_params(card.get("params")))
    if card.get("doodle"):
        parts.append(
            f'    <div class="margin-doodle md-{no}">{html.escape(card["doodle"])}'
            f'<span class="arr">⤶</span></div>'
        )
    if card.get("note_html"):
        parts.append(f'    <p class="note">✏️ 批注：{card["note_html"]}</p>')
    tips = card.get("tips")
    if tips:
        lis = "\n".join(f"        <li>{html.escape(t)}</li>" for t in tips)
        parts.append(
            '    <div class="tips">\n      <h3>📌 要点 / 建议</h3>\n      <ul>\n'
            f"{lis}\n      </ul>\n    </div>"
        )
    parts.append("  </div>")
    return "\n".join(parts)


def render_cheat(cheat: dict) -> str:
    if not cheat:
        return ""
    svg = cheat.get("svg", "")
    lines = "\n".join(f"      <p>{ln}</p>" for ln in cheat.get("lines", []))
    title = html.escape(cheat.get("title", "一页小抄"))
    return (
        '  <div class="cheat">\n'
        f"    {svg}\n"
        '    <div class="txt">\n'
        f"      <h3>🔖 {title}</h3>\n{lines}\n    </div>\n  </div>"
    )


def main():
    ap = argparse.ArgumentParser(description="手账风格知识卡组装器")
    ap.add_argument("spec", help="spec.json 路径")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    ap.add_argument("--template", default=None, help="自定义模板(默认用技能内置 handbook 模板)")
    args = ap.parse_args()

    skill_assets = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    template_path = args.template or os.path.join(skill_assets, "handbook-template.html")
    tpl = open(template_path, encoding="utf-8").read()

    spec = json.load(open(args.spec, encoding="utf-8"))
    cards = spec.get("cards", [])
    if not cards:
        raise SystemExit("spec.cards 为空")

    film_label = spec.get("film_label", "KODAK COLORPLUS 200 · 35mm")
    cards_html = "\n\n".join(render_card(c, i, len(cards), film_label) for i, c in enumerate(cards))

    stamp = spec.get("stamp", "")
    stamp_html = ""
    if stamp:
        note = spec.get("stamp_note", "")
        stamp_html = (
            f'    <div class="stamp">{html.escape(stamp)}</div>\n'
            + (f'    <div class="stamp-note">{html.escape(note)}</div>\n' if note else "")
        ).rstrip("\n")

    date = spec.get("date") or datetime.date.today().isoformat()
    tags = spec.get("tags", "")
    date_line = f'日期：<b>{html.escape(date)}</b>　|　{html.escape(tags)} ✂️ - - - - - -' if tags else f"日期：<b>{html.escape(date)}</b>"

    out = (
        tpl.replace("{{TITLE}}", html.escape(spec.get("title", "知识手账")))
        .replace("{{SUBTITLE}}", html.escape(spec.get("subtitle", "")))
        .replace("{{STAMP_HTML}}", stamp_html)
        .replace("{{DATE_LINE}}", date_line)
        .replace("{{CARDS}}", cards_html)
        .replace("{{CHEAT}}", render_cheat(spec.get("cheat")))
        .replace("{{FOOT}}", spec.get("foot", ""))
    )

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    open(args.out, "w", encoding="utf-8").write(out)
    print(f"[OK] {args.out} ({os.path.getsize(args.out)//1024} KB, {len(cards)} 张卡片)")


if __name__ == "__main__":
    main()
