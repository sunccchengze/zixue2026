#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
icourse163 课件(PDF)批量下载器  —  西安交通大学《理论力学》XJTU-1002985009 / tid=1488044471

用法:
    python3 dl.py                 # 下载全部 PDF 课件
    python3 dl.py --list-only     # 只导出清单不下载
    python3 dl.py --types 3,4     # 指定 contentType (1视频 2测验 3PDF 4附件 5富文本)
"""
import json, os, re, sys, time, csv, argparse, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts/icourse"))
from archive_safety import archive_url
import requests

COURSE_ID   = "1002985009"
TERM_ID     = "1488044471"
COURSE_NAME = "理论力学"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
BASE = "https://www.icourse163.org"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "downloads")
BAD  = r'[\\/:*?"<>|\r\n\t]'


def safe(name, limit=100):
    name = re.sub(BAD, "_", str(name or "")).strip().strip(".")
    return (name or "untitled")[:limit]


def load_cookies(path):
    raw = open(path, encoding="utf-8").read().strip()
    raw = re.sub(r"^\s*Cookie\s*:\s*", "", raw, flags=re.I).strip().strip("'\"")
    jar = {}
    if raw.startswith("["):
        for c in json.loads(raw):
            jar[c["name"]] = c["value"]
    else:
        for kv in raw.split(";"):
            kv = kv.strip()
            if "=" in kv:
                k, v = kv.split("=", 1)
                jar[k.strip()] = v.strip()
    return jar


class Client:
    def __init__(self, cookies):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA})
        for k, v in cookies.items():
            self.s.cookies.set(k, v, domain=".icourse163.org")
        self.tok = cookies.get("NTESSTUDYSI", "")

    def rpc(self, bean, method, data=None):
        h = {"User-Agent": UA, "Origin": BASE,
             "Referer": f"{BASE}/learn/XJTU-{COURSE_ID}?tid={TERM_ID}",
             "edu-script-token": self.tok,
             "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        r = self.s.post(f"{BASE}/web/j/{bean}.{method}.rpc?csrfKey={self.tok}",
                        headers=h, data=data or {}, timeout=40)
        return r.json()

    def dwr(self, script, method, params):
        d = {"callCount": "1", "scriptSessionId": "${scriptSessionId}190",
             "httpSessionId": self.tok, "c0-scriptName": script,
             "c0-methodName": method, "c0-id": "0",
             "batchId": str(int(time.time() * 1000))}
        for i, p in enumerate(params):
            d[f"c0-param{i}"] = p
        h = {"User-Agent": UA,
             "Referer": f"{BASE}/learn/XJTU-{COURSE_ID}?tid={TERM_ID}",
             "Content-Type": "text/plain;charset=UTF-8", "edu-script-token": self.tok}
        return self.s.post(f"{BASE}/dwr/call/plaincall/{script}.{method}.dwr",
                           headers=h, data=d, timeout=40).text


def get_tree(c):
    r = c.rpc("courseBean", "getLastLearnedMocTermDto", {"termId": TERM_ID})
    if r.get("code") != 0 or not r.get("result"):
        raise RuntimeError(f"目录获取失败: {r.get('code')} {r.get('message')}")
    return r["result"]["mocTermDto"]


def pdf_link(c, unit, tries=3):
    """返回 (url, 服务器上的原始文件名 or None)"""
    cid, uid, ct = unit.get("contentId"), unit.get("id"), unit.get("contentType", 3)
    for _ in range(tries):
        txt = c.dwr("CourseBean", "getLessonUnitLearnVo",
                    [f"number:{cid}", f"number:{ct}", "number:0", f"number:{uid}"])
        m = re.search(r'textOrigUrl:"([^"]+)"', txt)
        if m:
            url = m.group(1).replace("\\/", "/")
            fn = None
            q = urllib.parse.urlparse(url).query
            for k, v in urllib.parse.parse_qsl(q):
                if k.lower() == "download":
                    fn = urllib.parse.unquote(v)
            return url, fn
        time.sleep(1)
    return None, None


def unique_path(path, reserved):
    """Disambiguate same-run names, not files retained from an earlier run."""
    if path not in reserved:
        return path
    root, ext = os.path.splitext(path)
    i = 2
    while f"{root} ({i}){ext}" in reserved:
        i += 1
    return f"{root} ({i}){ext}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-only", action="store_true")
    ap.add_argument("--cookies", default=os.path.join(HERE, "cookies.txt"))
    ap.add_argument("--types", default="3")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    WANT = {int(x) for x in args.types.split(",")}

    cookies = load_cookies(args.cookies)
    if "NTESSTUDYSI" not in cookies:
        sys.exit("cookies.txt 缺少 NTESSTUDYSI")
    c = Client(cookies)

    info = c.rpc("mocMemberFollowBean", "userInfo", {})
    nick = (info.get("result") or {}).get("nickName", "?")
    print(f"登录身份: {nick}")

    term = get_tree(c)
    with open(os.path.join(HERE, "term_tree.json"), "w", encoding="utf-8") as stream:
        json.dump(term, stream, ensure_ascii=False, indent=1)

    targets = []
    for ci, ch in enumerate(term.get("chapters") or [], 1):
        cname = f"{ci:02d} {safe(ch.get('name'))}"
        for li, les in enumerate(ch.get("lessons") or [], 1):
            lname = f"{li:02d} {safe(les.get('name'))}"
            for ui, u in enumerate(les.get("units") or [], 1):
                if u.get("contentType") in WANT and u.get("visible", 1):
                    targets.append((cname, lname, ui, u))

    print(f"目录: {len(term.get('chapters') or [])} 章, 命中文档 {len(targets)} 个\n")

    rows, ok, fail, skipped = [], 0, [], 0
    reserved = set()
    for i, (cname, lname, ui, u) in enumerate(targets, 1):
        url, srv_name = pdf_link(c, u)
        if not url:
            print(f"[{i}/{len(targets)}] X 无直链  {cname}/{lname}/{u.get('name')}")
            fail.append((cname, lname, u.get("name"), "无直链"))
            rows.append([f"{cname}/{lname}/{u.get('name')}", "", "无直链"])
            continue

        fname = safe(srv_name or u.get("name") or f"unit_{u.get('id')}")
        if not fname.lower().endswith(".pdf"):
            fname += ".pdf"
        rel = os.path.join(COURSE_NAME, cname, lname, fname)
        dest = unique_path(os.path.join(OUT, rel), reserved)
        reserved.add(dest)
        rel = os.path.relpath(dest, OUT)

        if not args.overwrite and os.path.exists(dest) and os.path.getsize(dest) > 1024:
            skipped += 1
            rows.append([rel, archive_url(url), "已存在"])
            print(f"[{i}/{len(targets)}] = 跳过(已存在) {fname}")
            continue

        if args.list_only:
            rows.append([rel, archive_url(url), "未下载"]); print(f"[{i}/{len(targets)}] {rel}"); continue

        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with c.s.get(url, headers={"User-Agent": UA, "Referer": BASE + "/"},
                         stream=True, timeout=300) as r:
                r.raise_for_status()
                with open(dest + ".part", "wb") as f:
                    for chunk in r.iter_content(1 << 16):
                        if chunk:
                            f.write(chunk)
            size = os.path.getsize(dest + ".part")
            with open(dest + ".part", "rb") as f:
                head = f.read(5)
            if head != b"%PDF-":
                os.remove(dest + ".part")
                raise RuntimeError(f"不是PDF文件 (magic={head!r})")
            os.replace(dest + ".part", dest)
            ok += 1
            rows.append([rel, archive_url(url), "OK"])
            print(f"[{i}/{len(targets)}] OK {size/1024/1024:6.2f} MB  {fname}")
        except Exception as e:
            if os.path.exists(dest + ".part"):
                os.remove(dest + ".part")
            fail.append((cname, lname, fname, type(e).__name__))
            rows.append([rel, archive_url(url), f"失败:{type(e).__name__}"])
            print(f"[{i}/{len(targets)}] X 失败 {fname}: {type(e).__name__}")

    with open(os.path.join(HERE, "manifest.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["相对路径", "来源URL（已移除签名；下载时须重新授权获取）", "状态"])
        w.writerows(rows)

    print(f"\n完成 {ok} / 共 {len(targets)}，跳过 {skipped}，失败 {len(fail)}")
    for x in fail:
        print("  失败:", x)
    print("输出:", OUT)


if __name__ == "__main__":
    main()
