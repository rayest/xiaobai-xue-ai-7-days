#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/infographics/agents-enter-production-2026-09-05.png"
QR = ROOT / "assets/infographics/hub-smarphin-qr.png"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_MEDIUM if bold else FONT_LIGHT, size)


def text(draw, xy, value, size, fill="#22272B", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def card(draw, y, no, title, left1, left2, right1, action, note=None):
    x, w, h = 58, 964, 182
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill="#FFFFFF", outline="#DDD8CF", width=2)
    text(draw, (86, y + 24), no, 28, "#F2682A", True)
    text(draw, (148, y + 22), title, 27, bold=True)
    text(draw, (148, y + 66), left1, 19)
    text(draw, (148, y + 97), left2, 19)
    if right1:
        text(draw, (600, y + 97), right1, 18)
    if note:
        text(draw, (813, y + 100), note, 13, "#73787A")
    draw.rounded_rectangle((140, y + 134, 986, y + 166), 8, fill="#FFF0E8")
    text(draw, (156, y + 140), "行动｜" + action, 17, "#B94210", True)


def main():
    im = Image.new("RGB", (1080, 1440), "#F7F4EE")
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, 18, 1440), fill="#F2682A")

    text(draw, (66, 45), "海豚智脑", 28, bold=True)
    text(draw, (218, 50), "hub.smarphin.com", 17, "#74787A")
    text(draw, (66, 105), "AI INTELLIGENCE · 2026.09.05", 18, "#F2682A", True)
    text(draw, (66, 145), "代理进入生产约束期", 52, bold=True)
    text(draw, (68, 211), "真正的竞争，从模型分数转向成本、边界与系统验证", 22, "#555B5F")

    card(draw, 270, "01", "价格看 token，决策看任务",
         "Astra：$10 输入 / $50 输出，每百万 token",
         "单价约为 GPT-5.6 Sol 的 2.5 倍",
         "Fable 5.1 缓存读取降价 75%",
         "记录成功任务总成本、人工救援和失败恢复")
    card(draw, 470, "02", "开放生态进入控制权之争",
         "NVIDIA 拟以 129.303 亿美元收购 Hugging Face",
         "平台覆盖 1800 万+开发者、300 万模型",
         "承诺保持跨硬件、跨云开放",
         "持续检查跨硬件、跨云能力是否保持对等")
    card(draw, 670, "03", "代理把权限写进系统",
         "Commerce Agents 分开购物代理与商家代理",
         "参考实现不下单、不收费",
         "写操作先暂存，必须由人批准",
         "把审批、来源校验和回滚做成代码")
    card(draw, 870, "04", "AI 接入设备与公共服务",
         "MHS 用统一接口连接实验与制造设备",
         "官方案例：从数周缩到 8 小时",
         "WeatherNext 3 每小时刷新",
         "物理动作默认最小权限、可中止、可审计")
    card(draw, 1070, "05", "执行框架决定速度与安全",
         "预执行工具链最高降低 44.9% 墙钟时间*",
         "PlanFence：30 个受控流程无过期计划动作",
         "技能蒸馏复用操作知识",
         "版本化计划、依赖、验证与失败回滚", "*特定基准")

    draw.rounded_rectangle((58, 1270, 1022, 1400), 20, fill="#252B2F")
    text(draw, (86, 1304), "模型变强只是起点", 22, "#FFFFFF", True)
    text(draw, (86, 1344), "能否安全完成整项工作，取决于模型之外的系统。", 18, "#D9DEDF")

    qr = Image.open(QR).convert("RGB")
    # Reuse the previously decoded public-brand QR, cropping off its caption while
    # preserving the white quiet zone around all four sides.
    qr = qr.crop((60, 40, 580, 560)).resize((112, 112), Image.Resampling.NEAREST)
    im.paste(qr, (892, 1279))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, quality=95)


if __name__ == "__main__":
    main()
