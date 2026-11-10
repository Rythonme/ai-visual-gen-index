# -*- coding: utf-8 -*-
"""
AI 视觉生成资源榜 · 榜单构建 / 周更主脚本
=========================================================
职责：
  1. 合并人工层 data/tools.json（只读，人工维护）与自动收录层 data/auto_tools.json
     （由 scripts/discover.py 每次检索后增量写入，带待复核标记）；
  2. 通过 GitHub / Hugging Face 公开 API 拉取热度与项目信息（只读元数据，绝不下载模型或素材）；
  3. 按 data/config.json 中公开的算法计算 热度分 / 实用性分 / 综合分 / 上升分；
  4. 生成 data/rankings.json、docs/data.js、docs/data.json、README 榜单区块、周报与历史快照。

零第三方依赖，仅用 Python 标准库，便于在 GitHub Actions 里直接运行。

用法：
  python scripts/build.py                  # 正常构建（自动尝试刷新公开数据）
  python scripts/build.py --no-refresh     # 完全离线，只用缓存 / 基线值
  python scripts/build.py --verbose         # 打印抓取明细

环境变量：
  GITHUB_TOKEN / GH_TOKEN  可选。GitHub Actions 会自动注入内置令牌（5000 次/小时）；
                          不提供时走匿名限额（60 次/小时），脚本会自动降级，不会失败。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
for _p in (DATA, DOCS, REPORTS):
    _p.mkdir(parents=True, exist_ok=True)

CN_TZ = timezone(timedelta(hours=8))
UA = "ai-visual-gen-index/1.0 (weekly ranking bot)"
BEGIN_MARK = "<!-- BEGIN AUTO-GENERATED RANKING -->"
END_MARK = "<!-- END AUTO-GENERATED RANKING -->"


# ---------------------------------------------------------------- 基础工具
def now_cn() -> datetime:
    return datetime.now(CN_TZ)


def human_time() -> str:
    return now_cn().strftime("%Y-%m-%d %H:%M") + " (UTC+8)"


def week_key() -> str:
    d = now_cn().isocalendar()
    return f"{d.year}-W{d.week:02d}"


def load_json(path: Path, default=None):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
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


def clamp(x, lo=0.0, hi=100.0) -> float:
    return max(lo, min(hi, x))


def log(message: str) -> None:
    print(f"[build] {message}", flush=True)


def http_get_json(url: str, token: str | None = None, timeout: int = 12):
    """只读 GET 一个公开 JSON 接口；失败抛异常，由调用方降级处理。"""
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_github_time(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


# ---------------------------------------------------------------- 资源清单（分层合并）
def load_tools(config):
    """
    人工层 data/tools.json 只读、绝不改写；自动层 data/auto_tools.json 由 discover.py 维护。
    id 或 GitHub 仓库冲突时人工层优先，保证「转正」后不会出现重复条目。
    返回 (合并后的清单, 实际生效的自动收录条目数)。
    """
    manual = (load_json(DATA / "tools.json", {}) or {}).get("tools", [])
    ac = config.get("auto_admit") or {}
    auto = (load_json(DATA / "auto_tools.json", {}) or {}).get("tools", []) if ac.get("enabled") else []
    manual_ids = {t.get("id") for t in manual}
    manual_repos = {str(t.get("github", "")).lower() for t in manual if t.get("github")}
    merged = list(manual)
    seen_ids, seen_repos = set(manual_ids), set(manual_repos)
    for t in auto:
        rid, repo = t.get("id"), str(t.get("github", "")).lower()
        if not rid or rid in seen_ids or (repo and repo in seen_repos):
            continue
        merged.append(t)
        seen_ids.add(rid)
        if repo:
            seen_repos.add(repo)
    return merged, len(merged) - len(manual)


# ---------------------------------------------------------------- 公开数据抓取
def github_budget(token: str | None, wanted: int, verbose: bool) -> int:
    """查询剩余 API 额度，返回本次允许抓取的仓库数量。"""
    if not wanted:
        return 0
    try:
        d = http_get_json("https://api.github.com/rate_limit", token, timeout=8)
        remaining = int(d.get("resources", {}).get("core", {}).get("remaining", 0))
        allowed = max(0, remaining - 2)
        if verbose:
            log(f"GitHub API 剩余额度 {remaining}，本次最多抓取 {min(allowed, wanted)} 个仓库")
        return min(allowed, wanted)
    except Exception as exc:
        if verbose:
            log(f"额度查询失败（{type(exc).__name__}），按 {5000 if token else 0} 处理")
        return 5000 if token else 0


def fetch_repo(repo: str, token: str | None):
    """抓取单个仓库的公开元数据。只读元数据，不 clone、不下载任何文件。"""
    d = http_get_json(f"https://api.github.com/repos/{repo}", token)
    lic = d.get("license") or {}
    return {
        "full_name": d.get("full_name") or repo,
        "stars": int(d.get("stargazers_count") or 0),
        "forks": int(d.get("forks_count") or 0),
        "open_issues": int(d.get("open_issues_count") or 0),
        "pushed_at": d.get("pushed_at"),
        "created_at": d.get("created_at"),
        "description": d.get("description") or "",
        "license": lic.get("spdx_id") or "",
        "language": d.get("language") or "",
        "archived": bool(d.get("archived")),
        "html_url": d.get("html_url") or f"https://github.com/{repo}",
        "source": "api",
        "fetched_at": now_cn().isoformat(timespec="seconds"),
    }


def http_get_text(url: str, timeout: int = 12) -> str:
    """读取网页 HTML 文本（仅用于提取公开元数据，不下载模型 / 素材）。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_repo_html(repo: str, timeout: int = 12):
    """
    API 限流时的回退数据源：GitHub 仓库公开页面内嵌了 stargazerCount / forksCount /
    license spdxId / 官方简介等 JSON 片段。这只读取一个页面的公开元数据，
    不 clone 仓库、不下载任何权重、数据集或素材。
    """
    page = http_get_text(f"https://github.com/{repo}", timeout)

    def grab(pattern, default=""):
        m = re.search(pattern, page)
        return m.group(1) if m else default

    stars = int(grab(r'"stargazerCount":(\d+)', "0") or 0)
    forks = int(grab(r'"forksCount":(\d+)', "0") or 0)
    if not stars:
        raise ValueError("页面未包含 Star 元数据")
    desc = grab(r'<meta name="description" content="([^"]*)"')
    import html as html_lib
    desc = html_lib.unescape(desc)
    desc = re.sub(r"\s+-\s+" + re.escape(repo) + r"\s*$", "", desc)
    return {
        "full_name": repo,
        "stars": stars,
        "forks": forks,
        "open_issues": 0,
        "pushed_at": "",
        "created_at": grab(r'"createdAt":"([^"]+)"'),
        "description": desc,
        "license": grab(r'"license":\{"spdxId":"([^"]+)"'),
        "language": "",
        "archived": grab(r'"isArchived":(true|false)') == "true",
        "html_url": f"https://github.com/{repo}",
        "source": "html",
        "fetched_at": now_cn().isoformat(timespec="seconds"),
    }


