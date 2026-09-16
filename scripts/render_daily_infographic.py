#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "systems-competition-2026-09-16.png"
BACKGROUND = ASSETS / "systems-competition-2026-09-16-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-16.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def put(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, lines, action):
    x, w, h = 58, 964, 174
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFEFC", outline="#DCD6CC", width=2)
    put(draw, (86, y + 22), no, 26, "#F2682A", True)
    put(draw, (148, y + 18), title, 23, bold=True)
    for idx, line in enumerate(lines):
        put(draw, (148, y + 52 + idx * 22), "• " + line, 15, "#343A3E")
    draw.rounded_rectangle((140, y + 134, 986, y + 162), 8, fill="#FFF0E8")
    put(draw, (156, y + 138), "行动｜" + action, 14, "#B94210", True)


def main():
    im = Image.open(BACKGROUND).convert("RGB").resize((1080, 1440), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
    ImageDraw.Draw(overlay).rectangle((0, 0, 1080, 1440), fill=(244, 240, 231, 74))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((42, 28, 1038, 244), 22, fill="#FBF8F2", outline="#E4DDD2", width=2)
    put(draw, (66, 48), "海豚智脑", 28, bold=True)
    put(draw, (218, 53), "hub.smarphin.com", 17, "#74787A")
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.16", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 竞争正在变成系统竞争", 40, bold=True)
    put(draw, (68, 205), "控制、学习与基础设施决定真实能力", 20, "#555B5F")

    card(draw, 252, "01", "控制规则变成可测试规格", [
        "人类控制被写入模型最高目标",
        "权限、暂停和关闭形成明确控制链",
        "当前仍是咨询草案，并非现行能力",
    ], "把权限继承与越权测试写入验收")
    card(draw, 436, "02", "能力曲线要连同边界一起读", [
        "2024 年以来 50% 时间跨度约 89 天翻倍",
        "长期趋势更接近每 6–7 个月翻倍",
        "超过 16 小时测量不可靠，任务域有限",
    ], "同步标注任务域、成功率和置信区间")
    card(draw, 620, "03", "学习过程成为优化对象", [
        "递归改进路线图分为五级自治",
        "RLT 让隐藏状态跨 token 循环延续",
        "路线图与技术报告都不是规模化验证",
    ], "区分提案、实验和生产收益")
    card(draw, 804, "04", "连接组进入具身接口", [
        "脑与腹神经索连接组约含一亿突触",
        "开源实验接入 166,700 个神经元数据",
        "传感器与运动解码仍由工程接口决定",
    ], "检查接口假设、对照与可复现性")
    card(draw, 988, "05", "算力合同也是融资结构", [
        "六年 GPU 服务订单上限约 137 亿美元",
        "第三批交付仍附带客户审查条件",
        "50,808,408 股权证与实际采购挂钩",
    ], "拆开订单、交付条件与客户归因")

    draw.rounded_rectangle((58, 1178, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1206), "真正拉开差距的", 21, "#FFFFFF", True)
    put(draw, (86, 1244), "是把模型连接成可验证系统的能力。", 17, "#D9DEDF")
    put(draw, (86, 1318), "来源：Microsoft AI · METR · arXiv", 12, "#AEB6B9")
    put(draw, (86, 1341), "Nature · SEC", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1202))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
