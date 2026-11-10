# AI 视觉生成资源榜 · AI Visual Generation Index

> 收罗并展示目前 **AI 生图 / 生视频** 领域的工具、模型与平台资源，按 **热度** 与 **实用性** 制作排名榜，每周自动更新。
>
> **本项目只做整理归纳与展示：不托管、不下载、不分发任何模型权重、数据集或素材，全部资源仅提供官方超链接。**

[![每周更新榜单](https://github.com/Rythonme/ai-visual-gen-index/actions/workflows/weekly-update.yml/badge.svg)](https://github.com/Rythonme/ai-visual-gen-index/actions/workflows/weekly-update.yml)
[![部署榜单网站](https://github.com/Rythonme/ai-visual-gen-index/actions/workflows/pages.yml/badge.svg)](https://github.com/Rythonme/ai-visual-gen-index/actions/workflows/pages.yml)
![收录资源](https://img.shields.io/badge/收录-90%2B%20项-blue)
![许可](https://img.shields.io/badge/license-MIT%20%2F%20CC%20BY%204.0-green)

🌐 **在线榜单网站（GitHub Pages）**：<https://rythonme.github.io/ai-visual-gen-index/>
（首次需在仓库 `Settings → Pages → Build and deployment` 选择 **GitHub Actions**，详见下方「部署」）
📊 **项目进展看板**：[docs/kanban.html](docs/kanban.html) ｜ 🗂 **每周报告**：[reports/README.md](reports/README.md)

---

## 一、这个项目解决什么

AI 生图 / 生视频的工具、模型、平台迭代极快，信息散落在 GitHub、Hugging Face、官网、评测榜和社区里。本项目把散落的入口收拢成一份**可检索、可排序、可复算、每周自动刷新**的中文导航：

- **只给链接**：每个条目都指向官方仓库 / 官网 / 模型卡 / 文档，不下载、不镜像、不转存任何素材；
- **双维度排名**：既看社区热度（GitHub Stars、增速、维护活跃度、HF 下载/点赞），也看实用性（易上手、成本与许可、输出质量、中文支持、生态文档、硬件效率）；
- **五类榜单**：综合榜、热度榜、实用榜、上升榜、开源榜（仅开放权重项目），另有 7 个分类速览；
- **每周自动更新**：GitHub Actions 定时抓取公开 API → 重算分数 → 生成榜单/README/周报/历史快照 → 自动提交 → 自动部署网站。

---

## 二、榜单（自动生成）

<!-- BEGIN AUTO-GENERATED RANKING -->
> **榜单数据更新时间：2026-11-11 00:01 (UTC+8)** ｜ 第 2026-W46 周 ｜ 共收录 **90** 项资源，其中开源/开放权重 **52** 项。
> 本区块由 `scripts/build.py` 自动生成，请勿手动编辑；完整可筛选榜单见 [在线网站](https://rythonme.github.io/ai-visual-gen-index/)。

### 🏆 综合榜 Top 20（热度 45% + 实用性 55%）

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **Google Gemini 图像** | 生图平台 | 97.0 | 90.4 | **93.4** | [官网](https://gemini.google.com/) · [文档](https://ai.google.dev/gemini-api/docs/image-generation) · [API](https://deepmind.google/models/imagen/) |
| 2 | **可灵 Kling** | 生视频平台 | 93.0 | 92.8 | **92.9** | [官网](https://app.klingai.com/cn/) · [文档](https://app.klingai.com/global/quickstart/klingai-video-3-model-user-guide) · [API](https://klingai.com/) |
| 3 | **即梦 Seedance** | 生视频平台 | 92.0 | 92.8 | **92.4** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |
| 4 | **OpenAI GPT Image** | 生图平台 | 98.0 | 86.8 | **91.8** | [官网](https://openai.com/) · [文档](https://platform.openai.com/docs/guides/image-generation) · [API](https://platform.openai.com/docs/api-reference/images) |
| 5 | **ComfyUI** | 工具框架 | 88.4 | 90.4 | **89.5** | [GitHub](https://github.com/Comfy-Org/ComfyUI) · [官网](https://www.comfy.org/) · [文档](https://docs.comfy.org/) · [示例](https://comfyanonymous.github.io/ComfyUI_examples/) |
| 6 | **海螺 Hailuo AI** | 生视频平台 | 89.0 | 89.2 | **89.1** | [官网](https://hailuoai.com/) · [文档](https://platform.minimax.io/docs/guides/video-generation) |
| 7 | **Seedream / 即梦生图** | 生图平台 | 88.0 | 89.2 | **88.7** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |
| 8 | **Midjourney** | 生图平台 | 96.0 | 80.8 | **87.6** | [官网](https://www.midjourney.com/) · [文档](https://docs.midjourney.com/) |
| 9 | **通义万相（视频）** | 生视频平台 | 86.0 | 88.4 | **87.3** | [官网](https://tongyi.aliyun.com/wan/) · [文档](https://help.aliyun.com/zh/model-studio/) |
| 10 | **OpenAI Sora** | 生视频平台 | 95.0 | 80.8 | **87.2** | [官网](https://openai.com/sora/) · [文档](https://platform.openai.com/docs/) |
| 11 | **Google Veo / Flow** | 生视频平台 | 94.0 | 80.8 | **86.7** | [官网](https://deepmind.google/models/veo/) · [文档](https://ai.google.dev/gemini-api/docs/video) · [API](https://labs.google/flow/about) |
| 12 | **通义万相（生图）** | 生图平台 | 84.0 | 88.4 | **86.4** | [官网](https://tongyi.aliyun.com/wan/) · [文档](https://help.aliyun.com/zh/model-studio/) |
| 13 | **MoneyPrinterTurbo** | 工具框架 | 88.7 | 84.0 | **86.1** | [GitHub](https://github.com/harry0703/MoneyPrinterTurbo) · [官网](https://github.com/harry0703/MoneyPrinterTurbo) |
| 14 | **Wan 2.1** | 生视频模型 | 71.7 | 95.6 | **84.8** | [GitHub](https://github.com/Wan-Video/Wan2.1) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) |
| 15 | **Wan 2.2** | 生视频模型 | 76.0 | 91.6 | **84.6** | [GitHub](https://github.com/Wan-Video/Wan2.2) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B) · [文档](https://github.com/Wan-Video/Wan2.2#readme) |
| 16 | **Runway** | 生视频平台 | 92.0 | 78.4 | **84.5** | [官网](https://runwayml.com/) · [文档](https://docs.runwayml.com/) |
| 17 | **Vidu** | 生视频平台 | 84.0 | 84.8 | **84.4** | [官网](https://www.vidu.com/) · [文档](https://www.vidu.studio/) |
| 18 | **ComfyUI-Manager** | 工具框架 | 77.6 | 89.6 | **84.2** | [GitHub](https://github.com/ltdrdata/ComfyUI-Manager) · [官网](https://github.com/ltdrdata/ComfyUI-Manager) |
| 19 | **Adobe Firefly** | 生图平台 | 88.0 | 80.0 | **83.6** | [官网](https://firefly.adobe.com/) · [文档](https://www.adobe.com/products/firefly/features/ai-image-generator.html) |
| 20 | **rembg** | 控制增强 | 79.1 | 87.2 | **83.6** | [GitHub](https://github.com/danielgatis/rembg) · [官网](https://github.com/danielgatis/rembg) |

<details><summary>🔥 热度榜 Top 10</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **OpenAI GPT Image** | 生图平台 | 98.0 | 86.8 | **91.8** | [官网](https://openai.com/) · [文档](https://platform.openai.com/docs/guides/image-generation) · [API](https://platform.openai.com/docs/api-reference/images) |
| 2 | **Google Gemini 图像** | 生图平台 | 97.0 | 90.4 | **93.4** | [官网](https://gemini.google.com/) · [文档](https://ai.google.dev/gemini-api/docs/image-generation) · [API](https://deepmind.google/models/imagen/) |
| 3 | **Midjourney** | 生图平台 | 96.0 | 80.8 | **87.6** | [官网](https://www.midjourney.com/) · [文档](https://docs.midjourney.com/) |
| 4 | **OpenAI Sora** | 生视频平台 | 95.0 | 80.8 | **87.2** | [官网](https://openai.com/sora/) · [文档](https://platform.openai.com/docs/) |
| 5 | **Google Veo / Flow** | 生视频平台 | 94.0 | 80.8 | **86.7** | [官网](https://deepmind.google/models/veo/) · [文档](https://ai.google.dev/gemini-api/docs/video) · [API](https://labs.google/flow/about) |
| 6 | **可灵 Kling** | 生视频平台 | 93.0 | 92.8 | **92.9** | [官网](https://app.klingai.com/cn/) · [文档](https://app.klingai.com/global/quickstart/klingai-video-3-model-user-guide) · [API](https://klingai.com/) |
| 7 | **即梦 Seedance** | 生视频平台 | 92.0 | 92.8 | **92.4** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |
| 8 | **Runway** | 生视频平台 | 92.0 | 78.4 | **84.5** | [官网](https://runwayml.com/) · [文档](https://docs.runwayml.com/) |
| 9 | **海螺 Hailuo AI** | 生视频平台 | 89.0 | 89.2 | **89.1** | [官网](https://hailuoai.com/) · [文档](https://platform.minimax.io/docs/guides/video-generation) |
| 10 | **MoneyPrinterTurbo** | 工具框架 | 88.7 | 84.0 | **86.1** | [GitHub](https://github.com/harry0703/MoneyPrinterTurbo) · [官网](https://github.com/harry0703/MoneyPrinterTurbo) |

</details>

<details><summary>🧰 实用榜 Top 10</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **Wan 2.1** | 生视频模型 | 71.7 | 95.6 | **84.8** | [GitHub](https://github.com/Wan-Video/Wan2.1) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) |
| 2 | **可灵 Kling** | 生视频平台 | 93.0 | 92.8 | **92.9** | [官网](https://app.klingai.com/cn/) · [文档](https://app.klingai.com/global/quickstart/klingai-video-3-model-user-guide) · [API](https://klingai.com/) |
| 3 | **即梦 Seedance** | 生视频平台 | 92.0 | 92.8 | **92.4** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |
| 4 | **Z-Image** | 生图模型 | 68.3 | 92.0 | **81.3** | [GitHub](https://github.com/Tongyi-MAI/Z-Image) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) · [文档](https://github.com/Tongyi-MAI/Z-Image#readme) |
| 5 | **Wan 2.2** | 生视频模型 | 76.0 | 91.6 | **84.6** | [GitHub](https://github.com/Wan-Video/Wan2.2) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B) · [文档](https://github.com/Wan-Video/Wan2.2#readme) |
| 6 | **Google Gemini 图像** | 生图平台 | 97.0 | 90.4 | **93.4** | [官网](https://gemini.google.com/) · [文档](https://ai.google.dev/gemini-api/docs/image-generation) · [API](https://deepmind.google/models/imagen/) |
| 7 | **ComfyUI** | 工具框架 | 88.4 | 90.4 | **89.5** | [GitHub](https://github.com/Comfy-Org/ComfyUI) · [官网](https://www.comfy.org/) · [文档](https://docs.comfy.org/) · [示例](https://comfyanonymous.github.io/ComfyUI_examples/) |
| 8 | **ComfyUI-Manager** | 工具框架 | 77.6 | 89.6 | **84.2** | [GitHub](https://github.com/ltdrdata/ComfyUI-Manager) · [官网](https://github.com/ltdrdata/ComfyUI-Manager) |
| 9 | **海螺 Hailuo AI** | 生视频平台 | 89.0 | 89.2 | **89.1** | [官网](https://hailuoai.com/) · [文档](https://platform.minimax.io/docs/guides/video-generation) |
| 10 | **Seedream / 即梦生图** | 生图平台 | 88.0 | 89.2 | **88.7** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |

</details>

<details><summary>📈 上升榜 Top 10（仅有 GitHub 热度追踪的项目）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **ComfyUI** | 工具框架 | 88.4 | 90.4 | **89.5** | [GitHub](https://github.com/Comfy-Org/ComfyUI) · [官网](https://www.comfy.org/) · [文档](https://docs.comfy.org/) · [示例](https://comfyanonymous.github.io/ComfyUI_examples/) |
| 2 | **MoneyPrinterTurbo** | 工具框架 | 88.7 | 84.0 | **86.1** | [GitHub](https://github.com/harry0703/MoneyPrinterTurbo) · [官网](https://github.com/harry0703/MoneyPrinterTurbo) |
| 3 | **ComfyUI-Manager** | 工具框架 | 77.6 | 89.6 | **84.2** | [GitHub](https://github.com/ltdrdata/ComfyUI-Manager) · [官网](https://github.com/ltdrdata/ComfyUI-Manager) |
| 4 | **rembg** | 控制增强 | 79.1 | 87.2 | **83.6** | [GitHub](https://github.com/danielgatis/rembg) · [官网](https://github.com/danielgatis/rembg) |
| 5 | **Hugging Face Diffusers** | 工具框架 | 81.9 | 83.2 | **82.6** | [GitHub](https://github.com/huggingface/diffusers) · [官网](https://huggingface.co/docs/diffusers/) · [文档](https://huggingface.co/docs/diffusers/index) |
| 6 | **DiffSynth-Studio** | 生视频模型 | 75.8 | 82.4 | **79.4** | [GitHub](https://github.com/modelscope/DiffSynth-Studio) · [官网](https://modelscope.cn/) · [文档](https://github.com/modelscope/DiffSynth-Studio#readme) |
| 7 | **InvokeAI** | 工具框架 | 79.9 | 76.4 | **78.0** | [GitHub](https://github.com/invoke-ai/InvokeAI) · [官网](https://www.invoke.com/) |
| 8 | **LTX-Video** | 生视频模型 | 75.1 | 74.0 | **74.5** | [GitHub](https://github.com/Lightricks/LTX-Video) · [官网](https://ltx.io/) · [模型](https://huggingface.co/Lightricks/LTX-Video) |
| 9 | **SANA** | 生图模型 | 74.0 | 70.4 | **72.0** | [GitHub](https://github.com/NVlabs/Sana) · [官网](https://nvlabs.github.io/Sana/) · [模型](https://huggingface.co/Efficient-Large-Model/SANA1.6B_1024px) |
| 10 | **LTX-2** | 生视频模型 | 75.1 | 67.6 | **71.0** | [GitHub](https://github.com/Lightricks/LTX-2) · [官网](https://ltx.io/) · [模型](https://huggingface.co/Lightricks/LTX-2) |

</details>

### 🧩 开源榜 Top 10（仅开放权重 / 开源项目）

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **ComfyUI** | 工具框架 | 88.4 | 90.4 | **89.5** | [GitHub](https://github.com/Comfy-Org/ComfyUI) · [官网](https://www.comfy.org/) · [文档](https://docs.comfy.org/) · [示例](https://comfyanonymous.github.io/ComfyUI_examples/) |
| 2 | **MoneyPrinterTurbo** | 工具框架 | 88.7 | 84.0 | **86.1** | [GitHub](https://github.com/harry0703/MoneyPrinterTurbo) · [官网](https://github.com/harry0703/MoneyPrinterTurbo) |
| 3 | **Wan 2.1** | 生视频模型 | 71.7 | 95.6 | **84.8** | [GitHub](https://github.com/Wan-Video/Wan2.1) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) |
| 4 | **Wan 2.2** | 生视频模型 | 76.0 | 91.6 | **84.6** | [GitHub](https://github.com/Wan-Video/Wan2.2) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B) · [文档](https://github.com/Wan-Video/Wan2.2#readme) |
| 5 | **ComfyUI-Manager** | 工具框架 | 77.6 | 89.6 | **84.2** | [GitHub](https://github.com/ltdrdata/ComfyUI-Manager) · [官网](https://github.com/ltdrdata/ComfyUI-Manager) |
| 6 | **rembg** | 控制增强 | 79.1 | 87.2 | **83.6** | [GitHub](https://github.com/danielgatis/rembg) · [官网](https://github.com/danielgatis/rembg) |
| 7 | **AUTOMATIC1111 WebUI** | 工具框架 | 82.5 | 82.8 | **82.7** | [GitHub](https://github.com/AUTOMATIC1111/stable-diffusion-webui) · [官网](https://github.com/AUTOMATIC1111/stable-diffusion-webui) |
| 8 | **Hugging Face Diffusers** | 工具框架 | 81.9 | 83.2 | **82.6** | [GitHub](https://github.com/huggingface/diffusers) · [官网](https://huggingface.co/docs/diffusers/) · [文档](https://huggingface.co/docs/diffusers/index) |
| 9 | **Fooocus** | 工具框架 | 74.4 | 87.2 | **81.4** | [GitHub](https://github.com/lllyasviel/Fooocus) · [官网](https://github.com/lllyasviel/Fooocus) |
| 10 | **Z-Image** | 生图模型 | 68.3 | 92.0 | **81.3** | [GitHub](https://github.com/Tongyi-MAI/Z-Image) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) · [文档](https://github.com/Tongyi-MAI/Z-Image#readme) |

### 分类速览（各类别综合分 Top 5）

<details><summary>生图模型（16 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **Z-Image** | 生图模型 | 68.3 | 92.0 | **81.3** | [GitHub](https://github.com/Tongyi-MAI/Z-Image) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) · [文档](https://github.com/Tongyi-MAI/Z-Image#readme) |
| 2 | **Stable Diffusion XL** | 生图模型 | 70.8 | 85.2 | **78.7** | [GitHub](https://github.com/Stability-AI/generative-models) · [官网](https://stability.ai/) · [模型](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) · [文档](https://github.com/Stability-AI/generative-models#readme) |
| 3 | **Qwen-Image** | 生图模型 | 66.4 | 88.0 | **78.3** | [GitHub](https://github.com/QwenLM/Qwen-Image) · [官网](https://qwen.ai/) · [模型](https://huggingface.co/Qwen/Qwen-Image) · [文档](https://qwenlm.github.io/blog/qwen-image/) |
| 4 | **FLUX.1** | 生图模型 | 66.7 | 79.6 | **73.8** | [GitHub](https://github.com/black-forest-labs/flux) · [官网](https://bfl.ai/) · [模型](https://huggingface.co/black-forest-labs/FLUX.1-dev) · [文档](https://github.com/black-forest-labs/flux#readme) |
| 5 | **SANA** | 生图模型 | 74.0 | 70.4 | **72.0** | [GitHub](https://github.com/NVlabs/Sana) · [官网](https://nvlabs.github.io/Sana/) · [模型](https://huggingface.co/Efficient-Large-Model/SANA1.6B_1024px) |

</details>

<details><summary>生视频模型（17 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **Wan 2.1** | 生视频模型 | 71.7 | 95.6 | **84.8** | [GitHub](https://github.com/Wan-Video/Wan2.1) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) |
| 2 | **Wan 2.2** | 生视频模型 | 76.0 | 91.6 | **84.6** | [GitHub](https://github.com/Wan-Video/Wan2.2) · [官网](https://tongyi.aliyun.com/wan/) · [模型](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B) · [文档](https://github.com/Wan-Video/Wan2.2#readme) |
| 3 | **DiffSynth-Studio** | 生视频模型 | 75.8 | 82.4 | **79.4** | [GitHub](https://github.com/modelscope/DiffSynth-Studio) · [官网](https://modelscope.cn/) · [文档](https://github.com/modelscope/DiffSynth-Studio#readme) |
| 4 | **MiniMax H3** | 生视频模型 | 74.6 | 78.4 | **76.7** | [GitHub](https://github.com/MiniMax-AI/MiniMax-H3) · [官网](https://www.minimax.io/) · [模型](https://huggingface.co/MiniMaxAI) · [文档](https://platform.minimax.io/docs/guides/video-generation) |
| 5 | **FramePack** | 生视频模型 | 66.6 | 83.6 | **76.0** | [GitHub](https://github.com/lllyasviel/FramePack) · [官网](https://github.com/lllyasviel/FramePack) · [模型](https://huggingface.co/lllyasviel/FramePackI2V_HY) |

</details>

<details><summary>生图平台（13 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **Google Gemini 图像** | 生图平台 | 97.0 | 90.4 | **93.4** | [官网](https://gemini.google.com/) · [文档](https://ai.google.dev/gemini-api/docs/image-generation) · [API](https://deepmind.google/models/imagen/) |
| 2 | **OpenAI GPT Image** | 生图平台 | 98.0 | 86.8 | **91.8** | [官网](https://openai.com/) · [文档](https://platform.openai.com/docs/guides/image-generation) · [API](https://platform.openai.com/docs/api-reference/images) |
| 3 | **Seedream / 即梦生图** | 生图平台 | 88.0 | 89.2 | **88.7** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |
| 4 | **Midjourney** | 生图平台 | 96.0 | 80.8 | **87.6** | [官网](https://www.midjourney.com/) · [文档](https://docs.midjourney.com/) |
| 5 | **通义万相（生图）** | 生图平台 | 84.0 | 88.4 | **86.4** | [官网](https://tongyi.aliyun.com/wan/) · [文档](https://help.aliyun.com/zh/model-studio/) |

</details>

<details><summary>生视频平台（15 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **可灵 Kling** | 生视频平台 | 93.0 | 92.8 | **92.9** | [官网](https://app.klingai.com/cn/) · [文档](https://app.klingai.com/global/quickstart/klingai-video-3-model-user-guide) · [API](https://klingai.com/) |
| 2 | **即梦 Seedance** | 生视频平台 | 92.0 | 92.8 | **92.4** | [官网](https://jimeng.jianying.com/) · [文档](https://seed.bytedance.com/) |
| 3 | **海螺 Hailuo AI** | 生视频平台 | 89.0 | 89.2 | **89.1** | [官网](https://hailuoai.com/) · [文档](https://platform.minimax.io/docs/guides/video-generation) |
| 4 | **通义万相（视频）** | 生视频平台 | 86.0 | 88.4 | **87.3** | [官网](https://tongyi.aliyun.com/wan/) · [文档](https://help.aliyun.com/zh/model-studio/) |
| 5 | **OpenAI Sora** | 生视频平台 | 95.0 | 80.8 | **87.2** | [官网](https://openai.com/sora/) · [文档](https://platform.openai.com/docs/) |

</details>

<details><summary>工具框架（11 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **ComfyUI** | 工具框架 | 88.4 | 90.4 | **89.5** | [GitHub](https://github.com/Comfy-Org/ComfyUI) · [官网](https://www.comfy.org/) · [文档](https://docs.comfy.org/) · [示例](https://comfyanonymous.github.io/ComfyUI_examples/) |
| 2 | **MoneyPrinterTurbo** | 工具框架 | 88.7 | 84.0 | **86.1** | [GitHub](https://github.com/harry0703/MoneyPrinterTurbo) · [官网](https://github.com/harry0703/MoneyPrinterTurbo) |
| 3 | **ComfyUI-Manager** | 工具框架 | 77.6 | 89.6 | **84.2** | [GitHub](https://github.com/ltdrdata/ComfyUI-Manager) · [官网](https://github.com/ltdrdata/ComfyUI-Manager) |
| 4 | **AUTOMATIC1111 WebUI** | 工具框架 | 82.5 | 82.8 | **82.7** | [GitHub](https://github.com/AUTOMATIC1111/stable-diffusion-webui) · [官网](https://github.com/AUTOMATIC1111/stable-diffusion-webui) |
| 5 | **Hugging Face Diffusers** | 工具框架 | 81.9 | 83.2 | **82.6** | [GitHub](https://github.com/huggingface/diffusers) · [官网](https://huggingface.co/docs/diffusers/) · [文档](https://huggingface.co/docs/diffusers/index) |

</details>

<details><summary>控制增强（8 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **rembg** | 控制增强 | 79.1 | 87.2 | **83.6** | [GitHub](https://github.com/danielgatis/rembg) · [官网](https://github.com/danielgatis/rembg) |
| 2 | **ControlNet** | 控制增强 | 60.5 | 88.0 | **75.6** | [GitHub](https://github.com/lllyasviel/ControlNet) · [官网](https://github.com/lllyasviel/ControlNet) |
| 3 | **Segment Anything** | 控制增强 | 63.4 | 83.2 | **74.3** | [GitHub](https://github.com/facebookresearch/segment-anything) · [官网](https://github.com/facebookresearch/segment-anything) · [模型](https://huggingface.co/facebook/sam-vit-huge) |
| 4 | **GFPGAN** | 控制增强 | 61.9 | 83.6 | **73.8** | [GitHub](https://github.com/TencentARC/GFPGAN) · [官网](https://github.com/TencentARC/GFPGAN) |
| 5 | **Real-ESRGAN** | 控制增强 | 61.4 | 83.6 | **73.6** | [GitHub](https://github.com/xinntao/Real-ESRGAN) · [官网](https://github.com/xinntao/Real-ESRGAN) |

</details>

<details><summary>资源评测（10 项）</summary>

| # | 资源 | 分类 | 热度 | 实用 | 综合 | 官方链接 |
|---|---|---|---|---|---|---|
| 1 | **Hugging Face Models** | 资源评测 | 98.0 | 95.2 | **96.5** | [官网](https://huggingface.co/models?pipeline_tag=text-to-image) · [文档](https://huggingface.co/docs) · [视频模型](https://huggingface.co/models?pipeline_tag=text-to-video) |
| 2 | **Civitai** | 资源评测 | 94.0 | 91.6 | **92.7** | [官网](https://civitai.com/) |
| 3 | **魔搭 ModelScope** | 资源评测 | 88.0 | 92.0 | **90.2** | [官网](https://modelscope.cn/models) · [文档](https://modelscope.cn/docs) |
| 4 | **Artificial Analysis Video Arena** | 资源评测 | 86.0 | 89.2 | **87.8** | [官网](https://artificialanalysis.ai/video/leaderboard/text-to-video) · [文档](https://artificialanalysis.ai/) |
| 5 | **LMArena** | 资源评测 | 85.0 | 89.2 | **87.3** | [官网](https://lmarena.ai/leaderboard) · [文档](https://lmarena.ai/) |

</details>

> **口径说明**：热度分来自 GitHub / Hugging Face 公开 API（无仓库的闭源产品使用人工基线），实用性分来自六维人工打分，综合分按权重合成；算法与权重全部公开在 [`data/config.json`](data/config.json)。评分含主观判断，请结合自己的硬件、预算与许可需求判断。
<!-- END AUTO-GENERATED RANKING -->

> 💡 网页版支持 **搜索、分类筛选、开源/闭源筛选、四种榜单切换、Star 趋势迷你图**；本 README 只展示精简版。
> 模型社区与公开评测榜属于「参考入口」，**不参与主榜名次竞争**（避免把导航资源排到工具模型前面），可在网页的「资源评测」分类单独查看。

---

## 三、排名方法（公开可复算）

### 3.1 热度分 Heat（0–100）

| 信号 | 权重 | 来源与算法 |
|---|---|---|
| Star 规模 | 45% | `log10(stars+1) / log10(150000+1) × 100`，对数压缩避免头部项目一骑绝尘 |
| Star 增速 | 20% | 与上一次周快照 / 4 周前快照比较，`增长% / 5% × 100`（封顶 100）；历史不足时取中性 50 |
| 维护活跃度 | 20% | 按最近一次 push 距今天数线性衰减（7 天≈满分，730 天≈0 分） |
| 社区信号 | 15% | Fork 数量对数分；若配置了 Hugging Face 模型，则并入 likes 与近月下载量 |

- **有 GitHub 仓库**：以上四项加权合成，数据来自 [GitHub REST API](https://docs.github.com/en/rest) 与 [Hugging Face Hub API](https://huggingface.co/docs/hub/api) 的**公开元数据**，只读不下载。API 限流时会回退读取 GitHub 仓库公开页面内嵌的 Star / Fork / 许可证数字（仍只是读一个网页的公开元数据，不 clone、不下载任何素材），并在卡片上标注来源。
- **闭源平台 / 无仓库资源**（Midjourney、可灵、即梦、评测榜等）：GitHub Stars 天然不适用，改用 `data/tools.json` 中人工维护的 `heat_baseline` 基线，网站上会明确标注「人工基线」，不与开源项目混算口径。
- API 抓取失败或匿名限额耗尽时，自动回退到 `data/metrics_cache.json` 缓存或 `seed_stars` 基线值，并标注数据来源，**保证榜单每周都能生成**。

### 3.2 实用性分 Practical（0–100）

六维人工打分（各 1–5 分），权重公开在 [`data/config.json`](data/config.json)：

| 维度 | 权重 | 说明 |
|---|---|---|
| 易上手 | 18% | 从零到出图/出片的操作与配置成本 |
| 成本 / 许可友好 | 18% | 免费额度、Apache/MIT 等可商用条款、订阅价格 |
| 输出质量 | 22% | 画质/一致性/文字渲染/运动稳定性的公开口碑与评测表现 |
| 中文支持 | 12% | 中文提示词、中文界面与文档、国内访问可用性 |
| 生态与文档 | 18% | 工作流模板、LoRA/插件数量、教程与社区活跃度 |
| 硬件效率 | 12% | 显存门槛、推理速度、是否需自建 GPU |

`实用性分 = Σ(维度分 × 权重) / 5 × 100`。评分锚点与复核流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 3.3 综合分与上升榜

- **综合分 = 0.45 × 热度分 + 0.55 × 实用性分**（更偏「能不能真的用起来」）
- **上升榜**：只收录有 GitHub 热度追踪的项目（闭源平台没有公开增速数据，不参与该榜）；有历史快照时用 Star 增速分，历史不足时用维护活跃度代替，周报会注明。
- **开源榜**：只看 `type: open` 的开放权重 / 开源项目，按综合分单独排名，方便按部署可行性选型。

> ⚠️ 评分含主观判断，不构成性能背书或采购建议。请结合自己的显卡、预算、许可合规要求（尤其商用场景）判断。

---

## 四、每周自动更新

| 项 | 说明 |
|---|---|
| 定时 | `.github/workflows/weekly-update.yml`，`cron: 0 2 * * 1`（**每周一 10:00 北京时间**） |
| 手动 | 仓库 `Actions → 每周更新榜单 → Run workflow`；也可 `git push` 修改 `data/tools.json` 或 `scripts/**` 立即触发 |
| 认证 | 使用 Actions 内置 `secrets.GITHUB_TOKEN`（5000 次/小时），**无需配置任何密钥** |
| 更新内容 | Star/Fork/最近提交/许可证/官方简介（GitHub）、likes/下载量（Hugging Face）、五类榜单、README 榜单区块、周报、历史趋势、外链校验状态、新资源候选清单 |
| 自动收录？ | ❌ **不会**。新资源只生成候选清单 `reports/candidates.md`，必须人工核实后手工加入 `data/tools.json`，避免营销仓库污染榜单 |
| 人工边界 | 闭源产品热度基线、实用性六维评分、新增/下架条目 —— 这三类需要人工维护（建议季度复核） |
| 网站部署 | `.github/workflows/pages.yml`，`docs/**` 变更或手动触发即部署 GitHub Pages |

每次运行产出：

```
data/rankings.json      完整榜单数据（可供第三方程序读取）
data/history.json      近 26 周 Star 与排名快照（趋势图/增速来源）
data/metrics_cache.json 公开指标缓存（API 失败时兜底）
data/link_status.json   外链校验结果
data/candidates.json   新资源候选（人工审核用）
docs/data.js           网站数据源（script 标签加载，双击 HTML 也能看）
docs/data.json         网站数据源（JSON 版）
README.md              自动替换「榜单」区块
reports/YYYY-Www.md    本周更新报告
reports/candidates.md  候选清单（人读版）
```

> GitHub 会在仓库连续 60 天无活动后暂停 schedule，手动跑一次 workflow 即可恢复。

---

## 五、本地运行

零第三方依赖，Python 3.9+ 即可：

```bash
git clone https://github.com/Rythonme/ai-visual-gen-index.git
cd ai-visual-gen-index

python scripts/build.py            # 生成榜单（自动尝试刷新公开数据）
python scripts/build.py --no-refresh   # 完全离线，只用缓存/基线
python scripts/check_links.py      # 校验所有外链
python scripts/discover.py          # 生成新资源候选清单

# 直接双击 docs/index.html 即可查看网站（数据由 data.js 提供，无需起服务器）
```

可选：设置 `GITHUB_TOKEN` 环境变量以使用 5000 次/小时的认证额度；不设置则走匿名额度，脚本会自动降级。

### 目录结构

```
├── .github/workflows/    周更 + Pages 部署两条工作流
├── data/
│   ├── tools.json        ★ 唯一需要人工维护的源文件
│   ├── config.json       ★ 评分权重、分类、榜单口径
│   ├── rankings.json     生成的完整榜单
│   ├── history.json      26 周历史快照
│   └── ...
├── scripts/              build.py / check_links.py / discover.py
├── docs/                  GitHub Pages 静态网站 + 项目进展看板
└── reports/              每周报告与候选清单
```

---

## 六、收录标准与贡献

收录范围：AI **图像生成 / 视频生成** 的模型、平台、推理工具、控制增强组件，以及模型社区与公开评测榜。收录至少满足：有可访问的官方入口、与该领域直接相关、能说清许可或使用条件。

欢迎通过 Issue / PR 补充遗漏、修正失效链接、复核评分。新增条目请按 [CONTRIBUTING.md](CONTRIBUTING.md) 的字段说明与评分锚点填写 `data/tools.json`，push 后工作流会自动重算榜单。

---

## 七、部署自己的一份

1. Fork 或 push 本仓库到你的 GitHub 账号；
2. `Settings → Pages → Build and deployment → Source` 选 **GitHub Actions**；
3. `Actions → 每周更新榜单 → Run workflow` 跑一次，生成 `data/rankings.json`、`docs/data.js` 与 README 榜单；
4. 网站地址：`https://<你的用户名>.github.io/<仓库名>/`；
5. 修改 `data/config.json` 里的 `project.owner` 与 `site_url`，以及 README 顶部的徽章/链接。

---

## 八、声明与许可

- 本项目为**资源导航与社区热度观察**，与所列任何产品/团队无隶属或商业关系；商标与产品名称归各自权利人所有。
- **不下载、不托管、不分发**任何模型权重、数据集、图片或视频；所有链接指向第三方官方页面，访问与下载行为由用户自行决定并遵守对方条款。
- 开源项目许可请以各自仓库为准；商用前**务必逐个核对**许可证（尤其 FLUX dev 系列、社区 LoRA、Stability 社区许可等）。
- 代码：MIT（见 [LICENSE](LICENSE)）；清单文字与数据条目：CC BY 4.0（署名即可，见 [LICENSE-DATA](LICENSE-DATA)）。
