#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/infographics/verifiable-reusable-ai-2026-09-06.png"
QR = ROOT / "assets/infographics/hub-smarphin-qr-2026-09-06.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def text(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, line1, line2, line3, action, note=None):
    x, w, h = 58, 964, 172
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFFFF", outline="#DDD8CF", width=2)
    text(draw, (86, y + 24), no, 28, "#F2682A", True)
    text(draw, (148, y + 22), title, 27, bold=True)
    text(draw, (148, y + 60), line1, 18)
    text(draw, (148, y + 88), line2, 18)
    text(draw, (600, y + 88), line3, 17)
    if note:
        text(draw, (840, y + 92), note, 12, "#73787A")
    draw.rounded_rectangle((140, y + 126, 986, y + 158), 8, fill="#FFF0E8")
    text(draw, (156, y + 132), "行动｜" + action, 16, "#B94210", True)


def main():
    im = Image.new("RGB", (1080, 1440), "#F7F4EE")
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, 18, 1440), fill="#F2682A")

    # Low-contrast editorial grid and technical motifs stay outside copy zones.
    for gx in range(60, 1060, 80):
        draw.line((gx, 0, gx, 1440), fill="#EEEAE3", width=1)
    for gy in range(0, 1440, 80):
        draw.line((18, gy, 1080, gy), fill="#EEEAE3", width=1)
    draw.arc((900, 22, 1090, 212), 100, 260, fill="#E5B49A", width=3)
    draw.line((936, 85, 1036, 85), fill="#E5B49A", width=3)

    text(draw, (66, 45), "海豚智脑", 28, bold=True)
    text(draw, (218, 50), "hub.smarphin.com", 17, "#74787A")
    text(draw, (66, 105), "AI INTELLIGENCE · 2026.09.06", 18, "#F2682A", True)
    text(draw, (66, 145), "AI 进入可验证、可复用阶段", 48, bold=True)
    text(draw, (68, 208), "真正的落地，不只看模型能力，还要看验证、环境与生产路径", 21, "#555B5F")

    card(draw, 254, "01", "AI 产出开始附带机器验证",
         "Claude：11 天完成费马大定理 Lean 形式化",
         "约 1300 万行 Lean；29,500 个中间定理",
         "约 60 亿输出 token*",
         "把测试、证明与依赖追踪纳入交付物", "*官方披露")
    card(draw, 440, "02", "一条轨迹可以重建训练环境",
         "Terminal-Universe：37.3k 个任务充分环境",
         "单轮基准 +11.9 分",
         "多轮基准 +13.8 分*",
         "保存原始状态、工具结果和可执行验证", "*特定设置")
    card(draw, 626, "03", "高频提示词可以先“编译”",
         "自然语言规范转成可保存的本地神经函数",
         "特定难集：83.6% 语义准确率",
         "编译约 1 分钟",
         "只编译高频、稳定、可测试的任务")
    card(draw, 812, "04", "企业试点卡在系统，不只卡模型",
         "74% 计划增加 AI 预算",
         "83% 把不到一半试点转入生产",
         "集成是首要阻碍",
         "记录采用率、集成工时与业务结果")
    card(draw, 998, "05", "手表成为环境式 AI 入口",
         "点击手表即可记录现场对话",
         "绿色界面与声音提示状态",
         "需要 watchOS 11+",
         "明确同意、快速停止、最短保留、权限继承")

    draw.rounded_rectangle((58, 1204, 1022, 1400), 20, fill="#252B2F")
    text(draw, (86, 1236), "模型能力会迅速扩散", 22, "#FFFFFF", True)
    text(draw, (86, 1275), "真正稀缺的是可验证、可重复、可进入生产的系统。", 18, "#D9DEDF")
    text(draw, (86, 1322), "来源：Anthropic · Madrona · Granola · arXiv", 14, "#AEB6B9")
    text(draw, (86, 1351), "论文与厂商指标均为特定配置", 13, "#8F989B")

    qr = Image.open(QR).convert("RGB")
    qr = qr.resize((148, 148), Image.Resampling.NEAREST)
    im.paste(qr, (850, 1228))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, quality=95)


if __name__ == "__main__":
    main()