def fetch_hf(model_id: str):
    """抓取 Hugging Face 模型卡的 likes / downloads；网络不通时调用方会整批跳过。"""
    d = http_get_json(f"https://huggingface.co/api/models/{model_id}", timeout=8)
    return {
        "likes": int(d.get("likes") or 0),
        "downloads": int(d.get("downloads") or 0),
        "last_modified": d.get("lastModified") or "",
        "source": "api",
        "fetched_at": now_cn().isoformat(timespec="seconds"),
    }


def refresh_metrics(tools, token, args) -> dict:
    """刷新公开指标；任何失败都自动回退到缓存或基线值，保证榜单永远能生成。"""
    cache = load_json(DATA / "metrics_cache.json", {}) or {}
    repos = cache.setdefault("repos", {})
    hfs = cache.setdefault("hf", {})

    candidates = [t for t in tools if t.get("github")]
    # 优先刷新热度高 / 尚无缓存的仓库，让有限的匿名额度用到刀刃上
    candidates.sort(key=lambda t: (
        0 if t["id"] not in repos else 1,
        -(t.get("seed_stars") or t.get("heat_baseline") or 0),
    ))
    budget = 0 if args.no_refresh else github_budget(token, len(candidates), args.verbose)
    done = 0
    html_ok = 0
    for t in candidates:
        repo = t["github"]
        refreshed = False
        if done < budget:
            try:
                repos[repo] = fetch_repo(repo, token)
                done += 1
                refreshed = True
            except urllib.error.HTTPError as exc:
                if exc.code in (403, 429):
                    budget = done  # 后续全部改走公开页面回退
                    log("GitHub API 触发限流，改用仓库公开页面补充元数据")
                elif args.verbose:
                    log(f"{repo} API HTTP {exc.code}，改用网页回退")
            except Exception as exc:
                if args.verbose:
                    log(f"{repo} API 异常 {type(exc).__name__}，改用网页回退")
        if not refreshed:
            cached = repos.get(repo)
            if cached and cached.get("source") in ("api", "html"):
                continue  # 已有上次实取数据，不重复请求
            try:
                repos[repo] = fetch_repo_html(repo)
                html_ok += 1
            except Exception as exc:
                if args.verbose:
                    log(f"{repo} 网页回退失败 {type(exc).__name__}，沿用基线")
    if html_ok:
        log(f"通过 GitHub 公开页面补充实取 {html_ok} 个仓库的 Star / Fork")

    # 首次运行且完全抓不到数据时，用人工录入的 seed_stars 生成保底快照
    for t in candidates:
        repo = t["github"]
        if repo not in repos:
            repos[repo] = {
                "full_name": repo,
                "stars": int(t.get("seed_stars") or 0),
                "forks": 0,
                "open_issues": 0,
                "pushed_at": "",
                "created_at": "",
                "description": "",
                "license": "",
                "language": "",
                "archived": False,
                "html_url": f"https://github.com/{repo}",
                "source": "seed",
                "fetched_at": now_cn().isoformat(timespec="seconds"),
            }

    # Hugging Face：先探活，避免逐条超时拖慢周更
    hf_ids = [t["hf_model"] for t in tools if t.get("hf_model")]
    if hf_ids and not args.no_refresh:
        try:
            http_get_json("https://huggingface.co/api/models/gpt2", timeout=5)
            for mid in hf_ids:
                try:
                    hfs[mid] = fetch_hf(mid)
                except Exception:
                    pass
            if args.verbose:
                log(f"Hugging Face 指标已刷新 {sum(1 for m in hf_ids if m in hfs)}/{len(hf_ids)} 条")
        except Exception:
            log("Hugging Face 当前网络不可达，本次跳过（不影响榜单生成）")

    # 清理已不在清单里的旧缓存
    live_repos = {t["github"] for t in tools if t.get("github")}
    cache["repos"] = {k: v for k, v in repos.items() if k in live_repos}
    live_hf = set(hf_ids)
    cache["hf"] = {k: v for k, v in hfs.items() if k in live_hf}
    cache["generated"] = human_time()
    return cache


