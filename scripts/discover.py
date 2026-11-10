# -*- coding: utf-8 -*-
"""
新资源发现（只提候选，绝不自动写入主清单）。

每周通过 GitHub 公开搜索 API 找出近期新建且热度较高的生图 / 生视频项目，
与 data/tools.json 中已收录的仓库去重后，输出：
  data/candidates.json      机器可读候选
  reports/candidates.md     人工审核清单

收录与否必须由维护者人工确认（见 CONTRIBUTING.md），避免榜单被营销仓库污染。
用法：python scripts/discover.py
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "ai-visual-gen-index/1.0 (candidate discovery)"
CN_TZ = timezone(timedelta(hours=8))
QUERIES = [
    '"image generation" in:description stars:>300',
    '"video generation" in:description stars:>300',
    '"text-to-image" in:name,description stars:>200',
    '"text-to-video" in:name,description stars:>200',
    '"diffusion" "comfyui" in:description stars:>150',
]


def load_json(path: Path, default=None):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def search(q: str, since: str, token: str | None):
    full_q = f"{q} created:>{since}"
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({
        "q": full_q, "sort": "stars", "order": "desc", "per_page": 30,
    })
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8")).get("items", [])


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    since = (datetime.now(CN_TZ) - timedelta(days=120)).strftime("%Y-%m-%d")
    known = set()
    for t in (load_json(ROOT / "data" / "tools.json", {}) or {}).get("tools", []):
        if t.get("github"):
            known.add(t["github"].lower())

    found = {}
    for q in QUERIES:
        try:
            items = search(q, since, token)
            print(f"[discover] {q} -> {len(items)} 条")
            for r in items:
                name = r.get("full_name", "")
                if not name or name.lower() in known or name in found:
                    continue
                found[name] = {
                    "repo": name,
                    "url": r.get("html_url"),
                    "stars": int(r.get("stargazers_count") or 0),
                    "description": (r.get("description") or "")[:220],
                    "language": r.get("language") or "",
                    "license": (r.get("license") or {}).get("spdx_id") or "",
                    "created_at": r.get("created_at", "")[:10],
                    "pushed_at": r.get("pushed_at", "")[:10],
                    "query": q,
                }
        except urllib.error.HTTPError as exc:
            print(f"[discover] 查询失败 HTTP {exc.code}：{q}")
        except Exception as exc:
            print(f"[discover] 查询失败 {type(exc).__name__}：{q}")

    rows = sorted(found.values(), key=lambda x: -x["stars"])[:60]
    payload = {
        "generated": datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M") + " (UTC+8)",
        "window": f"近 120 天新建（created:>{since}）",
        "queries": QUERIES,
        "note": "仅为候选，需人工核实相关性、链接与许可证后，再手工加入 data/tools.json。",
        "candidates": rows,
    }
    out = ROOT / "data" / "candidates.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    lines = [
        "# 新资源候选清单（人工审核）",
        "",
        f"生成时间：{payload['generated']} ｜ 检索窗口：{payload['window']} ｜ 候选 {len(rows)} 个。",
        "",
        "> 这些只是 GitHub 搜索命中的候选，**并未被自动收录**。请逐个核实是否属于 AI 生图 / 生视频范畴、"
        "链接是否官方、许可证与实用性评分是否合理，再由维护者手工加入 `data/tools.json`。",
        "",
        "| # | 仓库 | Stars | 语言 | 许可证 | 创建 | 简介 |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, c in enumerate(rows, 1):
        desc = c["description"].replace("|", "\\|")
        lines.append(f"| {i} | [{c['repo']}]({c['url']}) | {c['stars']:,} | {c['language']} | {c['license']} | {c['created_at']} | {desc} |")
    lines += ["", "---", "", "[← 返回项目首页](../README.md)", ""]
    (ROOT / "reports").mkdir(exist_ok=True)
    with (ROOT / "reports" / "candidates.md").open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[discover] 输出 {len(rows)} 个候选 -> reports/candidates.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
