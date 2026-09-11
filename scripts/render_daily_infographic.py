#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "verifiable-operations-2026-09-11.png"
BACKGROUND = ASSETS / "verifiable-operations-2026-09-11-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-11.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def put(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, lines, action):
    x, w, h = 58, 964, 212
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFEFC", outline="#DCD6CC", width=2)
    put(draw, (86, y + 24), no, 28, "#F2682A", True)
    put(draw, (148, y + 20), title, 25, bold=True)
    for idx, line in enumerate(lines):
        put(draw, (148, y + 60 + idx * 25), "• " + line, 16, "#343A3E")
    draw.rounded_rectangle((140, y + 169, 986, y + 199), 8, fill="#FFF0E8")
    put(draw, (156, y + 174), "行动｜" + action, 15, "#B94210", True)


def main():
    im = Image.open(BACKGROUND).convert("RGB").resize((1080, 1440), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
    ImageDraw.Draw(overlay).rectangle((0, 0, 1080, 1440), fill=(244, 240, 231, 74))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((42, 28, 1038, 244), 22, fill="#FBF8F2", outline="#E4DDD2", width=2)
    put(draw, (66, 48), "海豚智脑", 28, bold=True)
    put(draw, (218, 53), "hub.smarphin.com", 17, "#74787A")
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.11", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 系统进入可验证运营期", 43, bold=True)
    put(draw, (68, 205), "真正的分水岭：接口、证据、审计与风险边界", 20, "#555B5F")

    card(draw, 258, "01", "代理接口为可验证执行重构", [
        "MCP 新版移除会话握手，每次请求携带完整上下文",
        "OpenDiscoveryTrace 记录 558 条完整科学代理轨迹",
        "相近成功率仍可能掩盖 30 倍的错误数差异",
    ], "把机器可判定的成功条件设计成接口契约")
    card(draw, 480, "02", "企业学习从完课转向能力证据", [
        "Project Helix 用自然语言生成自适应学习路径",
        "路径映射岗位、技能与组织数据，而非只推荐课程",
        "重点从完成徽章转向能否把知识用于真实工作",
    ], "用岗位任务与可验证产出定义学习成效")
    card(draw, 702, "03", "AI 安全从概率口号回到事故审计", [
        "Anthropic 扩大扫描约 4.81 亿条记录并确认第 4 起事故",
        "官方强调这些是受控网络评测，不等于现实自主攻击",
        "新增监控、环境加固与第三方评测准入要求",
    ], "用事故证据、触发条件和缓解措施讨论风险")
    card(draw, 924, "04", "AI 开始进入强监管后台流程", [
        "美国雇主医疗保险覆盖约 1.54 亿名 65 岁以下人群",
        "2025 年家庭保费同比上升 6%，成本压力持续",
        "AI 可降客服与理赔管理成本，但不能替代责任边界",
    ], "先自动化低风险环节，再逐步扩大决策权限")

    draw.rounded_rectangle((58, 1202, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1228), "真正可扩展的 AI，不只会回答", 21, "#FFFFFF", True)
    put(draw, (86, 1266), "还要让每一步可判定、可证明、可追溯。", 17, "#D9DEDF")
    put(draw, (86, 1324), "来源：MCP · Apify · arXiv · Coursera", 12, "#AEB6B9")
    put(draw, (86, 1347), "Anthropic · KFF · a16z", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1216))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
