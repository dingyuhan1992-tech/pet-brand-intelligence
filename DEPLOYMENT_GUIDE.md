# 云端部署运行指南

目标：本地电脑只做轻量编辑，云端负责运行、定时任务和看板发布。

## 第 1 阶段：先用 GitHub，暂时不买服务器

这个项目目前不需要阿里云、腾讯云或独立服务器。最省心的组合是：

| 功能 | 云端服务 | 为什么适合你 |
| --- | --- | --- |
| 网页看板 | GitHub Pages | 免费，不占电脑内存 |
| 定时任务 | GitHub Actions | 到时间自动运行，不用电脑开机 |
| 报告保存 | GitHub 仓库 `data/` | 暂时不用学数据库 |
| 密钥管理 | GitHub Secrets | 不把 API Key 写进代码 |

## 步骤 1：上传到 GitHub

如果这个项目还没有上传到 GitHub，先在 GitHub 创建一个仓库，然后把本地项目推上去。

如果你不熟悉 Git，可以先停在这里，让我帮你检查当前仓库是否已经连接远程地址。

## 步骤 2：开启 GitHub Pages

在 GitHub 网页操作：

1. 打开你的项目仓库。
2. 点击 `Settings`。
3. 点击左侧 `Pages`。
4. `Source` 选择 `GitHub Actions`。
5. 保存。

之后 `.github/workflows/deploy_dashboard.yml` 会负责发布 `docs/index.html`。

## 步骤 3：添加 GitHub Secrets

在 GitHub 网页操作：

1. 打开项目仓库。
2. 点击 `Settings`。
3. 点击 `Secrets and variables`。
4. 点击 `Actions`。
5. 点击 `New repository secret`。
6. 添加下面这个密钥：

| Name | Value |
| --- | --- |
| `ANTHROPIC_API_KEY` | 你的 Claude API Key |

第一阶段只填这一个即可。Amazon、Shopify、Notion、企业微信可以后面再接。

## 步骤 4：手动测试云端日报

在 GitHub 网页操作：

1. 打开项目仓库。
2. 点击 `Actions`。
3. 点击左侧 `Daily Report`。
4. 点击 `Run workflow`。
5. 等待运行完成。

如果成功，说明云端已经可以代替你的电脑生成日报。

## 步骤 5：手动测试在线看板

在 GitHub 网页操作：

1. 点击 `Actions`。
2. 点击左侧 `Deploy Dashboard`。
3. 点击 `Run workflow`。
4. 运行成功后，回到 `Settings` -> `Pages` 查看网址。

这个网址就是你的云端看板。

## 步骤 6：保留低配置电脑的使用习惯

建议这样用：

| 场景 | 推荐做法 |
| --- | --- |
| 改品牌名、关键词 | 只改 `config/settings.yaml` |
| 看报告 | 打开 GitHub Actions 日志或 Pages 看板 |
| 跑日报 | 用 GitHub Actions 手动触发或等定时 |
| 本地调试 | 只在必要时运行，不长期开服务 |
| 安装依赖 | 暂时不装，优先让云端装 |

## 现在不要急着做的事

这些可以后续再做，不影响第一阶段上线：

- 不急着买云服务器。
- 不急着接 Supabase 数据库。
- 不急着把 Amazon、Shopify、Notion 全部接完。
- 不急着本地安装所有 Python 依赖。

## 后续逐步落地顺序

| 阶段 | 要做什么 | 结果 |
| --- | --- | --- |
| 1 | GitHub Pages + GitHub Actions | 项目能云端运行 |
| 2 | 配好品牌名和关键词 | 报告内容更贴合你的业务 |
| 3 | 接入 Notion 或 GitHub 归档 | 报告可长期查询 |
| 4 | 接入企业微信或邮件 | 自动推送提醒 |
| 5 | 接入 Amazon / Shopify API | 用真实销售数据 |
| 6 | 需要多人使用时再考虑 Supabase 或服务器 | 进入正式系统阶段 |

## 当前项目状态

已具备云端运行基础：

- `docs/index.html`：已有静态看板。
- `.github/workflows/deploy_dashboard.yml`：已有 Pages 发布流程。
- `.github/workflows/daily_report.yml`：已有每日 07:00 自动日报。
- `.github/workflows/keyword_monitor.yml`：已有每日 09:00 关键词监控。
- `.github/workflows/save_reports.yml`：已有报告归档流程。

下一步最适合做的是：确认 GitHub 远程仓库，然后开启 Pages 和 Secrets。