# ---------------------------------------------------------------- 评分
def score_items(tools, config, metrics, history, link_status):
    w = config["scoring"]["weights"]
    wp = w["practical"]
    wh = w["heat"]
    wo = w["overall"]
    s = config["scoring"]
    scale = s["stars_scale"]

    # 本周星标序列（用于增速与迷你趋势图）
    star_series = history.get("stars", {})
    items = []

    # 识别「同日批量导入」：项目初次建库时 90 条人工条目 added 为同一天，
    # 不应把整库都算作「新收录」；只有零散人工新增才进入新收录榜。
    auto_cfg = config.get("auto_admit") or {}
    batch_threshold = int(auto_cfg.get("recent_batch_threshold", 5))
    added_counts = {}
    for t in tools:
        k = str(t.get("added") or "")[:10]
        if k:
            added_counts[k] = added_counts.get(k, 0) + 1

    for t in tools:
        practical = sum(wp[k] * float(t["scores"].get(k, 3)) for k in wp) / 5.0 * 100.0
        practical = round(clamp(practical), 1)

        repo_key = t.get("github")
        m = (metrics.get("repos", {}).get(repo_key) or {}) if repo_key else {}
        stars = int(m.get("stars") or t.get("seed_stars") or 0)
        forks = int(m.get("forks") or 0)
        pushed = parse_github_time(m.get("pushed_at"))
        days_since_push = (now_cn() - pushed).days if pushed else None
        source = m.get("source") if m else None

        series = [v for v in star_series.get(t["id"], []) if isinstance(v, (int, float))]
        # 增速基准取「上一次快照」；同一周重复构建时快照值不变，视为历史不足而非零增长
        prev = series[-1] if series else None
        base = None
        if prev and prev > 0 and prev != stars:
            base = prev
        elif len(series) >= 2:
            older = series[max(0, len(series) - 5)]
            base = older if older > 0 and older != stars else None
        growth_pct = round((stars - base) / base * 100, 2) if base else None

        star_score = clamp(math.log10(stars + 1) / math.log10(scale + 1) * 100) if stars else 0.0
        if growth_pct is None:
            growth_score = 50.0  # 历史不足时用中性值，不惩罚也不奖励
        else:
            growth_score = clamp(growth_pct / s["growth_full_score_pct"] * 100)
        if days_since_push is None:
            # 缺少提交时间（离线 / 网页回退）时按 Star 规模派生，避免把"未知"误判为"不活跃"
            activity_score = clamp(star_score * 0.9) if source != "api" else 50.0
        else:
            full = s["activity_full_score_days"]
            zero = s["activity_zero_score_days"]
            activity_score = clamp(100.0 * (zero - days_since_push) / (zero - full))
        if forks:
            fork_score = clamp(math.log10(forks + 1) / math.log10(scale / 3 + 1) * 100)
        elif stars:
            fork_score = clamp(star_score * 0.85)  # 缺 fork 数时的保守近似
        else:
            fork_score = 30.0
        hf = metrics.get("hf", {}).get(t.get("hf_model"), {}) if t.get("hf_model") else {}
        hf_likes = int(hf.get("likes") or 0)
        hf_downloads = int(hf.get("downloads") or 0)
        hf_score = clamp(math.log10(hf_downloads + hf_likes * 100 + 1) / 8.0 * 100) if (hf_likes or hf_downloads) else None
        community_score = (fork_score * 0.6 + hf_score * 0.4) if hf_score is not None else fork_score

        if m or repo_key:
            heat = (wh["stars"] * star_score + wh["growth"] * growth_score
                    + wh["activity"] * activity_score + wh["community"] * community_score)
            heat_source = {
                "api": "GitHub API",
                "html": "GitHub 公开页面",
                "cache": "缓存快照",
            }.get(source, "人工基线星标")
        else:
            heat = float(t.get("heat_baseline") or 50)
            heat_source = "人工基线（闭源/无仓库）"

        heat = round(clamp(heat), 1)
        overall = round(clamp(wo["heat"] * heat + wo["practical"] * practical), 1)
        momentum = round(clamp(growth_score if growth_pct is not None else activity_score), 1)

        # 链接可用性（由 scripts/check_links.py 生成，缺失时显示"未校验"）
        urls = [u for u in (t.get("links") or {}).values() if isinstance(u, str) and u.startswith("http")]
        statuses = [link_status.get("links", {}).get(u, "unknown") for u in urls]
        if statuses and all(v == "ok" for v in statuses):
            link_state = "ok"
        elif any(v == "fail" for v in statuses):
            link_state = "fail"
        else:
            link_state = "unknown"

        # 新收录榜：自动收录条目恒为「近期」，人工条目按 added 日期计算新鲜度
        recent_days = max(1, int(auto_cfg.get("recent_days", 60)))
        raw_added = str(t.get("admitted_at") or t.get("added") or "")
        added_dt = None
        for fmt, cut in (("%Y-%m-%d %H:%M", 16), ("%Y-%m-%d", 10)):
            try:
                added_dt = datetime.strptime(raw_added[:cut], fmt)
                break
            except (ValueError, TypeError):
                continue
        days_since_added = (now_cn().replace(tzinfo=None) - added_dt).days if added_dt else None
        if days_since_added is not None:
            days_since_added = max(0, days_since_added)
        same_day = added_counts.get(str(t.get("added") or "")[:10], 0)
        is_batch_import = same_day > batch_threshold
        is_recent = bool(t.get("auto_admitted")) or (
            days_since_added is not None and days_since_added <= recent_days
            and not is_batch_import)
        recency = round(clamp(100.0 - (days_since_added if days_since_added is not None else 9999)
                              * 100.0 / recent_days), 1)

        items.append({
            "id": t["id"],
            "name": t["name"],
            "alias": t.get("alias", ""),
            "category": t["category"],
            "type": t.get("type", "open"),
            "org": t.get("org", ""),
            "desc": t.get("desc", ""),
            "tags": t.get("tags", []),
            "license": t.get("license", ""),
            "links": t.get("links", {}),
            "github": repo_key or "",
            "hf_model": t.get("hf_model", ""),
            "added": t.get("added", ""),
            "scores": t.get("scores", {}),
            "practical": practical,
            "heat": heat,
            "heat_source": heat_source,
            "overall": overall,
            "momentum": momentum,
            "growth_pct": growth_pct,
            "stars": stars,
            "forks": forks,
            "days_since_push": days_since_push,
            "official_description": m.get("description", ""),
            "repo_license": m.get("license", ""),
            "data_source": source or "manual",
            "link_state": link_state,
            "spark": series[-12:],
            "auto_admitted": bool(t.get("auto_admitted")),
            "admitted_at": t.get("admitted_at", ""),
            "review_status": t.get("review_status", ""),
            "is_recent": is_recent,
            "recency": recency,
        })
    return items


