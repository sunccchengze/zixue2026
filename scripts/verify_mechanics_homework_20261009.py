#!/usr/bin/env python3
"""10月9日作业（2-12(a)、2-14、2-16）的独立验收。

仓库根运行：.venv/bin/python scripts/verify_mechanics_homework_20261009.py
依赖：numpy、Pillow、pymupdf（docx 审计走 scripts/docx_page_audit.py 子进程）。

与 generate 脚本**不同**的方程组：
- 2-12(a) 用对 A、对 B 两个矩方程（generate 用对 A 矩 + ΣFy）；
- 2-14 整体改用对 C 取矩求 F_NB，右腿改用 {ΣM_E, ΣFx, ΣFy}（对绳作用点取矩消去绳力；generate 用 ΣM_A）；
- 2-16 改用 {整体ΣM_B, 右半ΣM_B, 右半ΣM_C, 整体ΣFx, 整体ΣFy, 右半ΣFy}（generate 用整体ΣM_A 等）。
再核对参考答案.md 里的互证恒等式、图片可解码、作业单真的一页且不含答案。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "工程力学/作业/2026-10-09-作业"
MD = DIR / "参考答案.md"
DOCX = DIR / "工程力学作业单（2-12a、2-14、2-16）.docx"
BOOK = {"2-12a": (5 / 3, 1 / 3), "2-14": None, "2-16": (12, 40, 12, 20, 12, 8)}
fails: list[str] = []


def ok(cond, msg):
    print(("  ✔ " if cond else "  ✘ ") + msg)
    if not cond:
        fails.append(msg)


def z(pos, f):
    """逆正力矩 z = x*Fy - y*Fx，pos 为相对取矩点的位置。"""
    return pos[0] * f[1] - pos[1] * f[0]


def check_212a():
    print("2-12(a)")
    q = a = 1.0
    M = q * a * a  # 逆时针
    loads = [(a, -2 * q * a)]           # 均布合力作用点与力
    # ΣM_A 与 ΣM_B（两个矩方程，与 generate 不同）
    mA = sum(z((x, 0), (0, fy)) for x, fy in loads) + M
    mB = sum(z((x - 3 * a, 0), (0, fy)) for x, fy in loads) + M
    A = np.array([[3 * a, 0.0], [0.0, -3 * a]])
    b = np.array([-mA, -mB])
    FB, FA = np.linalg.solve(A, b)
    ok(abs(FA - BOOK["2-12a"][0]) < 1e-12 and abs(FB - BOOK["2-12a"][1]) < 1e-12,
       f"F_A={FA:.6f}、F_B={FB:.6f} 与教材 5/3、1/3 一致")
    # 参考答案.md 声称的对 B 校核恒等式
    lhs = -FA * 3 * a + 2 * q * a * 2 * a + M
    ok(abs(lhs) < 1e-12, f"参考答案『对B取矩=0』恒等式成立（={lhs:.2e}）")


def check_214():
    print("2-14")
    P, l, a, h = 1.0, 1.0, 0.37, 0.83
    for alpha_deg in (58.0, 72.0, 80.0):
        al = np.radians(alpha_deg)
        xc, H = l * np.cos(al), l * np.sin(al)
        xK, yK = (l - a) * np.cos(al), (l - a) * np.sin(al)
        yE = H - h
        xE = (H - yE) / np.tan(al)
        # 整体对 C 取矩求 F_NB（generate 用对 B）
        NB = -z((xK - xc, yK), (0, -P)) / z((-2 * xc, 0), (0, 1))
        NC = P - NB
        # 右腿：ΣM_E（消去绳力）、ΣFx、ΣFy，未知 (FT, Ax, Ay)——与 generate 的 ΣM_A 不同
        A = np.zeros((3, 3)); b = np.zeros(3)
        A[0, 1] = z((-xE, H - yE), (1, 0)); A[0, 2] = z((-xE, H - yE), (0, 1))
        b[0] = -(z((xK - xE, yK - yE), (0, -P)) + z((xc - xE, -yE), (0, NC)))
        A[1, 0] = -1; A[1, 1] = 1
        A[2, 2] = 1; b[2] = P - NC
        FT, Ax, Ay = np.linalg.solve(A, b)
        want = P * a * np.cos(al) / (2 * h)
        ok(abs(FT - want) < 1e-10, f"α={alpha_deg}°: F_T={FT:.8f} = Pa·cosα/(2h)={want:.8f}")
        ok(abs(NB - P * a / (2 * l)) < 1e-10, f"α={alpha_deg}°: F_NB={NB:.8f} = Pa/(2l)")
    # 参考答案.md 声称的左腿互证恒等式：-F_NB*l*cosα + F_T*h = 0
    al = np.radians(72.0)
    NB = P * a / (2 * l); FT = P * a * np.cos(al) / (2 * h)
    ok(abs(-NB * l * np.cos(al) + FT * h) < 1e-12, "左腿对A取矩互证恒等式成立")


def check_216():
    print("2-16")
    F, q = 12.0, 8.0
    W = q * 6.0
    xF = 8.0
    # 未知 (FAx, FAy, FBx, FBy, FCx, FCy)；方程组与 generate 不同
    A = np.zeros((6, 6)); b = np.zeros(6)
    # 整体 ΣM_B：A 相对 B=(-12,0)；W 相对 B=(3-12,8)；F 相对 B=(8-12,8)
    A[0, 0] = z((-12, 0), (1, 0)); A[0, 1] = z((-12, 0), (0, 1))
    b[0] = -(z((-9, 8), (0, -W)) + z((xF - 12, 8), (0, -F)))
    # 整体 ΣFx / ΣFy
    A[1, 0] += 1; A[1, 2] += 1
    A[2, 1] += 1; A[2, 3] += 1; b[2] = W + F
    # 右半 ΣM_B：C 相对 B=(-6,8)；F 相对 B=(-4,8)
    A[3, 4] = z((-6, 8), (1, 0)); A[3, 5] = z((-6, 8), (0, 1))
    b[3] = -z((-4, 8), (0, -F))
    # 右半 ΣM_C：B 相对 C=(6,-8)；F 相对 C=(2,0)
    A[4, 2] = z((6, -8), (1, 0)); A[4, 3] = z((6, -8), (0, 1))
    b[4] = -z((2, 0), (0, -F))
    # 右半 ΣFy
    A[5, 5] += 1; A[5, 3] += 1; b[5] = F
    v = np.linalg.solve(A, b)
    mag = (abs(v[0]), abs(v[1]), abs(v[2]), abs(v[3]), abs(v[4]), abs(v[5]))
    ok(np.allclose(mag, BOOK["2-16"], atol=1e-9), f"六分量大小 {tuple(round(x,6) for x in mag)} 与教材一致")
    ok(v[2] < 0 and v[0] > 0, f"方向：F_Bx 向左（{v[2]:.0f}）、F_Ax 向右（{v[0]:.0f}）")
    # 参考答案.md 声称的左半对 C 校核
    FAx, FAy = v[0], v[1]
    lhs = z((-6, -8), (FAx, FAy)) + z((-3, 0), (0, -W))
    ok(abs(lhs) < 1e-9, f"左半对C取矩=0 恒等式成立（={lhs:.2e}）")


def check_artifacts():
    print("产物")
    text = MD.read_text(encoding="utf-8")
    for needle in ("\\frac{5}{3}qa", "\\frac{Pa\\cos\\alpha}{2h}", "F_{By}=20", "逐位一致",
                   "关键结果自查表", "图/解答-2-12a.png", "图/解答-2-14.png", "图/解答-2-16.png"):
        ok(needle in text, f"参考答案.md 含 {needle!r}")
    imgs = ["图/题2-12a.png", "图/题2-14.png", "图/题2-16.png",
            "图/解答-2-12a.png", "图/解答-2-14.png", "图/解答-2-16.png"]
    for rel in imgs:
        p = DIR / rel
        good = p.exists()
        if good:
            with Image.open(p) as im:
                im.load()
                good = im.size[0] > 200 and im.size[1] > 150
        ok(good, f"{rel} 存在且可解码")
    for rel in imgs[:3]:
        ok(f"]({rel})" in (DIR / "题面.md").read_text(encoding="utf-8"), f"题面.md 内嵌 {rel}")
    # 作业单：一页 + 不含答案
    r = subprocess.run([sys.executable, str(ROOT / "scripts/docx_page_audit.py"), str(DOCX)],
                       capture_output=True, text=True)
    ok(r.returncode == 0 and "一页" in r.stdout, "作业单 docx 独立审计判为一页")
    sheet = (DIR / "作业单.json").read_text(encoding="utf-8")
    for bad in ("5/3", "qa/3", "cos", "2h", "40 kN", "答案"):
        ok(bad not in sheet, f"作业单 spec 不含答案串 {bad!r}")


def main():
    check_212a()
    check_214()
    check_216()
    check_artifacts()
    print()
    if fails:
        print(f"验收失败 {len(fails)} 项：")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("全部验收通过：三题数值、互证恒等式、图片、作业单页数与无答案泄漏。")


if __name__ == "__main__":
    main()
