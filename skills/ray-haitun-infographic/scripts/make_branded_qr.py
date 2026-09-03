#!/usr/bin/env python3
"""Create a stylized, scan-safe QR and optionally place it on a base image."""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H


def make_qr(url: str, size: int) -> Image.Image:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=12, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    raw = qr.make_image(fill_color="#20252B", back_color="white").convert("RGB")
    raw = raw.resize((size, size), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(raw)
    # Small orange accent inside the data field; never cover finder patterns.
    cx = cy = size // 2
    r = max(5, size // 45)
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill="#FF6B2C", outline="white", width=max(2, size//180))
    return raw


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=420)
    ap.add_argument("--base", help="Optional infographic PNG")
    ap.add_argument("--composite-out")
    ap.add_argument("--x", type=int, default=560)
    ap.add_argument("--y", type=int, default=1080)
    args = ap.parse_args()
    qr = make_qr(args.url, args.size)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    qr.save(args.out)
    if args.base and args.composite_out:
        base = Image.open(args.base).convert("RGB")
        base.paste(qr, (args.x, args.y))
        base.save(args.composite_out)


if __name__ == "__main__":
    main()