def rank_by(items, key):
    return sorted(items, key=lambda x: (-x[key], -x["overall"], x["name"]))


def board_items(items):
    """主榜只排名工具 / 模型 / 平台；资源评测类作为参考入口，不参与名次竞争。"""
    return [x for x in items if x["type"] != "resource"]


# ---------------------------------------------------------------- 历史快照
def update_history(items, prev_rankings, week, max_weeks=26):
    hist = load_json(DATA / "history.json", {}) or {}
    hist.setdefault("weeks", [])
    hist.setdefault("stars", {})
    hist.setdefault("rank", {})

    weeks = hist["weeks"]
    # 同一周重复运行：覆盖最后一周，不产生重复数据点
    if weeks and weeks[-1] == week:
        weeks.pop()
        for k in hist["stars"]:
            if hist["stars"][k]:
                hist["stars"][k].pop()
        for board in hist["rank"].values():
            for k in board:
                if board[k]:
                    board[k].pop()
    weeks.append(week)

    live_ids = {it["id"] for it in items}
    for it in items:
        arr = hist["stars"].setdefault(it["id"], [])
        arr.append(it["stars"] if it["github"] else None)
    for k in hist["stars"]:
        if k not in live_ids:
            hist["stars"][k].append(None)

    for board in ("overall", "heat", "practical", "momentum", "open_source"):
        r = hist["rank"].setdefault(board, {})
        if board == "open_source":
            pool = [x for x in items if x["type"] == "open"]
        elif board == "momentum":
            pool = [x for x in board_items(items) if x["github"]]
        else:
            pool = board_items(items)
        order = rank_by(pool, "overall" if board == "open_source" else board)
        for pos, it in enumerate(order, 1):
            r.setdefault(it["id"], []).append(pos)
        for k in r:
            if k not in live_ids:
                r[k].append(None)

    # 只保留最近 max_weeks 周
    if len(weeks) > max_weeks:
        overflow = len(weeks) - max_weeks
        hist["weeks"] = weeks[overflow:]
        for d in (hist["stars"], *[b for b in hist["rank"].values()]):
            for k in d:
                d[k] = d[k][overflow:] if len(d[k]) >= overflow else d[k]

    hist["updated"] = human_time()
    hist["prev_ids"] = [x["id"] for x in (prev_rankings.get("items") or [])]
    hist["prev_overall"] = {x["id"]: x["overall"] for x in (prev_rankings.get("items") or [])}
    hist["prev_stars"] = {x["id"]: x["stars"] for x in (prev_rankings.get("items") or [])}
    return hist


