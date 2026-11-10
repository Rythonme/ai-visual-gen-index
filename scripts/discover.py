# -*- coding: utf-8 -*-
"""
新资源自动发现与收录（v2.0）
=========================================================
每次运行都通过 GitHub 公开搜索 API 找出近期新建且热度较高的生图 / 生视频项目，
经 config.json -> auto_admit 中的护栏过滤后，**自动写入 data/auto_tools.json**，
由 build.py 合并进榜单，实现新资源自动进榜。

分层原则（重要）：
  data/tools.json       人工维护层，脚本永远只读、绝不改写
  data/auto_tools.json  自动收录层，由本脚本增量写入，可随时人工转正 / 下架
  build.py              合并两层后计算榜单；id 或仓库冲突时人工层优先

护栏（全部可在 config.json 调整）：
  Star 阈值 / 新建窗口 / 生图生视频关键词白名单 / 营销与工具类黑名单 /
  归档与 fork 排除 / 每轮新增上限 / 自动层总量上限 / 与两层清单去重

输出（审计轨迹）：
  data/auto_tools.json   自动收录层（机器可读）
  data/candidates.json   本轮检索与收录明细（含被拒原因）
  reports/candidates.md  人读版收录报告

用法：
  python scripts/discover.py              # 检索并自动收录
  python scripts/discover.py --dry-run    # 只预览，不写任何文件
  python scripts/discover.py --verbose    # 打印每条判定

环境变量：GITHUB_TOKEN / GH_TOKEN（GitHub Actions 自动注入；匿名亦可，限额更低）
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UA = "ai-visual-gen-index/2.0 (auto discovery)"
CN_TZ = timezone(timedelta(hours=8))

QUERIES = [
    '"image generation" in:description stars:>300',
    '"video generation" in:description stars:>300',
    '"text-to-image" in:name,description stars:>200',
    '"text-to-video" in:name,description stars:>200',
    '"diffusion" "comfyui" in:description stars:>150',
    '"image model" in:name,description stars:>200',
    '"video model" in:name,description stars:>200',
]


def load_json(path: Path, default=None):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def human_time() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M") + " (UTC+8)"


def search(q: str, since: str, token: str | None):
    full_q = f"{q} created:>{since}"
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({
        "q": full_q, "sort": "stars", "order": "desc", "per_page": 30,
    })
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8")).get("items", [])


def guard(repo: dict, ac: dict):
    """返回 (是否通过, 拒绝原因)。护栏规则全部来自 data/config.json。"""
    name = repo.get("full_name", "") or ""
    desc = repo.get("description") or ""
    text = (name + " " + desc).lower()
    stars = int(repo.get("stargazers_count") or 0)

    if stars < int(ac.get("min_stars", 300)):
        return False, f"Stars {stars} 低于阈值 {ac.get('min_stars')}"
    if ac.get("require_description") and not desc.strip():
        return False, "缺少项目简介"
    min_len = int(ac.get("min_description_length", 0))
    if min_len and len(desc.strip()) < min_len:
        return False, f"简介过短（{len(desc.strip())} < {min_len} 字），信息不足"
    if ac.get("exclude_archived") and repo.get("archived"):
        return False, "仓库已归档"
    if ac.get("exclude_forks") and repo.get("fork"):
        return False, "Fork 仓库"
    if not any(k in text for k in ac.get("include_keywords", [])):
        return False, "未命中生图 / 生视频关键词"
    hit = next((k for k in ac.get("exclude_keywords", []) if k in text), None)
    if hit:
        return False, f"命中排除词「{hit}」"
    return True, ""


def relevance(repo: dict, ac: dict) -> float:
    """
    相关性优先于纯 Star：领域关键词命中数 + Star 对数 + 明确许可证 + 官方机构加分，
    周边 ComfyUI 插件与评测榜降权。权重全部来自 config.json -> relevance_weights。
    """
    full = (repo.get("full_name", "") or "").lower()
    desc = (repo.get("description") or "").lower()
    text = full + " " + desc
    rw = ac.get("relevance_weights") or {}
    hits = sum(1 for k in ac.get("include_keywords", []) if k in text)
    lic = (repo.get("license") or {}).get("spdx_id") or ""
    has_license = 1 if lic and lic not in ("NOASSERTION", "NONE") else 0
    stars = int(repo.get("stargazers_count") or 0)
    score = (hits * float(rw.get("keyword_hit", 10))
             + math.log10(stars + 1) * float(rw.get("stars_log", 20))
             + has_license * float(rw.get("license", 8)))
    owner = full.split("/")[0] if "/" in full else ""
    if owner in {o.lower() for o in ac.get("preferred_orgs", [])}:
        score += float(rw.get("preferred_org", 45))
    short = full.split("/")[-1]
    if short.startswith("comfyui-") or any(k in text for k in ("workflow for", "plugin for", "node for")):
        score += float(rw.get("plugin_penalty", -40))
    if any(k in text for k in ("benchmark", "leaderboard")):
        score += float(rw.get("benchmark_penalty", -15))
    return score


def guess_category(name: str, desc: str) -> str:
    t = (name + " " + desc).lower()
    if any(k in t for k in ("benchmark", "leaderboard", "arena", "评测榜", "榜单")):
        return "resource"
    if any(k in t for k in ("controlnet", "ip-adapter", "lora", "inpaint", "upscal",
                            "super resolution", "image editing", "video editing")):
        return "edit"
    if any(k in t for k in ("comfyui", "webui", "studio", "workflow", "plugin", "node", "interface")):
        return "tool"
    if any(k in t for k in ("video", "t2v", "i2v", "film", "animate", "视频")):
        return "video_model"
    return "image_model"


def make_id(repo: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", repo.lower()).strip("-")
    return "auto-" + slug[:48]


def to_tool(repo: dict, ac: dict, query: str) -> dict:
    """把 GitHub 搜索结果转换成一条合规的榜单条目（字段与 tools.json 一致）。"""
    full = repo.get("full_name", "")
    owner = full.split("/")[0] if "/" in full else ""
    short = full.split("/")[-1] if "/" in full else full
    desc = (repo.get("description") or "").strip()
    lang = repo.get("language") or ""
    lic = (repo.get("license") or {}).get("spdx_id") or ""
    if lic in ("NOASSERTION", "NONE", ""):
        lic = "详见仓库"
    url = repo.get("html_url") or f"https://github.com/{full}"
    category = guess_category(full, desc)
    tags = ["自动收录", "待复核"] + ([lang] if lang else [])
    return {
        "id": make_id(full),
        "name": short,
        "alias": "自动收录 · 待复核",
        "category": category,
        "type": "resource" if category == "resource" else "open",
        "org": owner,
        "desc": desc[:180] if desc else "自动收录的新项目，中文简介待维护者补充。",
        "links": {"home": url, "github": url},
        "github": full,
        "license": lic,
        "tags": tags,
        "added": datetime.now(CN_TZ).strftime("%Y-%m-%d"),
        "scores": dict(ac.get("default_scores", {})),
        "seed_stars": int(repo.get("stargazers_count") or 0),
        "auto_admitted": True,
        "admitted_at": datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M"),
        "review_status": ac.get("review_status", "pending"),
        "source_query": query,
        "source_stars": int(repo.get("stargazers_count") or 0),
        "source_relevance": round(relevance(repo, ac), 1),
        "source_created": (repo.get("created_at") or "")[:10],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="自动发现并收录 AI 生图 / 生视频新资源")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写任何文件")
    ap.add_argument("--verbose", action="store_true", help="打印每条判定")
    args = ap.parse_args()

    cfg = load_json(DATA / "config.json", {}) or {}
    ac = cfg.get("auto_admit") or {}
    if not ac.get("enabled", False):
        print("[discover] auto_admit.enabled = false，跳过自动收录")
        return 0

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    days = int(ac.get("lookback_days", 120))
    since = (datetime.now(CN_TZ) - timedelta(days=days)).strftime("%Y-%m-%d")

    manual = (load_json(DATA / "tools.json", {}) or {}).get("tools", [])
    auto_doc = load_json(DATA / "auto_tools.json", {}) or {}
    existing = auto_doc.get("tools", [])
    known_repos = {str(t.get("github", "")).lower() for t in manual if t.get("github")}
    known_repos |= {str(t.get("github", "")).lower() for t in existing if t.get("github")}
    known_ids = {t.get("id") for t in manual} | {t.get("id") for t in existing}

    found: dict[str, dict] = {}
    for q in QUERIES:
        try:
            rows = search(q, since, token)
            print(f"[discover] {q} -> {len(rows)} 条")
            for r in rows:
                name = r.get("full_name", "")
                if name and name.lower() not in found:
                    r["_q"] = q
                    found[name.lower()] = r
        except urllib.error.HTTPError as exc:
            print(f"[discover] 查询失败 HTTP {exc.code}：{q}")
        except Exception as exc:
            print(f"[discover] 查询失败 {type(exc).__name__}：{q}")

    if ac.get("sort_by_relevance", True):
        hits = sorted(found.values(), key=lambda r: -relevance(r, ac))
    else:
        hits = sorted(found.values(), key=lambda r: -int(r.get("stargazers_count") or 0))
    admitted, rejected, known = [], [], []
    for r in hits:
        name = r.get("full_name", "")
        if not name:
            continue
        if name.lower() in known_repos or make_id(name) in known_ids:
            known.append(name)
            continue
        ok, reason = guard(r, ac)
        if not ok:
            rejected.append({
                "repo": name, "stars": int(r.get("stargazers_count") or 0),
                "reason": reason, "description": (r.get("description") or "")[:160],
            })
            if args.verbose:
                print(f"  [拒] {name}: {reason}")
            continue
        admitted.append(to_tool(r, ac, r.get("_q", "")))
        if args.verbose:
            print(f"  [收] {name} -> {admitted[-1]['category']}")

    max_per_run = int(ac.get("max_per_run", 8))
    deferred = admitted[max_per_run:]
    admitted = admitted[:max_per_run]
    if deferred:
        print(f"[discover] 本轮新增上限 {max_per_run}，{len(deferred)} 个顺延到下次运行")

    # 合并并应用总量上限（超出时按 Star 规模保留，避免自动层无限膨胀）
    merged = existing + admitted
    max_total = int(ac.get("max_total", 60))
    retired = []
    if len(merged) > max_total:
        merged_sorted = sorted(merged, key=lambda x: -(int(x.get("source_stars") or x.get("seed_stars") or 0)))
        keep, drop = merged_sorted[:max_total], merged_sorted[max_total:]
        retired = [x.get("github", "") for x in drop]
        merged = sorted(keep, key=lambda x: x.get("admitted_at", ""))

    new_doc = {
        "generated": human_time(),
        "note": "本文件由 scripts/discover.py 自动维护；人工核实后可把条目移入 data/tools.json 转正，或直接删掉下架。",
        "config_version": ac.get("version", "2.0"),
        "count": len(merged),
        "tools": merged,
    }

    stats = {
        "hit": len(hits),
        "admitted_this_run": len(admitted),
        "rejected": len(rejected),
        "already_known": len(known),
        "deferred": len(deferred),
        "retired": len(retired),
        "total_auto": len(merged),
    }
    print(f"[discover] 命中 {stats['hit']} ｜ 自动收录 {stats['admitted_this_run']} ｜ "
          f"护栏拒绝 {stats['rejected']} ｜ 已在榜 {stats['already_known']} ｜ 自动层共 {stats['total_auto']} 条")

    if args.dry_run:
        print("[discover] --dry-run：未写入任何文件")
        for t in admitted:
            print(f"   + {t['github']} ({t['source_stars']} stars, {t['category']})")
        return 0

    save_json(DATA / "auto_tools.json", new_doc)
    payload = {
        "generated": human_time(),
        "window": f"近 {days} 天新建（created:>{since}）",
        "queries": QUERIES,
        "note": "符合护栏的候选已自动收录进 data/auto_tools.json 并进入榜单；本文件保留被拒原因供复核。",
        "stats": stats,
        "admitted": [{"repo": t["github"], "stars": t["source_stars"], "category": t["category"],
                      "admitted_at": t["admitted_at"], "url": t["links"]["github"]} for t in admitted],
        "rejected": rejected,
        "retired": retired,
        "candidates": [{
            "repo": r.get("full_name"), "url": r.get("html_url"),
            "stars": int(r.get("stargazers_count") or 0),
            "description": (r.get("description") or "")[:220],
            "language": r.get("language") or "",
            "license": (r.get("license") or {}).get("spdx_id") or "",
            "created_at": (r.get("created_at") or "")[:10],
            "pushed_at": (r.get("pushed_at") or "")[:10],
        } for r in hits],
    }
    save_json(DATA / "candidates.json", payload)

    lines = [
        "# 新资源自动收录报告",
        "",
        f"生成时间：{payload['generated']} ｜ 检索窗口：{payload['window']}",
        "",
        f"本轮命中 **{stats['hit']}** 个仓库：**自动收录 {stats['admitted_this_run']} 个**、"
        f"护栏拒绝 {stats['rejected']} 个、已在榜 {stats['already_known']} 个；自动收录层目前共 **{stats['total_auto']}** 条。",
        "",
        "> 符合护栏的候选已由 `scripts/discover.py` 自动写入 `data/auto_tools.json` 并进入榜单，"
        "带「自动收录 · 待复核」标记。**人工清单 `data/tools.json` 不会被脚本改写**。"
        "维护者可把优质条目转正（移入 tools.json）或删掉下架，方法见 CONTRIBUTING.md。",
        "",
        f"## 本轮自动收录（{len(admitted)}）",
        "",
        "| # | 仓库 | Stars | 推断分类 | 收录时间 | 链接 |",
        "|---|---|---|---|---|---|",
    ]
    for i, t in enumerate(admitted, 1):
        lines.append(f"| {i} | {t['github']} | {t['source_stars']:,} | {t['category']} | "
                     f"{t['admitted_at']} | [GitHub]({t['links']['github']}) |")
    if not admitted:
        lines.append("| — | 本轮无符合条件的新仓库 | — | — | — | — |")

    lines += ["", f"## 被护栏拒绝（{len(rejected)}）", "",
              "| 仓库 | Stars | 拒绝原因 |", "|---|---|---|"]
    for r in rejected[:40]:
        lines.append(f"| {r['repo']} | {r['stars']:,} | {r['reason']} |")
    if not rejected:
        lines.append("| — | — | 无 |")

    lines += ["", "## 自动收录层当前条目", "",
              "| 仓库 | Stars | 分类 | 收录时间 |", "|---|---|---|---|"]
    for t in sorted(merged, key=lambda x: x.get("admitted_at", ""), reverse=True)[:60]:
        lines.append(f"| {t.get('github','')} | {int(t.get('source_stars') or t.get('seed_stars') or 0):,} | "
                     f"{t.get('category','')} | {t.get('admitted_at','')} |")
    if retired:
        lines += ["", f"> 本轮因总量上限淘汰 {len(retired)} 条：" + "、".join(retired)]
    lines += ["", "---", "", "[← 返回项目首页](../README.md)", ""]
    save_text(DATA.parent / "reports" / "candidates.md", "\n".join(lines))
    print(f"[discover] 已写入 data/auto_tools.json、data/candidates.json、reports/candidates.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
