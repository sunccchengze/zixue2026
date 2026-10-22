from pathlib import Path
PROJECT = Path(__file__).resolve().parent
"""Pixel-level QA + auto-hardening for the deck.

Why this exists: the old check *estimated* text width (avg glyph = 0.50 em).
Microsoft YaHei is wider than the Linux substitute LibreOffice renders with, so
lines that looked fine here silently re-wrap in PowerPoint, blow out of their
panel and wreck the alignment. Guessing cannot catch that; measuring pixels can.

Loop:  build -> render -> measure real ink -> widen/grow boxes -> rebuild.
"""
import math, os, re, subprocess
import numpy as np
from PIL import Image, ImageFilter
from pptx import Presentation
from pptx.util import Emu

EMU = 914400.0
DECK = str(PROJECT / "Mask-Reuse-Qualification-Review.pptx")
RD = str(PROJECT / "build/render")
DPI = 150
HEADROOM = 0.80          # longest line may fill at most 80% of its box
MIN_GROWTH = 0.01        # inches; ignore smaller nudges


# ------------------------------------------------------------------ render
def render(dpi=DPI):
    os.makedirs(RD, exist_ok=True)
    for f in os.listdir(RD):
        if f.endswith((".png", ".pdf")):
            os.remove(f"{RD}/{f}")
    subprocess.run(["soffice", "--headless", "--norestore", "--convert-to", "pdf",
                    "--outdir", RD, DECK], capture_output=True)
    pdf = f"{RD}/{os.path.basename(DECK).replace('.pptx', '.pdf')}"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, f"{RD}/r"], capture_output=True)
    return sorted(f"{RD}/{f}" for f in os.listdir(RD) if f.startswith("r-"))