# ---------------------------------------------------------------- README / 周报
def md_link_list(it):
    links = it["links"]
    preferred = [("github", "GitHub"), ("home", "官网"), ("model", "模型"), ("docs", "文档"), ("docs2", "示例"), ("api", "API"), ("paper", "论文"), ("video", "视频模型")]
    parts = []
    for key, label in preferred:
        if links.get(key):
            parts.append(f"[{label}]({links[key]})")
    return " · ".join(parts) or "—"


def md_board_table(items, key, n=10, cat=None, exclude_resource=True, open_only=False,
                   github_only=False, recent_only=False):
    pool = [x for x in items if (cat is None or x["category"] == cat)]
    if exclude_resource:
        pool = [x for x in pool if x["type"] != "resource"]
    if open_only:
        pool = [x for x in pool if x["type"] == "open"]
    if github_only:
        pool = [x for x in pool if x["github"]]
    if recent_only:
        pool = [x for x in pool if x["is_recent"]]
    rows = rank_by(pool, key)[:n]
    out = ["| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |", "|---|---|---|---|---|---|---|"]
    cat_labels = load_json(DATA / "config.json", {})["categories"]
    for i, it in enumerate(rows, 1):
        out.append(
            f"| {i} | **{it['name']}** | {cat_labels[it['category']]['label']} | "
            f"{it['heat']:.1f} | {it['practical']:.1f} | **{it['overall']:.1f}** | {md_link_list(it)} |"
        )
    return "\n".join(out)


