#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/infographics"
OUT = ASSETS / "ai-control-plane-2026-09-12.png"
BACKGROUND = ASSETS / "ai-control-plane-2026-09-12-background.png"
QR = ASSETS / "hub-smarphin-qr-2026-09-12.png"
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
    put(draw, (66, 101), "AI INTELLIGENCE · 2026.09.12", 18, "#F2682A", True)
    put(draw, (66, 140), "AI 进入控制平面竞争", 43, bold=True)
    put(draw, (68, 205), "规模化落地取决于成本、执行、来源与持续审计", 20, "#555B5F")

    card(draw, 258, "01", "低成本模型改写采购逻辑", [
        "每百万 token 有效价格较 3 月高点下降 41%",
        "企业开始把标准模型设为默认",
        "竞争单位转向完成一个可靠任务的总成本",
    ], "标准模型默认，前沿模型按风险升级")
    card(draw, 480, "02", "代理从聊天框进入执行环境", [
        "Agents API 提供托管 harness 与长时任务能力",
        "执行环境可选托管沙箱、自有基础设施或合作方",
        "自治越强，越需要终态、审批点和回滚边界",
    ], "把代理按有权限的执行者设计")
    card(draw, 702, "03", "内容真实性转向来源证明", [
        "SynthID 在生成时调整 token 采样概率",
        "在线实验覆盖近 2,000 万条 Gemini 响应",
        "C2PA 记录媒体来源与编辑历史",
    ], "保存来源链，检测分数只作线索")
    card(draw, 924, "04", "安全升级为持续轨迹审计", [
        "高能力模型的能力与可观测性可能不同步",
        "滥用规模不等于真实受众与实际影响",
        "完整轨迹、最小权限和自动阻断成为基础设施",
    ], "高权限代理必须全程可追踪、可中止")

    draw.rounded_rectangle((58, 1202, 1022, 1402), 20, fill="#252B2F")
    put(draw, (86, 1228), "真正可扩展的 AI", 21, "#FFFFFF", True)
    put(draw, (86, 1266), "要把成本、权限、来源与风险放进同一个控制平面。", 17, "#D9DEDF")
    put(draw, (86, 1324), "来源：Ramp · OpenAI · Google DeepMind", 12, "#AEB6B9")
    put(draw, (86, 1347), "Nature · C2PA · Anthropic", 12, "#AEB6B9")

    qr = Image.open(QR).convert("RGB").resize((174, 174), Image.Resampling.NEAREST)
    im.paste(qr, (817, 1216))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