# ------------------------------------------------------------------ ink
def ink(img, box, W, H):
    """(lines, ink_w, ink_h, ink_L, ink_T, ink_R, ink_B) in inches for one box."""
    ih, iw = img.shape
    sx, sy = iw / W, ih / H
    pad = 2
    x0 = max(0, int(box[0] * sx) - pad); y0 = max(0, int(box[1] * sy) - pad)
    x1 = min(iw, int(box[2] * sx) + pad); y1 = min(ih, int(box[3] * sy) + pad)
    if x1 - x0 < 3 or y1 - y0 < 3:
        return None
    crop = img[y0:y1, x0:x1].astype(float)
    k = min(31, max(9, (min(crop.shape) // 4) | 1))
    bg = np.asarray(Image.fromarray(crop.astype(np.uint8)).filter(ImageFilter.MedianFilter(k))).astype(float)
    d = np.abs(crop - bg)
    m = d > max(26, d.max() * 0.30)
    m[:4, :] = False; m[-4:, :] = False; m[:, :4] = False; m[:, -4:] = False
    if m.sum() < 6:
        return None
    rows = m.sum(1); cols = m.sum(0)
    peak = rows.max()
    on = rows > max(1.0, peak * 0.14)
    bands, run = [], False
    for v in on:
        if v and not run:
            bands.append(1); run = True
        elif v:
            bands[-1] += 1
        elif run:
            run = False
    intervals = []
    st = None
    for i2, v in enumerate(on):
        if v and st is None:
            st = i2
        elif not v and st is not None:
            intervals.append([st, i2 - 1]); st = None
    if st is not None:
        intervals.append([st, len(on) - 1])
    seq = []
    for iv in intervals:
        if seq and iv[0] - seq[-1][1] <= 2:
            seq[-1][1] = iv[1]
        else:
            seq.append(iv)
    seq = [q for q in seq if q[1] - q[0] >= 1]
    ys = [i for i, v in enumerate(on) if v]; xs = [i for i, v in enumerate(cols > 0) if v]
    if not ys or not xs:
        return None
    return dict(lines=len(seq), w=(xs[-1] - xs[0] + 1) / sx, h=(ys[-1] - ys[0] + 1) / sy,
                L=(x0 + xs[0]) / sx, T=(y0 + ys[0]) / sy,
                R=(x0 + xs[-1] + 1) / sx, B=(y0 + ys[-1] + 1) / sy)


def fill_of(sh):
    x = sh._element.xml
    m = re.search(r"<a:(solidFill|gradFill)\b[^>]*>(.*?)</a:\1>", x, re.S)
    if not m:
        return None
    cols = [tuple(int(v, 16) for v in [c[i:i + 2] for i in (0, 2, 4)])
            for c in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', m.group(2))]
    if not cols:
        return None
    rgb = tuple(int(sum(c[i] for c in cols) / len(cols)) for i in range(3))
    a = re.findall(r'<a:alpha val="(\d+)"', m.group(2)) or re.findall(r'<a:alpha val="(\d+)"', x[:m.start()])
    return (rgb, min(int(a[-1]) / 100000.0, 1.0) if a else 1.0)


def bbox(sh):
    return (sh.left / EMU, sh.top / EMU,
            (sh.left + sh.width) / EMU, (sh.top + sh.height) / EMU)


def container(shapes, k):
    """Nearest filled rectangle drawn before shape k that fully contains it."""
    bk = bbox(shapes[k])
    for j in range(k - 1, -1, -1):
        bj = bbox(shapes[j])
        f = fill_of(shapes[j])
        if not f:
            continue
        if (bj[0] <= bk[0] + 0.02 and bj[1] <= bk[1] + 0.02 and
                bj[2] >= bk[2] - 0.02 and bj[3] >= bk[3] - 0.02):
            if (bj[2] - bj[0]) > 0.5 and (bj[3] - bj[1]) > 0.3:
                return bj
    return None


def max_font(sh):
    fs = [r.font.size.pt for p in sh.text_frame.paragraphs for r in p.runs if r.font.size]
    return max(fs) if fs else 12.0


def is_right_aligned(sh):
    for p in sh.text_frame.paragraphs:
        if p.alignment is not None and "RIGHT" in str(p.alignment):
            return True
    return False


# ------------------------------------------------------------------ measure
def measure(verbose=False):
    files = render()
    prs = Presentation(DECK)
    W = prs.slide_width / EMU; H = prs.slide_height / EMU
    out = []
    for i, sl in enumerate(prs.slides, 1):
        img = np.asarray(Image.open(files[i - 1]).convert("L")).astype(float)
        shapes = list(sl.shapes)
        for k, sh in enumerate(shapes):
            if not sh.has_text_frame or not sh.text_frame.text.strip():
                continue
            b = bbox(sh)
            m = ink(img, b, W, H)
            out.append(dict(slide=i, idx=k, sh=sh, box=b, m=m,
                            cont=container(shapes, k),
                            txt=sh.text_frame.text.replace("\n", " / ")[:52],
                            right=is_right_aligned(sh), fs=max_font(sh),
                            rot=bool(sh.rotation)))
    return prs, out, W, H


def report(prs, recs, W, H):
    probs = []
    for d in recs:
        m = d["m"]
        if not m:
            continue
        bw = d["box"][2] - d["box"][0]; bh = d["box"][3] - d["box"][1]
        if bw <= 0:
            continue
        if m["w"] / bw > HEADROOM:
            probs.append(("TIGHT", d["slide"], d["txt"],
                          f"longest line {m['w'] / bw * 100:.0f}% of {bw:.2f}in box"))
        if m["h"] > bh - 0.02:
            probs.append(("OVERFLOW", d["slide"], d["txt"],
                          f"ink {m['h']:.2f}in vs box {bh:.2f}in"))
    # ink-level collisions
    for a in range(len(recs)):
        for b in range(a + 1, len(recs)):
            A, B = recs[a], recs[b]
            if A["slide"] != B["slide"] or not A["m"] or not B["m"]:
                continue
            ox = min(A["m"]["R"], B["m"]["R"]) - max(A["m"]["L"], B["m"]["L"])
            oy = min(A["m"]["B"], B["m"]["B"]) - max(A["m"]["T"], B["m"]["T"])
            if ox > 0.06 and oy > 0.06:
                probs.append(("COLLIDE", A["slide"], f'{A["txt"]}|{B["txt"]}',
                              f"ink overlap {ox:.2f}x{oy:.2f}in"))
    # ink-level alignment near-misses
    for i in range(1, len(prs.slides) + 1):
        grp = [d for d in recs if d["slide"] == i and d["m"] and not d["rot"]]
        for key, e1, e2 in (("L", "L", "L"), ("R", "R", "R"), ("T", "T", "T")):
            pts = [(d["m"][e1], d) for d in grp]
            for a in range(len(pts)):
                for b in range(a + 1, len(pts)):
                    dv = pts[b][0] - pts[a][0]
                    if 0.035 < abs(dv) < 0.085:
                        A, B = pts[a][1], pts[b][1]
                        if A["txt"] == B["txt"] or abs(A["m"]["T"] - B["m"]["T"]) > 1.2:
                            continue
                        probs.append((f"ALIGN-{key}", i, f'{A["txt"]}|{B["txt"]}',
                                      f"ink edges {pts[a][0]:.3f} vs {pts[b][0]:.3f} "
                                      f"— off by {abs(dv) * 72:.0f}pt"))
    seen, uniq = set(), []
    for p in probs:
        if p[:3] in seen:
            continue
        seen.add(p[:3]); uniq.append(p)
    return uniq


def show(probs):
    for tag in ("COLLIDE", "OVERFLOW", "TIGHT", "ALIGN-L", "ALIGN-R", "ALIGN-T"):
        g = [p for p in probs if p[0] == tag]
        if not g:
            continue
        print(f"\n### {tag}  ({len(g)})")
        for t, i, txt, msg in g[:18]:
            print(f"  S{i:02d} {txt[:56]}\n        {msg}")
        if len(g) > 18:
            print(f"  ... +{len(g) - 18} more")
    print(f"\n=== {len(probs)} problems ===")


# ------------------------------------------------------------------ harden
def harden(passes=4):
    for p in range(passes):
        prs, recs, W, H = measure()
        changed = 0
        for d in recs:
            m = d["m"]
            if not m or d["rot"]:
                continue
            sh = d["sh"]; L, T, R, B = d["box"]
            bw, bh = R - L, B - T
            fs = d["fs"]
            # ---- 1. widen so the longest line keeps >= 20% headroom
            need = m["w"] / HEADROOM
            if need > bw + MIN_GROWTH:
                lim = W - 0.90                       # slide margin
                if d["cont"]:
                    lim = min(lim, d["cont"][2] - 0.10)
                for e in recs:
                    if e is d or e["slide"] != d["slide"] or not e["m"]:
                        continue
                    eb = e["box"]
                    if eb[1] < B - 0.02 and eb[3] > T + 0.02 and eb[0] >= R - 0.01:
                        lim = min(lim, eb[0] - 0.03)
                neww = min(need, lim - L)
                if d["right"]:
                    sh.left = Emu(int((R - neww) * EMU))
                sh.width = Emu(int(neww * EMU))
                R, bw = L + neww, neww
                changed += 1
            # ---- 2. grow height by one line, but only into provable slack
            if m["h"] > bh - 0.035:
                grow = min(fs * 1.30 / 72.0, 0.45)
                lim = H - 0.30
                if d["cont"]:
                    lim = min(lim, d["cont"][3] - 0.10)
                newh = min(bh + grow, lim - T)
                if newh > bh + MIN_GROWTH:
                    sh.height = Emu(int(newh * EMU))
                    changed += 1
        prs.save(DECK)
        prs2, recs2, W2, H2 = measure()
        probs = report(prs2, recs2, W2, H2)
        tight = sum(1 for x in probs if x[0] == "TIGHT")
        print(f"pass {p + 1}: moved {changed} boxes -> {len(probs)} problems ({tight} tight)")
        if changed == 0:
            break
    return probs


if __name__ == "__main__":
    import sys
    if "--harden" in sys.argv:
        pr = harden()
    else:
        pr = report(*measure())
    show(pr)