def build_readme_block(items, config, stats, week):
    cats = config["categories"]
    boards = config["boards"]
    lines = [
        BEGIN_MARK,
        f"> **榜单数据更新时间：{human_time()}** ｜ 第 {week} 周 ｜ 共收录 **{stats['total']}** 项资源，"
        f"其中开源/开放权重 **{stats['open']}** 项、自动收录待复核 **{stats['auto_pending']}** 项。",
        f"> 本区块由 `scripts/build.py` 自动生成，请勿手动编辑；完整可筛选榜单见 [在线网站]({config['project'].get('site_url', 'https://github.com/')})。",
        "",
        "### 🏆 综合榜 Top 20（热度 45% + 实用性 55%）",
        "",
        md_board_table(items, "overall", 20),
        "",
        "<details><summary>🔥 热度榜 Top 10</summary>",
        "",
        md_board_table(items, "heat", 10),
        "",
        "</details>",
        "",
        "<details><summary>🧰 实用榜 Top 10</summary>",
        "",
        md_board_table(items, "practical", 10),
        "",
        "</details>",
        "",
        "<details><summary>📈 上升榜 Top 10（仅有 GitHub 热度追踪的项目）</summary>",
        "",
        md_board_table(items, "momentum", 10, github_only=True),
        "",
        "</details>",
        "",
        "### 🧩 开源榜 Top 10（仅开放权重 / 开源项目）",
        "",
        md_board_table(items, "overall", 10, open_only=True),
        "",
        "### 🆕 新收录榜 Top 10（自动发现，按收录新鲜度 / 综合分）",
        "",
        md_board_table(items, "recency", 10, recent_only=True),
        "",
        "### 分类速览（各类别综合分 Top 5）",
        "",
    ]
    for cid, meta in cats.items():
        count = sum(1 for x in items if x["category"] == cid)
        if not count:
            continue
        lines += [f"<details><summary>{meta['label']}（{count} 项）</summary>", "", md_board_table(items, "overall", 5, cat=cid, exclude_resource=False), "", "</details>", ""]
    lines += [
        "> **口径说明**：热度分来自 GitHub / Hugging Face 公开 API（无仓库的闭源产品使用人工基线），实用性分来自六维人工打分，"
        "综合分按权重合成；算法与权重全部公开在 [`data/config.json`](data/config.json)。"
        "新资源经关键词护栏自动收录，使用保守默认分并标注「待复核」，详见 [`reports/candidates.md`](reports/candidates.md)。"
        "评分含主观判断，请结合自己的硬件、预算与许可需求判断。",
        END_MARK,
    ]
    return "\n".join(lines)


def update_readme(block):
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8") if path.exists() else f"# AI 视觉生成资源榜\n\n{BEGIN_MARK}\n{END_MARK}\n"
    if BEGIN_MARK not in text or END_MARK not in text:
        text = text.rstrip() + f"\n\n{BEGIN_MARK}\n{END_MARK}\n"
    pattern = re.compile(re.escape(BEGIN_MARK) + r".*?" + re.escape(END_MARK), re.S)
    save_text(path, pattern.sub(lambda _m: block, text, count=1))


