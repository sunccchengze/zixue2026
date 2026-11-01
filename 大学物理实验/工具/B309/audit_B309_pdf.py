#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quantitative preflight for the B309 PDF: A4, page ink, bottom whitespace, overflow and key text."""
from __future__ import annotations
import argparse
from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageOps

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
DEFAULT_PDF = ROOT / "大学物理实验/实验项目/实验报告/B309-等厚干涉/实验报告-等厚干涉-完整版.pdf"


def audit(pdf_path: Path, dpi: int, max_gap_mm: float, preview_dir: Path | None) -> int:
    doc = fitz.open(pdf_path)
    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"PDF: {pdf_path}\nPages: {len(doc)} | Size: {size_mb:.2f} MiB | DPI: {dpi}")
    failures: list[str] = []
    warnings: list[str] = []
    if not (0.0 < size_mb <= 3.0):
        failures.append(f"PDF size is outside the 0–3 MiB budget ({size_mb:.2f} MiB)")
    if not 1 <= len(doc) <= 20:
        failures.append(f"Unexpected page count: {len(doc)}")

    required = ["1.0144", "23.2", "0.63", "4.8", "1.01355", "0.999716"]
    all_text = "\n".join(page.get_text() for page in doc)
    for token in required:
        if token not in all_text:
            failures.append(f"Required result not found in extracted PDF text: {token}")

    if preview_dir:
        preview_dir.mkdir(parents=True, exist_ok=True)

    for idx, page in enumerate(doc, start=1):
        width_pt, height_pt = page.rect.width, page.rect.height
        width_mm, height_mm = width_pt * 25.4 / 72, height_pt * 25.4 / 72
        is_a4 = abs(width_mm - 210) <= 1.0 and abs(height_mm - 297) <= 1.0
        if not is_a4:
            failures.append(f"Page {idx}: not A4 ({width_mm:.2f} × {height_mm:.2f} mm)")

        # Check every extracted text/image block remains inside the physical page.
        for block in page.get_text("blocks"):
            x0, y0, x1, y1 = block[:4]
            if x0 < -0.5 or y0 < -0.5 or x1 > width_pt + 0.5 or y1 > height_pt + 0.5:
                failures.append(f"Page {idx}: content block exceeds page bounds: {(x0, y0, x1, y1)}")
                break

        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False, colorspace=fitz.csRGB)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if preview_dir:
            image.save(preview_dir / f"page-{idx:02d}.png", optimize=True)

        # Exclude headers/footers and page-number band; inspect printable body only.
        x0 = round(0.78 * dpi)
        x1 = min(pix.width, round((width_pt / 72 - 0.78) * dpi))
        y0 = round(0.72 * dpi)
        y1 = min(pix.height, round((height_pt / 72 - 0.72) * dpi))
        body = ImageOps.grayscale(image.crop((x0, y0, x1, y1)))
        mask = body.point(lambda value: 255 if value < 245 else 0)
        bbox = mask.getbbox()
        ink_pixels = sum(mask.histogram()[1:])
        body_pixels = max(1, body.width * body.height)
        ink_pct = 100 * ink_pixels / body_pixels
        if bbox:
            last_ink_row = y0 + bbox[3] - 1
            blank_px = max(0, y1 - last_ink_row)
            blank_mm = blank_px / dpi * 25.4
        else:
            blank_mm = (y1 - y0) / dpi * 25.4
        # The final page is allowed to end with natural whitespace; all earlier pages are checked.
        status = "EXEMPT (final page)" if idx == len(doc) else ("OK" if blank_mm <= max_gap_mm else "REVIEW")
        print(f"  p{idx:02d}: {width_mm:.1f} × {height_mm:.1f} mm | bottom blank {blank_mm:5.1f} mm | body ink {ink_pct:4.1f}% | {status}")
        if idx != len(doc) and blank_mm > max_gap_mm:
            failures.append(f"Page {idx}: bottom whitespace {blank_mm:.1f} mm exceeds {max_gap_mm:.1f} mm")
        if ink_pct < 3.0 and idx != len(doc):
            warnings.append(f"Page {idx}: low body ink density ({ink_pct:.1f}%)")

    print(f"A4 pages: {'PASS' if not any('not A4' in x for x in failures) else 'FAIL'}")
    print(f"Body bottom-gap target: ≤ {max_gap_mm:.1f} mm on non-final pages")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(" -", warning)
    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" -", failure)
        return 1
    print("Preflight: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--dpi", type=int, default=110)
    parser.add_argument("--max-gap-mm", type=float, default=60.0)
    parser.add_argument("--preview-dir", type=Path, help="Optional directory for 110-dpi page renders")
    args = parser.parse_args()
    return audit(args.pdf.resolve(), args.dpi, args.max_gap_mm, args.preview_dir)

if __name__ == "__main__":
    raise SystemExit(main())
