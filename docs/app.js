/* AI 视觉生成资源榜 · 前端渲染（原生 JS，零依赖；数据由 data.js 以 script 标签注入，file:// 直接打开也能用） */
(function () {
  'use strict';
  var D = window.__INDEX_DATA__;
  if (!D || !D.items) {
    document.getElementById('grid').innerHTML = '<div class="empty">数据文件尚未生成，请先运行 <code>python scripts/build.py</code>。</div>';
    return;
  }

  var cfg = D.config || {};
  var cats = cfg.categories || {};
  var boards = cfg.boards || {};
  var items = D.items || [];
  var stats = D.stats || {};
  var state = { board: 'overall', cat: 'all', type: 'all', q: '', cnOnly: false };

  var LINK_LABEL = {
    home: '官网', github: 'GitHub', model: '模型卡', docs: '文档', docs2: '示例',
    api: 'API', paper: '论文', video: '视频模型'
  };
  var LINK_ORDER = ['home', 'github', 'model', 'docs', 'docs2', 'api', 'paper', 'video'];
  var TYPE_LABEL = { open: '开源', closed: '闭源', resource: '资源' };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function fmtNum(n) {
    n = Number(n) || 0;
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
    return String(n);
  }
  function scoreRow(label, value, cls) {
    return '<div class="score-row ' + (cls || '') + '"><span>' + label + '</span>' +
      '<div class="bar"><i style="width:' + Math.max(0, Math.min(100, value)) + '%"></i></div>' +
      '<b>' + Number(value).toFixed(1) + '</b></div>';
  }
  function sparkline(arr) {
    var vals = (arr || []).filter(function (v) { return typeof v === 'number' && isFinite(v); });
    if (vals.length < 2) return '<span class="no-trend">趋势累积中</span>';
    var w = 76, h = 22, mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals), span = (mx - mn) || 1;
    var pts = vals.map(function (v, i) {
      return (i / (vals.length - 1) * w).toFixed(1) + ',' + (h - 2 - (v - mn) / span * (h - 5)).toFixed(1);
    }).join(' ');
    return '<svg width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" aria-label="Star 趋势">' +
      '<polyline points="' + pts + '" fill="none" stroke="var(--accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<circle cx="' + w + '" cy="' + (h - 2 - (vals[vals.length - 1] - mn) / span * (h - 5)).toFixed(1) + '" r="2.2" fill="var(--accent)"/></svg>';
  }
  function linkButtons(links) {
    var html = '';
    LINK_ORDER.forEach(function (k) {
      var u = links && links[k];
      if (typeof u === 'string' && u.indexOf('http') === 0) {
        html += '<a class="link-btn" href="' + esc(u) + '" target="_blank" rel="noopener noreferrer">' +
          esc(LINK_LABEL[k] || k) + ' ↗</a>';
      }
    });
    return html || '<span class="no-trend">暂无官方链接</span>';
  }

  // ---------- 顶部统计 ----------
  function renderStats() {
    var s = [
      [stats.total, '收录资源'],
      [stats.open, '开源 / 开放权重'],
      [stats.closed, '闭源平台'],
      [stats.github_tracked, 'GitHub 热度追踪'],
      [stats.api_refreshed, '本次实取仓库'],
      [stats.auto_pending, '自动收录待复核']
    ];
    document.getElementById('stats').innerHTML = s.map(function (x) {
      return '<div class="stat"><b>' + esc(x[0] == null ? '—' : x[0]) + '</b><span>' + esc(x[1]) + '</span></div>';
    }).join('');
    document.getElementById('updated').textContent =
      '榜单数据更新时间：' + D.generated + ' ｜ 第 ' + D.week + ' 周 ｜ 每日 08:30（UTC+8）自动检索收录并刷新' +
      (stats.link_checked_at ? ' ｜ 外链校验：' + stats.link_checked_at : '');
    var repo = (cfg.project && cfg.project.repo) || '';
    if (repo) {
      document.getElementById('repoLink').href = 'https://github.com/' + repo;
    }
    document.getElementById('disclaimer').textContent = D.disclaimer || '';
  }

  // ---------- 榜单 Tab / 分类 chips ----------
  function renderControls() {
    var tabs = Object.keys(boards).map(function (k) {
      return '<button class="tab' + (state.board === k ? ' active' : '') + '" data-board="' + esc(k) + '" type="button">' +
        esc(boards[k].label) + '<small>' + esc(boards[k].desc) + '</small></button>';
    }).join('');
    var tabsEl = document.getElementById('boardTabs');
    tabsEl.innerHTML = tabs;
    tabsEl.querySelectorAll('.tab').forEach(function (btn) {
      btn.addEventListener('click', function () { state.board = btn.dataset.board; renderControls(); render(); });
    });

    var counts = stats.by_category || {};
    var mainCount = items.filter(function (x) { return x.type !== 'resource'; }).length;
    var chips = '<button class="chip' + (state.cat === 'all' ? ' active' : '') + '" data-cat="all" type="button">全部 <em>' + mainCount + '</em></button>';
    chips += Object.keys(cats).map(function (k) {
      return '<button class="chip' + (state.cat === k ? ' active' : '') + '" data-cat="' + esc(k) + '" type="button">' +
        esc(cats[k].label) + ' <em>' + (counts[k] || 0) + '</em></button>';
    }).join('');
    var el = document.getElementById('catChips');
    el.innerHTML = chips;
    el.querySelectorAll('.chip').forEach(function (btn) {
      btn.addEventListener('click', function () { state.cat = btn.dataset.cat; renderControls(); render(); });
    });
  }

  // ---------- 方法说明 ----------
  function renderMethod() {
    var w = (cfg.scoring && cfg.scoring.weights) || {};
    var wh = w.heat || {}, wp = w.practical || {}, wo = w.overall || {};
    var labels = (cfg.scoring && cfg.scoring.practical_labels) || {};
    var pct = function (x) { return Math.round((x || 0) * 100) + '%'; };
    var rows = [
      ['Star 规模', pct(wh.stars), 'GitHub Stars 对数归一（log10 压缩）'],
      ['Star 增速', pct(wh.growth), '与 4 周前历史快照比较；历史不足取中性值'],
      ['维护活跃度', pct(wh.activity), '最近一次 push 距今天数线性衰减'],
      ['社区信号', pct(wh.community), 'Fork 数 + Hugging Face likes / 下载量']
    ].map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>'; }).join('');
    var prows = Object.keys(wp).map(function (k) {
      return '<tr><td>' + esc(labels[k] || k) + '</td><td>' + pct(wp[k]) + '</td><td>人工 1–5 分，锚点见 CONTRIBUTING.md</td></tr>';
    }).join('');
    document.getElementById('methodBody').innerHTML =
      '<p><strong>综合分 = ' + pct(wo.heat) + ' × 热度分 + ' + pct(wo.practical) + ' × 实用性分</strong>。所有分数 0–100，算法与权重公开在 <code>data/config.json</code>，可复算。</p>' +
      '<p><strong>热度分（有 GitHub 仓库的开源项目）</strong></p>' +
      '<table><thead><tr><th>信号</th><th>权重</th><th>口径</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<p><strong>实用性分（全部条目）</strong></p>' +
      '<table><thead><tr><th>维度</th><th>权重</th><th>口径</th></tr></thead><tbody>' + prows + '</tbody></table>' +
      '<p>闭源平台 / 无仓库资源没有 Star 数据，使用人工维护的 <code>heat_baseline</code> 基线，卡片上会标注「人工基线」，不与开源项目混算。</p>' +
      '<p><strong>新资源自动收录</strong></p>' +
      '<p>每日通过 GitHub 公开搜索检索近 120 天新建项目，经 Star 阈值、生图 / 生视频关键词白名单、' +
      '营销与接口封装类黑名单、归档与 Fork 排除、两层清单去重、每轮与总量上限等护栏后，' +
      '自动写入 <code>data/auto_tools.json</code> 并进入榜单。这类条目使用保守默认六维分、' +
      '带「自动收录 · 待复核」标记，可在「新收录榜」或类型筛选「自动收录 / 待复核」中集中复核；' +
      '人工清单 <code>data/tools.json</code> 永远不会被脚本改写。全部护栏参数公开在 <code>data/config.json → auto_admit</code>。</p>';
  }

  // ---------- 卡片 ----------
  function cardHtml(it, rank) {
    var cls = rank <= 3 ? ' rank-' + rank : '';
    var today = (D.generated_iso || '').slice(0, 10);
    var isNew = it.added && it.added === today;
    var badges = '<span class="badge cat">' + esc((cats[it.category] && cats[it.category].label) || it.category) + '</span>' +
      '<span class="badge">' + esc(TYPE_LABEL[it.type] || it.type) + '</span>' +
      (it.type === 'open' || it.type === 'tool' ? '<span class="badge open">开放权重</span>' : '') +
      ((it.scores && it.scores.cn >= 4) ? '<span class="badge">中文友好</span>' : '') +
      (/Apache|MIT/i.test(it.license || '') ? '<span class="badge open">宽松许可</span>' : '') +
      (isNew ? '<span class="badge new">本周新增</span>' : '') +
      (it.auto_admitted ? '<span class="badge auto">自动收录 · 待复核</span>' : '') +
      (it.link_state === 'ok' ? '<span class="badge ok">链接已验证</span>' : '');

    var meta = '<span>★ <strong>' + (it.github ? fmtNum(it.stars) : '—') + '</strong> Stars</span>';
    if (it.growth_pct !== null && it.growth_pct !== undefined) {
      meta += '<span class="growth">4 周 ' + (it.growth_pct > 0 ? '+' : '') + Number(it.growth_pct).toFixed(2) + '%</span>';
    }
    if (it.github) meta += '<span class="spark">' + sparkline(it.spark) + '</span>';
    if (it.days_since_push !== null && it.days_since_push !== undefined) {
      meta += '<span>最近提交 ' + it.days_since_push + ' 天前</span>';
    }

    return '<article class="card' + cls + '">' +
      '<div class="card-head"><div class="rank">' + (rank ? '#' + rank : '参考') + '</div><div class="card-title">' +
      '<h2>' + esc(it.name) + '</h2>' +
      (it.alias ? '<p class="alias">' + esc(it.alias) + (it.org ? ' · ' + esc(it.org) : '') + '</p>' : '') +
      '<div class="badges">' + badges + '</div></div></div>' +
      '<p class="desc">' + esc(it.desc) + '</p>' +
      '<div class="scores">' + scoreRow('热度', it.heat) + scoreRow('实用', it.practical) +
      scoreRow('综合', it.overall, 'overall') + '</div>' +
      '<div class="meta">' + meta + '</div>' +
      '<div class="links">' + linkButtons(it.links) + '</div>' +
      '<div class="source">热度来源：' + esc(it.heat_source) +
      (it.license ? ' ｜ 许可：' + esc(it.license) : '') + ' ｜ ' + (it.tags || []).map(esc).join(' · ') + '</div>' +
      '</article>';
  }

  function render() {
    var boardIds = D.boards && D.boards[state.board] ? D.boards[state.board] : [];
    var rankMap = {};
    boardIds.forEach(function (id, i) { rankMap[id] = i + 1; });
    var q = state.q.trim().toLowerCase();
    // 主榜只排名工具 / 模型 / 平台；资源评测类仅在明确选择该分类或类型时作为参考入口展示
    var showRef = state.cat === 'resource' || state.type === 'resource' || state.type === 'auto';
    var list = items.filter(function (it) {
      if (!showRef && it.type === 'resource') return false;
      if (state.board === 'open_source' && it.type !== 'open') return false;
      if (state.board === 'momentum' && !it.github) return false;
      if (state.board === 'recent' && !it.is_recent) return false;
      if (state.cat !== 'all' && it.category !== state.cat) return false;
      if (state.type === 'auto') { if (!it.auto_admitted) return false; }
      else if (state.type !== 'all' && it.type !== state.type) return false;
      if (state.cnOnly && (!it.scores || it.scores.cn < 4)) return false;
      if (q) {
        var hay = [it.name, it.alias, it.org, it.desc, (it.tags || []).join(' '), it.license].join(' ').toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    });
    var key = state.board === 'open_source' ? 'overall'
      : (state.board === 'recent' ? 'recency' : state.board);
    list.sort(function (a, b) { return (b[key] - a[key]) || (b.overall - a.overall) || a.name.localeCompare(b.name); });

    document.getElementById('grid').innerHTML = list.map(function (it) {
      return cardHtml(it, rankMap[it.id] || 0);
    }).join('');
    document.getElementById('empty').hidden = list.length !== 0;
    document.getElementById('resultLine').textContent =
      '当前显示 ' + list.length + ' / ' + items.length + ' 项资源 ｜ 榜单：' +
      (boards[state.board] ? boards[state.board].label : state.board) +
      ' ｜ 卡片上的 # 名次为该榜单的全库排名，筛选后保持不变；模型社区与评测榜作为「参考」入口，不参与主榜名次。';
  }

  // ---------- 事件 ----------
  document.getElementById('search').addEventListener('input', function (e) { state.q = e.target.value; render(); });
  document.getElementById('typeFilter').addEventListener('change', function (e) { state.type = e.target.value; render(); });
  document.getElementById('cnOnly').addEventListener('change', function (e) { state.cnOnly = e.target.checked; render(); });
  document.getElementById('resetBtn').addEventListener('click', function () {
    state = { board: 'overall', cat: 'all', type: 'all', q: '', cnOnly: false };
    document.getElementById('search').value = '';
    document.getElementById('typeFilter').value = 'all';
    document.getElementById('cnOnly').checked = false;
    renderControls(); render();
  });

  renderStats();
  renderControls();
  renderMethod();
  render();
})();