def write_weekly_report(items, hist, week, stats, prev_rankings):
    prev_stars = hist.get("prev_stars", {})
    prev_overall = hist.get("prev_overall", {})
    prev_ids = set(hist.get("prev_ids", []))
    rank_now = {x["id"]: i for i, x in enumerate(rank_by(board_items(items), "overall"), 1)}

    changes = []
    for it in items:
        if it["id"] in prev_stars and it["github"] and prev_stars[it["id"]]:
            delta = it["stars"] - prev_stars[it["id"]]
            if delta:
                changes.append((delta, it))
    changes.sort(key=lambda x: -x[0])

    newcomers = [it for it in items if it["id"] not in prev_ids] if prev_ids else []
    failures = [it for it in items if it["link_state"] == "fail"]

    lines = [
        f"# 第 {week} 周 · 榜单更新报告",
        "",
        f"- 生成时间：{human_time()}",
        f"- 收录资源：{stats['total']} 项（开源/开放权重 {stats['open']} 项，闭源平台 {stats['closed']} 项，资源评测 {stats['resource']} 项）",
        f"- 数据来源：GitHub REST API（仓库元数据）+ Hugging Face API（模型 likes / downloads）+ 人工维护清单",
        "- 说明：本项目只读取公开元数据，**不下载任何模型权重、素材或数据集**。",
        "",
        "## 本周 Star 增长 Top 10",
        "",
        "| 资源 | 当前 Stars | 较上次构建 | 热度分 |",
        "|---|---|---|---|",
    ]
    if changes:
        for delta, it in changes[:10]:
            sign = "+" if delta > 0 else ""
            lines.append(f"| [{it['name']}]({it['links'].get('github') or it['links'].get('home')}) | {it['stars']:,} | {sign}{delta:,} | {it['heat']:.1f} |")
    else:
        lines.append("| — | — | 首次构建，暂无可比快照 | — |")

    lines += ["", "## 综合分上升最快 Top 10", "", "| 资源 | 综合分 | 较上次构建 | 当前排名 |", "|---|---|---|---|"]
    score_changes = []
    for it in board_items(items):
        if it["id"] in prev_overall:
            delta = round(it["overall"] - prev_overall[it["id"]], 1)
            if delta:
                score_changes.append((delta, it))
    score_changes.sort(key=lambda x: -x[0])
    if score_changes:
        for delta, it in score_changes[:10]:
            sign = "+" if delta > 0 else ""
            lines.append(f"| {it['name']} | {it['overall']:.1f} | {sign}{delta} | #{rank_now[it['id']]} |")
    else:
        lines.append("| — | — | 首次构建，暂无可比快照 | — |")

    # 自动收录按「本周收录日期」统计，保证同一周内多次刷新时周报仍完整列出本周新资源
    week_start = (now_cn() - timedelta(days=now_cn().weekday())).strftime("%Y-%m-%d")
    auto_new = [it for it in items if it["auto_admitted"]
                and str(it.get("admitted_at", ""))[:10] >= week_start]
    manual_new = [it for it in newcomers if not it["auto_admitted"]]
    lines += ["", "## 本周新增收录", "",
              f"### 🤖 自动发现并收录（{len(auto_new)}）", ""]
    if auto_new:
        for it in auto_new:
            lines.append(f"- **{it['name']}**（{it['org']}，{it['stars']:,} Stars）— {it['desc']} ｜ {md_link_list(it)}")
        lines += ["", "> 以上条目由 `scripts/discover.py` 经护栏自动写入 `data/auto_tools.json`，"
                  "使用保守默认分并标记「待复核」，可在网站「自动收录 / 待复核」筛选中集中复核。"]
    else:
        lines.append("- 本轮无符合护栏的新仓库（或为首次构建）。")
    lines += ["", f"### ✍️ 人工新增（{len(manual_new)}）", ""]
    if manual_new:
        for it in manual_new:
            lines.append(f"- **{it['name']}**（{it['org']}）— {it['desc']} ｜ {md_link_list(it)}")
    else:
        lines.append("- 无。人工新增请在 `data/tools.json` 中补充，并在 CONTRIBUTING.md 记录来源。")

    lines += ["", "## 待复核事项", ""]
    if failures:
        lines.append(f"- ⚠️ 检测到 {len(failures)} 个条目存在失效链接，请运行 `python scripts/check_links.py` 复核：" + "、".join(x["name"] for x in failures))
    else:
        lines.append("- 链接校验无明确失效项（未校验的链接不计入）。")
    lines += [
        "- 闭源产品的热度为人工基线，建议每季度人工复核一次 `heat_baseline`。",
        f"- 自动收录层目前 {stats['auto_pending']} 条待复核，建议每周浏览 `reports/candidates.md`，"
        "把优质条目转正写入 `data/tools.json`，把误收录的从 `data/auto_tools.json` 删除。",
        "- 上升榜在历史快照不足 2 周时以维护活跃度代替增速，属正常现象。",
        "",
        "---",
        "",
        f"[← 返回榜单]({ '../README.md' }) ｜ [在线网站]({ '../docs/index.html' })",
        "",
    ]
    save_text(REPORTS / f"{week}.md", "\n".join(lines))
    # 周报索引
    files = sorted([p.name for p in REPORTS.glob("20*-W*.md")], reverse=True)
    index = ["# 每周更新报告", "", "每周一自动生成，记录 Star 变化、分数变化、新增收录与待复核事项。", ""]
    index += [f"- [{f[:-3]}]({f})" for f in files]
    index += ["", "> 报告由 `scripts/build.py` 生成，请勿手动编辑。", ""]
    save_text(REPORTS / "README.md", "\n".join(index))
    return {"star_changes": len(changes), "new": len(auto_new) + len(manual_new),
            "auto_new": len(auto_new), "failed_links": len(failures)}


