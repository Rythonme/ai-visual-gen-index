# -*- coding: utf-8 -*-
"""
外链可用性校验（只发 HEAD/GET 请求读取响应码，不下载任何内容）。

判定口径（刻意保守，避免把反爬/网络不通误判为链接失效）：
  ok       -> HTTP 2xx / 3xx
  fail     -> 明确的 404 / 410 / 5xx（真正的失效）
  unknown  -> 超时、DNS 失败、403 反爬、429 限流等无法确认的情况

结果写入 data/link_status.json，由 build.py 读取并在网站上标记校验状态。
用法：python scripts/check_links.py [--timeout 10] [--workers 8]
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (compatible; ai-visual-gen-index-linkcheck/1.0)"
CN_TZ = timezone(timedelta(hours=8))


def load_json(path: Path, default=None):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def check_one(url: str, timeout: int) -> str:
    headers = {"User-Agent": UA, "Accept": "*/*"}
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                # GET 时只读 1 个字节，不下载页面内容
                if method == "GET":
                    resp.read(1)
                return "ok"
        except urllib.error.HTTPError as exc:
            code = exc.code
            if code in (404, 410) or 500 <= code < 600:
                # 部分站点对 HEAD 直接返回 404 但 GET 正常，先回退 GET 复核再判失效
                if method == "HEAD":
                    continue
                return "fail"
            if code in (403, 405, 429) and method == "HEAD":
                continue  # 部分站点拒绝 HEAD，回退 GET 再试
            return "unknown"  # 403 反爬等一律不算失效
        except Exception:
            if method == "HEAD":
                continue
            return "unknown"
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=10)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    tools = load_json(ROOT / "data" / "tools.json", {}) or {}
    urls = []
    for t in tools.get("tools", []):
        for u in (t.get("links") or {}).values():
            if isinstance(u, str) and u.startswith("http") and u not in urls:
                urls.append(u)
    print(f"[linkcheck] 待校验 {len(urls)} 个唯一链接，并发 {args.workers}")

    result = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_one, u, args.timeout): u for u in urls}
        for fut in as_completed(futures):
            result[futures[fut]] = fut.result()

    summary = {k: list(result.values()).count(k) for k in ("ok", "fail", "unknown")}
    failed = [u for u, v in sorted(result.items()) if v == "fail"]
    payload = {
        "checked_at": datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M") + " (UTC+8)",
        "method": "HEAD 优先，405/403 回退 GET；超时与反爬记为 unknown 而非失效",
        "links": dict(sorted(result.items())),
        "summary": summary,
        "failed": failed,
    }
    out = ROOT / "data" / "link_status.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"[linkcheck] ok={summary['ok']} fail={summary['fail']} unknown={summary['unknown']}")
    if failed:
        print("[linkcheck] 明确失效的链接：")
        for u in failed:
            print("  -", u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
