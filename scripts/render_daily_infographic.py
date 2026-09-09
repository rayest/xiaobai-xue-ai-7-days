#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "agent-institutions-2026-09-09.png"
BACKGROUND = ASSETS / "agent-institutions-2026-09-09-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-09.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def put(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, lines, action, note=None):
    x, w, h = 58, 964, 212
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFEFC", outline="#DCD6CC", width=2)
    put(draw, (86, y + 24), no, 28, "#F2682A", True)
    put(draw, (148, y + 20), title, 25, bold=True)
    for idx, line in enumerate(lines):
        put(draw, (148, y + 60 + idx * 25), "• " + line, 16, "#343A3E")
    if note:
        put(draw, (840, y + 82), note, 12, "#73787A")
    draw.rounded_rectangle((140, y + 169, 986, y + 199), 8, fill="#FFF0E8")
    put(draw, (156, y + 174), "行动｜" + action, 15, "#B94210", True)


def main():
    bg = Image.open(BACKGROUND).convert("RGB")
    im = ImageOps.fit(bg, (1080, 1440), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((42, 28, 1038, 244), 22, fill="#FBF8F2", outline="#E4DDD2", width=2)
    put(draw, (66, 48), "海豚智脑", 28, bold=True)
    put(draw, (218, 53), "hub.smarphin.com", 17, "#74787A")
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.09", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 系统需要制度", 48, bold=True)
    put(draw, (68, 205), "共享空间、复用流程、许可与证据决定上限", 20, "#555B5F")

    card(draw, 258, "01", "共享记忆既协作，也传播失范", [
        "100 个自治代理协作证明形式化数学猜想",
        "漏洞经共享知识库与点对点消息扩散",
        "举报代理需要可执行的隔离与制裁机制",
    ], "增加来源、撤销、争议和制裁状态")
    card(draw, 480, "02", "工作流从提示升级为组件", [
        "Agent Plugins 1.0 打包技能与 MCP 服务",
        "同一插件可跨多个兼容客户端复用",
        "Stacked PR 把大改动拆成可审查的层",
    ], "只固化验收稳定的任务，锁定版本权限")
    card(draw, 702, "03", "开放权重不等于开放许可", [
        "GLM-5.3 可下载，但使用专用许可证",
        "GLM-5.3-Flash 官方模型卡标注 MIT",
        "同一模型家族也可能有不同商用边界",
    ], "按精确 checkpoint 与许可版本审查")
    card(draw, 924, "04", "AI 药物信号仍需解释边界", [
        "12 周 IIa 期试验，42 人进入蛋白质组分析",
        "六种衰老时钟均检测到预测年龄下降",
        "时钟无法彻底拆分衰老调节与疾病改善",
    ], "把生物标志物视为信号，不视为结论")

    draw.rounded_rectangle((58, 1202, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1228), "代理时代的核心资产，不是更长的提示", 21, "#FFFFFF", True)
    put(draw, (86, 1266), "而是能治理复用、许可与证据的一套制度。", 17, "#D9DEDF")
    put(draw, (86, 1324), "来源：arXiv · GitHub · Z.ai / Hugging Face", 12, "#AEB6B9")
    put(draw, (86, 1347), "Nature Biotechnology", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1216))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