# ---------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser(description="构建 AI 视觉生成资源榜")
    ap.add_argument("--no-refresh", action="store_true", help="完全离线，不访问任何网络")
    ap.add_argument("--verbose", action="store_true", help="打印抓取明细")
    args = ap.parse_args()

    config = load_json(DATA / "config.json")
    if not config:
        log("错误：data/config.json 缺失/为空")
        return 1
    tools, auto_count = load_tools(config)
    if not tools:
        log("错误：data/tools.json 缺失/为空")
        return 1
    if len({t["id"] for t in tools}) != len(tools):
        log("错误：合并后的资源清单存在重复 id，请先修复 data/auto_tools.json")
        return 1

    prev_rankings = load_json(DATA / "rankings.json", {}) or {}
    link_status = load_json(DATA / "link_status.json", {}) or {}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    log(f"载入 {len(tools)} 条资源（人工层 {len(tools) - auto_count} + 自动收录 {auto_count}）；"
        f"GitHub {'已认证（内置令牌）' if token else '匿名模式'}")

    metrics = refresh_metrics(tools, token, args)
    save_json(DATA / "metrics_cache.json", metrics)

    history = load_json(DATA / "history.json", {}) or {}
    # 先基于历史算分，再写入本周快照，避免自引用
    items = score_items(tools, config, metrics, history, link_status)
    week = week_key()
    hist = update_history(items, prev_rankings, week)
    save_json(DATA / "history.json", hist)
    # 用最新历史再算一次，让趋势图包含本周
    items = score_items(tools, config, metrics, hist, link_status)

    boards = {key: [x["id"] for x in rank_by(board_items(items), key)]
              for key in ("overall", "heat", "practical")}
    boards["momentum"] = [x["id"] for x in rank_by(
        [i for i in board_items(items) if i["github"]], "momentum")]
    boards["open_source"] = [x["id"] for x in rank_by([i for i in items if i["type"] == "open"], "overall")]
    boards["recent"] = [x["id"] for x in rank_by(
        [i for i in board_items(items) if i["is_recent"]], "recency")]
    week_start = (now_cn() - timedelta(days=now_cn().weekday())).strftime("%Y-%m-%d")
    stats = {
        "total": len(items),
        "open": sum(1 for x in items if x["type"] == "open"),
        "closed": sum(1 for x in items if x["type"] == "closed"),
        "resource": sum(1 for x in items if x["type"] == "resource"),
        "github_tracked": sum(1 for x in items if x["github"]),
        "api_refreshed": sum(1 for x in items if x["data_source"] in ("api", "html")),
        "api_only": sum(1 for x in items if x["data_source"] == "api"),
        "auto_admitted": sum(1 for x in items if x["auto_admitted"]),
        "auto_pending": sum(1 for x in items if x["review_status"] == "pending"),
        "recent_count": len(boards["recent"]),
        "by_category": {cid: sum(1 for x in items if x["category"] == cid) for cid in config["categories"]},
        "new_this_week": len([x for x in items
                              if (x["auto_admitted"] and str(x.get("admitted_at", ""))[:10] >= week_start)
                              or (prev_rankings.get("items") and not x["auto_admitted"]
                                  and x["id"] not in {p["id"] for p in prev_rankings["items"]})]),
        "link_checked_at": link_status.get("checked_at", ""),
    }

    payload = {
        "generated": human_time(),
        "generated_iso": now_cn().isoformat(timespec="seconds"),
        "week": week,
        "project": config["project"],
        "config": config,
        "stats": stats,
        "boards": boards,
        "history": {"weeks": hist["weeks"], "stars": hist["stars"], "rank": hist["rank"]},
        "items": items,
        "disclaimer": config["disclaimer"],
    }
    save_json(DATA / "rankings.json", payload)
    save_json(DOCS / "data.json", payload)
    js = "window.__INDEX_DATA__ = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
    save_text(DOCS / "data.js", js.replace("</", "<\\/"))
    update_readme(build_readme_block(items, config, stats, week))
    report = write_weekly_report(items, hist, week, stats, prev_rankings)

    log(f"完成：{stats['total']} 条资源（自动收录 {stats['auto_admitted']} 条），"
        f"公开数据实取 {stats['api_refreshed']} 条（其中 REST API {stats['api_only']} 条），周报 {week}.md")
    log(f"榜单 Top 3：" + " / ".join(x["name"] for x in rank_by(board_items(items), "overall")[:3]))
    log(f"周报：Star 变化 {report['star_changes']} 项、新增 {report['new']} 项、失效链接 {report['failed_links']} 项")
    return 0


if __name__ == "__main__":
    sys.exit(main())
