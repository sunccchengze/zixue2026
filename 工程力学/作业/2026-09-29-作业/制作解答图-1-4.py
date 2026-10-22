#!/usr/bin/env python3
"""兼容旧入口：1-4精确解答图；实际实现移入仓级scripts/，可从任意目录运行。"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_mechanics_homework_20260929 import main

if __name__ == "__main__":
    main(("1-4",))
