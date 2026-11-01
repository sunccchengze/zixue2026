#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render report-ready plots from the already verified B309 derived readings."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
OUT = ROOT / "大学物理实验/实验项目/assets"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#17324D"
BLUE = "#4D7EA8"
GOLD = "#D6A83B"
PALE = "#EAF1F6"
GRID = "#D8E0E7"
MUTED = "#607080"
WHITE = "#FFFFFF"
FONT_REG = str(ROOT / "大学物理实验/工具/B309/fonts/SourceHanSerifCN-Regular.otf")
FONT_BOLD = str(ROOT / "大学物理实验/工具/B309/fonts/SourceHanSerifCN-Bold.otf")

def font(size: int, bold: bool = False):
    path = FONT_BOLD if bold else FONT_REG
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

def draw_chart(filename, values, labels, mean, y_min, y_max, y_ticks,
               y_label, annotation, decimals=3):
    w, h = 1500, 820
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    f_axis, f_tick, f_note = font(29), font(25), font(25)
    left, top, right, bottom = 155, 75, 70, 145
    x0, y0, x1, y1 = left, top, w-right, h-bottom
    # Plot frame and subtle horizontal grid.
    for tick in y_ticks:
        y = y1 - (tick-y_min)/(y_max-y_min)*(y1-y0)
        d.line((x0, y, x1, y), fill=GRID, width=2)
        text = f"{tick:.2f}" if (y_max-y_min) < 2 else f"{tick:.1f}"
        bbox = d.textbbox((0, 0), text, font=f_tick)
        d.text((x0-18-(bbox[2]-bbox[0]), y-16), text, fill=MUTED, font=f_tick)
    d.line((x0, y0, x0, y1, x1, y1), fill=NAVY, width=4)
    xs = [x0 + 62 + (x1-x0-124)*i/(len(values)-1) for i in range(len(values))]
    def yy(v): return y1 - (v-y_min)/(y_max-y_min)*(y1-y0)
    # Mean line and a restrained ± one standard deviation band.
    if filename.endswith("u_k.png"):
        spread = 0.1683
    else:
        spread = 1.6366
    band_top, band_bottom = yy(mean+spread), yy(mean-spread)
    d.rectangle((x0, band_top, x1, band_bottom), fill=PALE)
    d.line((x0, yy(mean), x1, yy(mean)), fill=BLUE, width=4)
    pts = list(zip(xs, [yy(v) for v in values]))
    d.line(pts, fill=NAVY, width=5)
    for i, ((x, y), v, lab) in enumerate(zip(pts, values, labels)):
        r = 12
        d.ellipse((x-r, y-r, x+r, y+r), fill=GOLD, outline=NAVY, width=3)
        t = f"{v:.{decimals}f}"
        bbox = d.textbbox((0, 0), t, font=f_tick)
        tw = bbox[2]-bbox[0]
        label_y = y-55 if (i % 2 == 0 or y > y1-90) else y+17
        d.rounded_rectangle((x-tw/2-8, label_y-3, x+tw/2+8, label_y+34), radius=7, fill=WHITE)
        d.text((x-tw/2, label_y), t, fill=NAVY, font=f_tick)
        bbox = d.textbbox((0, 0), lab, font=f_tick)
        d.text((x-(bbox[2]-bbox[0])/2, y1+24), lab, fill=MUTED, font=f_tick)
    mean_label = f"mean = {mean:.4f}" if "u_k" in filename else f"mean = {mean:.3f} mm"
    mean_box = d.textbbox((0, 0), mean_label, font=f_note)
    d.rounded_rectangle((x0+18, y0+15, x0+mean_box[2]-mean_box[0]+42, y0+55), radius=7, fill=WHITE)
    d.text((x0+30, y0+18), mean_label, fill=BLUE, font=f_note)
    # Axis descriptions are intentionally English/math-only for consistent glyph support.
    d.text((x0, 18), annotation, fill=NAVY, font=font(27, True))
    axis_text = "级数 k"
    axis_box = d.textbbox((0, 0), axis_text, font=f_axis)
    d.text((x0+(x1-x0-(axis_box[2]-axis_box[0]))/2, h-57), axis_text, fill=MUTED, font=f_axis)
    # Rotated y-axis label.
    label = Image.new("RGBA", (360, 52), (255,255,255,0))
    ld = ImageDraw.Draw(label)
    ld.text((0,0), y_label, fill=MUTED, font=f_axis)
    label = label.rotate(90, expand=True)
    im.paste(label, (18, (h-label.height)//2), label)
    im.save(OUT / filename, dpi=(220,220), optimize=True)

# Derived values shown in the report tables; original microscope readings remain unchanged.
draw_chart("B309-图-牛顿环逐差量u_k.png",
           [11.862, 11.807, 12.241, 11.946, 11.923],
           ["k=6", "k=7", "k=8", "k=9", "k=10"],
           11.95584, 11.75, 12.30,
           [11.8, 11.9, 12.0, 12.1, 12.2, 12.3],
           "u_k（mm²）", "牛顿环逐差量 u_k｜均值与 ±s(u_k)", 3)
draw_chart("B309-图-劈尖间距l_k.png",
           [19.026, 17.572, 16.260, 15.251],
           ["k=0", "k=10", "k=20", "k=30"],
           17.02725, 14.0, 20.5,
           [14, 15, 16, 17, 18, 19, 20],
           "l_k（mm）", "劈尖逐差量 l_k｜均值与 ±s(l_k)", 3)
# A compact conceptual illustration, intentionally separate from the measured-data plots.
def draw_geometry():
    w, h = 1500, 560
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    title = font(30, True)
    sub = font(23)
    d.rounded_rectangle((12, 12, 738, h-12), radius=22, fill="#F8FAFC", outline="#D7E0E8", width=3)
    d.rounded_rectangle((762, 12, w-12, h-12), radius=22, fill="#F8FAFC", outline="#D7E0E8", width=3)
    d.text((55, 40), "牛顿环", fill=NAVY, font=title)
    d.text((55, 82), "同一厚度对应的同心干涉环", fill=MUTED, font=sub)
    # Top view: concentric contours and a radius marker.
    cx, cy = 350, 325
    for r in (54, 88, 122, 156):
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=BLUE if r != 122 else GOLD, width=5 if r == 122 else 3)
    d.ellipse((cx-7, cy-7, cx+7, cy+7), fill=NAVY)
    d.line((cx, cy, cx+122, cy), fill=NAVY, width=4)
    d.text((cx+43, cy-42), "r_k", fill=NAVY, font=font(27, True))
    d.text((cx-22, cy+15), "O", fill=NAVY, font=sub)
    d.text((95, 500), "环半径 r_k 随薄膜厚度增加", fill=MUTED, font=sub)
    d.text((795, 40), "空气劈尖", fill=NAVY, font=title)
    d.text((795, 82), "劈尖侧视：条纹间距与箔厚关系示意", fill=MUTED, font=sub)
    # Two plates forming a small wedge; the right spacer is the foil thickness D.
    x_left, x_right = 830, 1405
    y_base = 365
    d.line((x_left, y_base, x_right, y_base), fill=NAVY, width=12)
    d.line((x_left, y_base-28, x_right-24, y_base-100), fill=BLUE, width=12)
    d.rectangle((x_right-24, y_base-102, x_right+25, y_base), fill=GOLD, outline=NAVY, width=3)
    # A few lightly drawn fringe traces, roughly parallel to the plates.
    for frac in (0.20, 0.36, 0.52, 0.68, 0.84):
        x = x_left + (x_right-x_left)*frac
        y = y_base - 28 - (x-x_left)*72/(x_right-x_left)
        d.line((x, y+15, x, y_base-10), fill="#A9B9C8", width=2)
    d.line((x_left, 438, x_right-24, 438), fill=MUTED, width=2)
    d.polygon([(x_left,438),(x_left+12,431),(x_left+12,445)], fill=MUTED)
    d.polygon([(x_right-24,438),(x_right-36,431),(x_right-36,445)], fill=MUTED)
    d.text((1085, 446), "L", fill=NAVY, font=font(27, True))
    d.line((x_right+60, y_base-102, x_right+60, y_base), fill=GOLD, width=4)
    d.polygon([(x_right+60,y_base-102),(x_right+53,y_base-88),(x_right+67,y_base-88)], fill=GOLD)
    d.polygon([(x_right+60,y_base),(x_right+53,y_base-14),(x_right+67,y_base-14)], fill=GOLD)
    d.text((x_right+28, y_base-72), "D", fill=NAVY, font=font(27, True))
    d.line((946, 300, 1038, 300), fill=GOLD, width=3)
    d.polygon([(946,300),(958,293),(958,307)], fill=GOLD)
    d.polygon([(1038,300),(1026,293),(1026,307)], fill=GOLD)
    d.text((983, 263), "s", fill=NAVY, font=font(27, True))
    d.text((x_left+30, y_base-64), "α", fill=NAVY, font=sub)
    d.text((795, 500), "s：条纹间距　D：箔厚　L：劈尖长度", fill=MUTED, font=sub)
    im.save(OUT / "B309-图-等厚干涉几何示意.png", dpi=(220,220), optimize=True)

draw_geometry()
print("Generated:", *(str(OUT / name) for name in ("B309-图-牛顿环逐差量u_k.png", "B309-图-劈尖间距l_k.png", "B309-图-等厚干涉几何示意.png")), sep="\n")
