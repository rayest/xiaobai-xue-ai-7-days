#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "ai-systems-cross-boundaries-2026-09-07.png"
BACKGROUND = ASSETS / "ai-systems-cross-boundaries-2026-09-07-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-07.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def put(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, lines, action, note=None):
    x, w, h = 58, 964, 202
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFEFC", outline="#DCD6CC", width=2)
    put(draw, (86, y + 24), no, 28, "#F2682A", True)
    put(draw, (148, y + 22), title, 27, bold=True)
    for idx, line in enumerate(lines):
        put(draw, (148, y + 66 + idx * 28), "• " + line, 17, "#343A3E")
    if note:
        put(draw, (840, y + 92), note, 12, "#73787A")
    draw.rounded_rectangle((140, y + 158, 986, y + 190), 8, fill="#FFF0E8")
    put(draw, (156, y + 164), "行动｜" + action, 16, "#B94210", True)


def main():
    bg = Image.open(BACKGROUND).convert("RGB")
    im = ImageOps.fit(bg, (1080, 1440), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((42, 28, 1038, 244), 22, fill="#FBF8F2", outline="#E4DDD2", width=2)
    put(draw, (66, 48), "海豚智脑", 28, bold=True)
    put(draw, (218, 53), "hub.smarphin.com", 17, "#74787A")
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.07", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 系统开始跨越边界", 48, bold=True)
    put(draw, (68, 205), "竞争从模型能力转向权限、反馈、上下文与必要的人类思考", 20, "#555B5F")

    card(draw, 264, "01", "“只读”不等于没有副作用", [
        "旧 Wiki 可通过 GET 请求执行编辑",
        "Reuters 报道超过 1.5 万次代理编辑",
        "归属、规模与时间线仍待完整审查",
    ], "按状态变化测试权限，不只看动作名称")
    card(draw, 480, "02", "生产失败开始训练专用模型", [
        "低分轨迹经过批评、修复、重放与复评",
        "系统提示约从 6000 token 压至 1500",
        "特定负载测试端到端延迟下降约 38%",
    ], "先校准评估器，再自动生成训练数据", "*官方系统")
    card(draw, 696, "03", "专有上下文进入 2000+ 门店", [
        "Magic Apron 每月处理数百万个问题",
        "支持文字、语音、图片与多语言输入",
        "结合实时库存、过道与货架位置回答",
    ], "先打通实体、权限和时效，再加聊天入口")
    card(draw, 912, "04", "教育 AI 刻意保留思考摩擦", [
        "Koji 通过问题和提示引导，不直接交答案",
        "可读取并操作课程中的交互组件",
        "效果要看迁移与独立完成，不只看完成率",
    ], "测提示依赖、延迟后测与独立解决能力")

    draw.rounded_rectangle((58, 1140, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1170), "最强的 AI 系统，不只是更聪明", 22, "#FFFFFF", True)
    put(draw, (86, 1210), "它知道哪里不能越界、如何从失败学习，", 18, "#D9DEDF")
    put(draw, (86, 1239), "以及何时不替人思考。", 18, "#D9DEDF")
    put(draw, (86, 1295), "来源：Shopify · Home Depot · Google Cloud", 13, "#AEB6B9")
    put(draw, (86, 1320), "Brilliant · NCES · Reuters", 13, "#AEB6B9")
    put(draw, (86, 1354), "厂商指标均为特定系统；事件归属仍待完整审查", 12, "#8F989B")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1182))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
