#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "ai-operating-models-2026-09-14.png"
BACKGROUND = ASSETS / "ai-operating-models-2026-09-14-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-14.png"
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
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.14", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 系统需要新的运行体系", 41, bold=True)
    put(draw, (68, 205), "记忆、岗位、开放与治理成为生产竞争力", 20, "#555B5F")

    card(draw, 252, "01", "长上下文进入内存经济学", [
        "V4.1 Flash 为 552B MoE 主干",
        "输入仅激活 8B，输出激活 16B 参数",
        "竞争点转向缓存、检索与恢复成本",
    ], "压测真实长任务，再决定上下文策略")
    card(draw, 436, "02", "代理管理开始像岗位设计", [
        "每个代理对应岗位、技能、经理和预算",
        "发现、执行、审批拆成不同角色",
        "不确定性升级给人，而不是继续猜测",
    ], "把升级条件写成系统规则")
    card(draw, 620, "03", "开放模型不是二选一题", [
        "模型发布至少存在六级访问梯度",
        "权重开放不等于数据、代码、许可全开放",
        "部署控制权与短期性能是两条决策轴",
    ], "按五个维度审查开放程度")
    card(draw, 804, "04", "安全转向系统级协作", [
        "真实滥用跨越网络攻击、影响行动与监控",
        "最终答案不足以覆盖长链路代理风险",
        "完整轨迹、独立评估与威胁共享缺一不可",
    ], "高权限代理必须可追踪、可中止")
    card(draw, 988, "05", "脑图开放不等于数字生命", [
        "果蝇连接图含 16.6 万+神经元",
        "记录 1.25 亿个突触连接",
        "结构地图不包含记忆或意识",
    ], "区分结构、动力学与学习机制")

    draw.rounded_rectangle((58, 1178, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1206), "更强模型只是起点", 21, "#FFFFFF", True)
    put(draw, (86, 1244), "可靠运行体系才是生产竞争力。", 17, "#D9DEDF")
    put(draw, (86, 1318), "来源：DeepSeek · Brex · FAccT", 12, "#AEB6B9")
    put(draw, (86, 1341), "OpenAI · Anthropic · Google Research", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1202))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
