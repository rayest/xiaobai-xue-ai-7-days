#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "evidence-over-answers-2026-09-15.png"
BACKGROUND = ASSETS / "evidence-over-answers-2026-09-15-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-15.png"
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
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.15", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 不只需要答案，更需要证据", 40, bold=True)
    put(draw, (68, 205), "证据、边界与判断成为生产价值", 20, "#555B5F")

    card(draw, 252, "01", "前沿治理走向可检查", [
        "外部评估者需要内部级访问能力",
        "30 天扫描发现约 35 项相关研究",
        "500+ 恶意包被清理，AI 归因未证实",
    ], "预设复核、披露与自动暂停门槛")
    card(draw, 436, "02", "AI 科研进入证明与溯源阶段", [
        "Navier–Stokes 项目约用一万个并发代理",
        "产生 270 万条消息、1300 亿输出 token",
        "Lean 验证不替代同行评议与贡献认定",
    ], "同时交付轨迹、证明和贡献时间线")
    card(draw, 620, "03", "长视频变成预算化证据搜索", [
        "动态调整帧率、分辨率与模态",
        "最高减少 88% token、降低 66% 成本",
        "基准准确率最高提升 7%",
    ], "组合采样、层级检索与按需重看")
    card(draw, 804, "04", "金融 AI 竞争转向可信数据层", [
        "内置 Daloopa、PitchBook、LSEG News",
        "数字和结论可回到具体表格与段落",
        "输出仍需独立专业判断",
    ], "把数据权利、引用和复核列为硬指标")
    card(draw, 988, "05", "构建变便宜，判断仍稀缺", [
        "AI 大幅降低原型与实现成本",
        "产品核心转向影响力与取舍",
        "更快建造需要更严格的删除标准",
    ], "用 AI 加速原型，不外包产品判断")

    draw.rounded_rectangle((58, 1178, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1206), "生成能力趋于普及", 21, "#FFFFFF", True)
    put(draw, (86, 1244), "证据、边界和判断才是生产价值。", 17, "#D9DEDF")
    put(draw, (86, 1318), "来源：Dario Amodei · Anthropic · RubyGems", 12, "#AEB6B9")
    put(draw, (86, 1341), "OpenAI · Google · a16z", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1202))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
