# 贡献指南 · 如何新增 / 复核一条资源

## 原则

1. **只收录链接**：本项目不下载、不镜像、不转存任何模型权重、数据集、图片或视频。新增条目只填 URL 与文字描述。
2. **官方入口优先**：官网 > 官方 GitHub 仓库 > 官方模型卡（Hugging Face / ModelScope）> 官方文档。不要填转载站、聚合站、网盘、第三方下载页。
3. **不自动收录**：`scripts/discover.py` 只产出候选清单 `reports/candidates.md`，必须由维护者人工核实后才能写入主清单。
4. **许可要说清**：`license` 字段写不下就写「详见仓库」并在 `desc` 里提示商用限制，不要给出笼统的「可商用」结论。

## 新增一条（3 步）

### 第 1 步：编辑 `data/tools.json`

复制一条结构相近的条目，字段说明：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 全局唯一小写英文/数字，如 `wan22`；**不可重复**（build.py 会校验） |
| `name` / `alias` | ✅ / 可选 | 官方名称 / 别名或版本说明 |
| `category` | ✅ | `image_model` 生图模型、`video_model` 生视频模型、`image_platform` 生图平台、`video_platform` 生视频平台、`tool` 工具框架、`edit` 控制增强、`resource` 资源评测 |
| `type` | ✅ | `open`（开放权重/开源）、`closed`（闭源商业）、`resource`（社区/榜单/文档） |
| `org` / `desc` | ✅ | 团队；中文简介 40–80 字，客观描述，不写「最强」「第一」等无法验证的结论 |
| `links` | ✅ | 至少 1 个官方 URL；常用键：`home` 官网、`github` 仓库、`model` 模型卡、`docs` 文档、`docs2` 示例、`api` API、`paper` 论文、`video` 视频模型 |
| `github` | 建议 | `owner/repo` 格式，用于抓取 Star / 更新活跃度；**填了这个字段才会进热度自动更新** |
| `hf_model` | 可选 | Hugging Face 模型 ID，用于抓取 likes / 下载量 |
| `license` | ✅ | SPDX 或简明条款说明 |
| `tags` | ✅ | 2–4 个中文短标签 |
| `added` | ✅ | 收录日期 `YYYY-MM-DD`，周报据此统计新增 |
| `scores` | ✅ | 六维各 1–5 分，见下方锚点 |
| `seed_stars` | 建议 | 首次/离线时的 Star 基线（有 `github` 时填） |
| `heat_baseline` | 建议 | 无 GitHub 仓库时的人工热度基线 0–100 |

### 第 2 步：给六维打分（1–5 分锚点）

| 维度 | 1 分 | 3 分 | 5 分 |
|---|---|---|---|
| `ease` 易上手 | 需自己写训练/推理代码 | 需配置环境与工作流 | 打开网页或一键包即可出图 |
| `cost` 成本/许可友好 | 高价订阅或禁止商用 | 有免费额度 / 有限制许可 | 免费且 Apache-2.0 / MIT 可商用 |
| `quality` 输出质量 | 明显瑕疵、不稳定 | 可用但需挑选 | 公开评测/口碑第一梯队 |
| `cn` 中文支持 | 仅英文、国内难访问 | 部分中文或需代理 | 中文提示词/界面/文档齐全、国内直连 |
| `ecosystem` 生态文档 | 只有论文 | 有 README 与少量示例 | 大量工作流、LoRA、插件、教程与社区 |
| `efficiency` 硬件效率 | 需多卡 / 云端集群 | 24GB 消费卡 | 8–12GB 显卡或纯云端免配置 |

> 评分是**相对导航口径**，不是绝对性能测评。如有公开评测数据，请在 `desc` 或 Issue 中给出处，方便复核。

### 第 3 步：本地验证后提交

```bash
python scripts/build.py           # 重新生成榜单、README、周报
python scripts/check_links.py    # 校验新链接是否可达
git add data/tools.json && git commit -m "feat: add <资源名>"
```

push 后 GitHub Actions 会自动重算榜单并部署网站；也可以在 Actions 页手动触发「每周更新榜单」。

## 复核与修正

- **链接失效**：运行 `python scripts/check_links.py`，`data/link_status.json` 中 `fail` 的链接需要人工确认后更新或下架条目（超时/反爬记为 `unknown`，不算失效）。
- **热度基线**：闭源产品没有 Star 数据，建议每季度复核一次 `heat_baseline`（参考 Artificial Analysis / LMArena 等公开榜单位次与产品热度变化）。
- **评分争议**：欢迎开 Issue 说明具体维度与理由；维护者复核后调整 `scores`，周报会记录分数变化。
- **下架**：产品停服、仓库归档、许可发生重大变更时，可提交 PR 删除条目，并在 PR 描述中说明原因。

## 调整算法

权重、分类名称、榜单口径全部集中在 `data/config.json`。修改后 push 会自动触发工作流重算全站。若改变算法，请在 PR 中说明对 Top 20 的影响，并在 README 的「排名方法」章节同步更新公式。
