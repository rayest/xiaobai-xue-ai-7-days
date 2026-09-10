#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "ai-workflows-threshold-2026-09-10.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-10.png"
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


def background():
    im = Image.new("RGB", (1080, 1440), "#F4F0E7")
    draw = ImageDraw.Draw(im)
    for x in range(42, 1080, 58):
        draw.line((x, 0, x, 1440), fill="#EAE4DA", width=1)
    for y in range(34, 1440, 58):
        draw.line((0, y, 1080, y), fill="#ECE6DD", width=1)
    draw.line((26, 0, 26, 1440), fill="#F2682A", width=3)
    for cx, cy in [(1015, 84), (978, 116), (1030, 154), (994, 190)]:
        draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill="#E7B39C")
    draw.line((1015, 84, 978, 116, 1030, 154, 994, 190), fill="#E7B39C", width=2)
    for y in range(300, 1100, 36):
        draw.arc((12, y, 62, y + 60), 270, 90, fill="#E5BBA8", width=2)
        draw.arc((-12, y + 18, 38, y + 78), 90, 270, fill="#C9CED0", width=2)
    return im


def main():
    im = background()
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((42, 28, 1038, 244), 22, fill="#FBF8F2", outline="#E4DDD2", width=2)
    put(draw, (66, 48), "海豚智脑", 28, bold=True)
    put(draw, (218, 53), "hub.smarphin.com", 17, "#74787A")
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.10", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 工作流跨过实验门槛", 43, bold=True)
    put(draw, (68, 205), "验证、权限与单位任务成本成为新的系统瓶颈", 20, "#555B5F")

    card(draw, 258, "01", "多代理科研成为生产线", [
        "约 1 万个并发代理探索 Navier–Stokes 问题",
        "约 88 小时形成结果，17 小时完成 Lean 验证",
        "Clay 认定仍要求发表、两年等待与学界接受",
    ], "把探索、验证、复核和归属分开记录")
    card(draw, 480, "02", "基因数据库升级为预测地图", [
        "AlphaGenome Atlas 覆盖约 90 亿种单碱基变异",
        "约 1 PB 数据，同时覆盖编码区与非编码区",
        "预测用于科研排序，不能替代临床与实验确认",
    ], "先排序、再解释机制、最后独立验证")
    card(draw, 702, "03", "代理采用快于治理成熟度", [
        "Deloitte 调查覆盖 24 国、3235 名负责人",
        "仅 21% 称治理成熟，74% 预计 2027 年广泛采用",
        "写权限需要边界、人工确认、监控与审计链",
    ], "每增加一种工具，就同步增加四类控制")
    card(draw, 924, "04", "模型选择成为单位任务工程", [
        "Astra 支持 105 万上下文、12.8 万最大输出",
        "标准 API 的输出 token 单价是输入的 5 倍",
        "推测解码原始论文报告 2–3 倍加速",
    ], "按成功率、时延与单次完成成本路由")

    draw.rounded_rectangle((58, 1202, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1228), "AI 正从“生成答案”进入“运行流程”", 21, "#FFFFFF", True)
    put(draw, (86, 1266), "可信度由验证、权限与单位经济性共同决定。", 17, "#D9DEDF")
    put(draw, (86, 1324), "来源：OpenAI · Clay · Google DeepMind", 12, "#AEB6B9")
    put(draw, (86, 1347), "Deloitte · Meta · ICML / PMLR", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1216))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
