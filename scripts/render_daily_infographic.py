#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "verification-becomes-bottleneck-2026-09-08.png"
BACKGROUND = ASSETS / "verification-becomes-bottleneck-2026-09-08-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-08.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def put(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, lines, action, note=None):
    x, w, h = 58, 964, 178
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFEFC", outline="#DCD6CC", width=2)
    put(draw, (86, y + 24), no, 28, "#F2682A", True)
    put(draw, (148, y + 20), title, 25, bold=True)
    for idx, line in enumerate(lines):
        put(draw, (148, y + 60 + idx * 25), "• " + line, 16, "#343A3E")
    if note:
        put(draw, (840, y + 82), note, 12, "#73787A")
    draw.rounded_rectangle((140, y + 136, 986, y + 166), 8, fill="#FFF0E8")
    put(draw, (156, y + 141), "行动｜" + action, 15, "#B94210", True)


def main():
    bg = Image.open(BACKGROUND).convert("RGB")
    im = ImageOps.fit(bg, (1080, 1440), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((42, 28, 1038, 244), 22, fill="#FBF8F2", outline="#E4DDD2", width=2)
    put(draw, (66, 48), "海豚智脑", 28, bold=True)
    put(draw, (218, 53), "hub.smarphin.com", 17, "#74787A")
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.08", 18, "#F2682A", True)
    put(draw, (66, 140), "验证成为 AI 新瓶颈", 48, bold=True)
    put(draw, (68, 205), "生成更快之后，可信、边界与单位经济性决定价值", 20, "#555B5F")

    card(draw, 258, "01", "AI 研发加速快于可监控性", [
        "每个人类工作日对应约 3.1 个代理工作日",
        "成功的 4–8 小时任务过半仍需人工干预",
        "Astra 达关键级网络能力，书面推理更难监控",
    ], "自主时长与权限绑定可监控性门槛")
    card(draw, 446, "02", "代理把可写表面变成协作通道", [
        "独立调查记录约 1.8 万条帖子",
        "3700+ 个代理名称共享答案与绕过方法",
        "GET 请求也可能产生真实外部副作用",
    ], "按状态变化定义权限，并设披露阈值", "*研究者口径")
    card(draw, 634, "03", "评测脚手架让得分跃升 37.2 分", [
        "标准脚手架：62.7%，成本 26,098 美元",
        "Provider Adapter：99.9%，成本 18,817 美元",
        "记忆与上下文管理已成为系统能力",
    ], "同时报告模型、脚手架、成本与动作数")
    card(draw, 822, "04", "形式化验证追上 AI 生成速度", [
        "11 天完成费马大定理端到端 Lean 形式化",
        "约 1300 万行代码、60 亿输出 token",
        "独立内核检查 1,052,234 个声明无错误",
    ], "交付人类解释与机器可检验证据")
    card(draw, 1010, "05", "AI 收入增长接受毛利检验", [
        "研究估算年化收入约 2290 亿美元，同比增长 3.5 倍",
        "Snowflake 产品收入同比增长 37%",
        "AI 工作负载推动增长，毛利率指引降至 74%",
    ], "按工作流追踪贡献毛利与成功任务成本", "*行业收入为估算")

    draw.rounded_rectangle((58, 1202, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1230), "下一阶段，不是比谁生成得更多", 21, "#FFFFFF", True)
    put(draw, (86, 1268), "而是比谁能把能力变成可信且可持续的结果。", 17, "#D9DEDF")
    put(draw, (86, 1320), "来源：OpenAI · ARC Prize · Anthropic · Snowflake", 12, "#AEB6B9")
    put(draw, (86, 1343), "GitHub · SEC · Exponential View", 12, "#AEB6B9")
    put(draw, (86, 1368), "行业收入为研究机构估算", 11, "#8F989B")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1216))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
