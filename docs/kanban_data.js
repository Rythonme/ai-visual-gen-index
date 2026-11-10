/* 项目进展看板数据文件 —— 任务状态变化时只改这个文件，刷新页面即生效，不用动 kanban.html */
window.__KANBAN_DATA__ = {
  "project": "AI 视觉生成资源榜 · AI Visual Generation Index",
  "subtitle": "生图 / 生视频资源导航与双维度排名榜 · 每周自动更新",
  "updated": "2026-11-11 01:05 (UTC+8)",
  "repo": "https://github.com/Rythonme/ai-visual-gen-index",
  "site": "https://rythonme.github.io/ai-visual-gen-index/",
  "workspace": "F:\\00在研项目\\05_Github\\ai-visual-gen-index",
  "principle": "只做整理归纳与展示，不下载任何模型权重/素材，全部资源仅提供官方超链接；原始数据只读。",
  "columns": [
    { "id": "todo", "label": "待办", "color": "#8a92ab" },
    { "id": "doing", "label": "进行中", "color": "#4f46e5" },
    { "id": "done", "label": "已完成", "color": "#0d9488" }
  ],
  "tasks": [
    {
      "id": "T1", "title": "探测本机环境与 GitHub 凭据", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-11",
      "desc": "确认目标目录 F:\\00在研项目\\05_Github 可用；git 2.55、Python 3.10 可用；Git 凭据管理器已缓存 Rythonme 账号（推送与 API 均已验证可用，无需 PAT）；GitHub API 可达，Hugging Face 本机不通（脚本已做容错）。",
      "deliverables": ["环境探测结论"]
    },
    {
      "id": "T2", "title": "核实 2026 年 AI 生图 / 生视频资源清单", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "联网核实主流开源模型（FLUX.2 / Qwen-Image / Z-Image / Wan2.2 / HunyuanVideo / LTX-2 等）、闭源平台、工具框架与公开评测榜的官方入口，避免链接与描述过时。",
      "deliverables": ["资源核实结果已落入 data/tools.json"]
    },
    {
      "id": "T3", "title": "设计数据模型与排名算法并录入资源", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "建立 7 大分类、90+ 条资源的结构化清单；设计公开可复算的热度分（Star/增速/活跃度/社区）、实用性六维评分与综合分，权重集中在 config.json。",
      "deliverables": ["data/tools.json", "data/config.json", "CONTRIBUTING.md 评分锚点"]
    },
    {
      "id": "T4", "title": "编写每周自动更新脚本与 GitHub Actions", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "build.py 合并人工层与自动收录层后抓公开 API 元数据、重算六类榜单并生成 README/周报/历史快照；discover.py 每日自动检索并按护栏收录新资源；check_links.py 校验外链；两条工作流分别负责每日更新与 Pages 部署。",
      "deliverables": ["scripts/build.py", "scripts/check_links.py", "scripts/discover.py", ".github/workflows/*.yml"]
    },
    {
      "id": "T5", "title": "开发 GitHub Pages 展示网站与进展看板", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "纯静态零依赖中文网站：六榜切换（含新收录榜）、搜索、分类/类型/自动收录筛选、分数条、Star 迷你趋势、官方外链按钮、算法与自动收录机制说明；另建本动态看板。",
      "deliverables": ["docs/index.html", "docs/app.js", "docs/style.css", "docs/kanban.html", "docs/kanban_data.js"]
    },
    {
      "id": "T6", "title": "本地运行构建脚本并验证产出", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "构建全链路跑通：90 条资源、五类榜单、173 个外链 0 失效、50/50 GitHub 仓库取得真实 Star/Fork；Python 与前端 JS 语法校验通过；本地 git 完成 3 次提交。",
      "deliverables": ["data/rankings.json", "docs/data.js", "reports/2026-W46.md", "logs/2026-11-10.md"]
    },
    {
      "id": "T7", "title": "初始化 git 仓库并推送到 GitHub", "status": "done", "priority": "高",
      "owner": "用户 + WorkBuddy", "updated": "2026-11-11",
      "desc": "用户创建空仓库后完成推送：保留远端 Initial commit 做 unrelated-histories 合并（未强推）、本地分支统一为 main、忽略目录内用户自行 clone 的副本（保留未删）。远端 HEAD 与本地一致，28 个文件全部上线。",
      "deliverables": ["https://github.com/Rythonme/ai-visual-gen-index", "首次 commit / push"]
    },
    {
      "id": "T8", "title": "启用 GitHub Pages 与首次周更验证", "status": "done", "priority": "中",
      "owner": "用户 + WorkBuddy", "updated": "2026-11-11",
      "desc": "Pages 已启用（build_type=workflow），站点返回 200 且标题/静态资源正常；首次 push 自动触发的两条工作流均 success，并两轮自动提交（9f470eb、4647b25）更新榜单/周报/候选清单；云端复验外链 161 ok / 0 fail。更新频率已升级为每日 08:30。",
      "deliverables": ["在线网站可访问", "首份自动周报", "data/candidates.json", "reports/candidates.md"]
    },
    {
      "id": "T9", "title": "复核自动收录条目并转正 / 下架", "status": "todo", "priority": "中",
      "owner": "维护者", "updated": "2026-11-11",
      "desc": "已有 12 条自动收录进榜（Qwen-Image-2.1、MAGI-2-preview、SparkDiffusion、open-higgsfield、TaoMate、StreamEval 等），均带 pending 标记与保守默认分。需逐个核实范畴/官方链接/许可证，优质条目转正写入 tools.json 并给正式六维分，误收的从 auto_tools.json 删除。另季度复核 heat_baseline 与护栏关键词。",
      "deliverables": ["reports/candidates.md 审核记录", "data/auto_tools.json 复核"]
    },
    {
      "id": "T10", "title": "外链质量复核（Adobe 反爬误报）", "status": "done", "priority": "低",
      "owner": "WorkBuddy", "updated": "2026-11-11",
      "desc": "云端首轮校验 161 ok / 1 fail / 11 unknown，唯一 fail 为 Adobe 官网对爬虫返回 404/403 的误报。已把 4 条 Adobe 链接改用 firefly.adobe.com 官方直达入口（均 200），并让 check_links.py 对 HEAD 404 回退 GET 复核；第二轮云端周更复验结果为 161 ok / 0 fail / 11 unknown。",
      "deliverables": ["data/tools.json", "scripts/check_links.py"]
    },
    {
      "id": "T11", "title": "新资源自动收录 + 每日实时刷新", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-11",
      "desc": "按用户要求把「只出候选、绝不自动收录」改为自动进榜：人工层 tools.json 只读 + 自动层 auto_tools.json 增量写入，build.py 合并两层；护栏含 Star 阈值、生图生视频白名单、NSFW / 营销 / 接口封装 / 教程 / Claude Code 工具箱黑名单、简介长度、归档与 Fork 排除、去重、每轮 8 条与总量 60 条上限、官方机构优先的相关性排序；新增「新收录榜」与「自动收录 / 待复核」筛选；cron 由每周改为每日 08:30。本地实测命中 32 个、自动收录 8 个、护栏拒绝 20 个；推送后云端工作流自动再收录顺延的 4 个（命中 32 / 新增 4 / 已在榜 8），自动层达 12 条、榜单由 90 增至 102 条，62/62 仓库经 API 实取，线上站点已含新条目。",
      "deliverables": ["data/auto_tools.json", "data/config.json → auto_admit", "scripts/discover.py", "scripts/build.py", ".github/workflows/weekly-update.yml", "reports/candidates.md"]
    }
  ],
  "milestones": [
    { "name": "M1 本地仓库完整可用", "status": "done", "date": "2026-11-10", "note": "90 条资源 / 五类榜单 / 周更链路 / 网站 / 看板全部完成并验证" },
    { "name": "M2 GitHub 上线 + Pages 可访问", "status": "done", "date": "2026-11-11", "note": "仓库已推送、Pages 已启用且站点 200 可访问" },
    { "name": "M3 首次自动更新闭环", "status": "done", "date": "2026-11-11", "note": "两条工作流 success，自动提交榜单/周报；58/58 仓库经 API 实取" },
    { "name": "M4 新资源自动收录上线", "status": "done", "date": "2026-11-11", "note": "每日 08:30 检索收录；两轮共 12 条自动进榜、榜单 102 条，六类榜单含新收录榜；护栏实测拦截 20 个误收候选；云端自动收录工作流 success 并自动提交 dd4fa4e" }
  ],
  "links": [
    { "label": "GitHub 仓库", "url": "https://github.com/Rythonme/ai-visual-gen-index" },
    { "label": "在线榜单网站", "url": "https://rythonme.github.io/ai-visual-gen-index/" },
    { "label": "榜单网站（本地）", "url": "index.html" },
    { "label": "项目 README", "url": "../README.md" },
    { "label": "榜单 JSON", "url": "../data/rankings.json" },
    { "label": "每周报告", "url": "../reports/README.md" },
    { "label": "新资源候选", "url": "../reports/candidates.md" }
  ]
};
