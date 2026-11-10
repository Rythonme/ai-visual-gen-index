/* 项目进展看板数据文件 —— 任务状态变化时只改这个文件，刷新页面即生效，不用动 kanban.html */
window.__KANBAN_DATA__ = {
  "project": "AI 视觉生成资源榜 · AI Visual Generation Index",
  "subtitle": "生图 / 生视频资源导航与双维度排名榜 · 每周自动更新",
  "updated": "2026-11-10 21:55 (UTC+8)",
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
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "确认目标目录 F:\\00在研项目\\05_Github 可用；git 2.55 已装、Python 3.10 可用；gh CLI 与 PAT 未配置（推送需用户提供令牌）；GitHub API 可达、Hugging Face 本机不通（脚本已做容错）。",
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
      "desc": "build.py 抓公开 API 元数据并重算榜单、生成 README/周报/历史快照；check_links.py 校验外链；discover.py 只提新资源候选不自动收录；两条工作流分别负责周更与 Pages 部署。",
      "deliverables": ["scripts/build.py", "scripts/check_links.py", "scripts/discover.py", ".github/workflows/*.yml"]
    },
    {
      "id": "T5", "title": "开发 GitHub Pages 展示网站与进展看板", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "纯静态零依赖中文网站：四榜切换、搜索、分类/类型/中文筛选、分数条、Star 迷你趋势、官方外链按钮、算法说明；另建本动态看板。",
      "deliverables": ["docs/index.html", "docs/app.js", "docs/style.css", "docs/kanban.html", "docs/kanban_data.js"]
    },
    {
      "id": "T6", "title": "本地运行构建脚本并验证产出", "status": "done", "priority": "高",
      "owner": "WorkBuddy", "updated": "2026-11-10",
      "desc": "构建全链路跑通：90 条资源、五类榜单、173 个外链 0 失效、50/50 GitHub 仓库取得真实 Star/Fork；Python 与前端 JS 语法校验通过；本地 git 已完成 2 次提交。",
      "deliverables": ["data/rankings.json", "docs/data.js", "reports/2026-W46.md", "logs/2026-11-10.md"]
    },
    {
      "id": "T7", "title": "初始化 git 仓库并推送到 GitHub", "status": "todo", "priority": "高",
      "owner": "用户 + WorkBuddy", "updated": "2026-11-10",
      "desc": "用户选择「先在 GitHub 网页新建空仓库」。已核实账号 Rythonme 存在，但目标仓库 ai-visual-gen-index 当前仍为 404；待用户创建并把仓库地址发来后，由 WorkBuddy 执行推送（认证可能需要 PAT 或系统弹窗登录；也可双击 push_to_github.bat 自行推送）。",
      "deliverables": ["远程仓库", "首次 commit / push"]
    },
    {
      "id": "T8", "title": "启用 GitHub Pages 与首次周更验证", "status": "todo", "priority": "中",
      "owner": "用户 + WorkBuddy", "updated": "2026-11-10",
      "desc": "仓库 Settings → Pages 选择 GitHub Actions 源；手动触发一次 weekly-update 工作流，确认内置 GITHUB_TOKEN 下可完整刷新 90+ 仓库指标、榜单自动提交、Pages 自动部署。",
      "deliverables": ["在线网站可访问", "首份自动周报"]
    },
    {
      "id": "T9", "title": "季度复核闭源基线、评分与新资源候选", "status": "todo", "priority": "低",
      "owner": "维护者", "updated": "2026-11-10",
      "desc": "定期复核 heat_baseline、六维评分与 discover.py 产出的候选清单；人工核实后才写入 tools.json，保持榜单不被营销仓库污染。",
      "deliverables": ["reports/candidates.md 审核记录"]
    }
  ],
  "milestones": [
    { "name": "M1 本地仓库完整可用", "status": "done", "date": "2026-11-10", "note": "90 条资源 / 五类榜单 / 周更链路 / 网站 / 看板全部完成并验证" },
    { "name": "M2 GitHub 上线 + Pages 可访问", "status": "todo", "date": "待定", "note": "依赖令牌与 Pages 设置" },
    { "name": "M3 首次自动周更闭环", "status": "todo", "date": "下周一 10:00", "note": "验证 cron 与自动提交" }
  ],
  "links": [
    { "label": "榜单网站", "url": "index.html" },
    { "label": "项目 README", "url": "../README.md" },
    { "label": "榜单 JSON", "url": "../data/rankings.json" },
    { "label": "每周报告", "url": "../reports/README.md" },
    { "label": "新资源候选", "url": "../reports/candidates.md" }
  ]
};
