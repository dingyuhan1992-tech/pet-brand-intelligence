# 宠物保健品品牌智能管理系统

这是一个轻量级运营自动化项目：本地只负责写代码和改配置，真正的定时运行、报告生成、看板发布都交给云端完成，适合低配置电脑使用。

## 当前最省心方案

| 能力 | 使用方案 | 电脑负担 |
| --- | --- | --- |
| 在线看板 | GitHub Pages | 几乎没有 |
| 每日运营报告 | GitHub Actions 定时运行 | 不占本机内存 |
| 关键词监控 | GitHub Actions 定时运行 | 不占本机内存 |
| 报告归档 | 先保存到 GitHub 仓库 `data/` | 不需要数据库 |
| 后续数据库 | Notion 或 Supabase | 按需要再接入 |

## 你平时怎么用

1. 在本地改配置或文案。
2. 推送到 GitHub。
3. GitHub 自动运行任务。
4. 打开 GitHub Pages 查看看板。

本地不需要长期开着开发服务器，也不需要自己维护云服务器。

## 第一次部署

详细步骤见 [云端部署运行指南](DEPLOYMENT_GUIDE.md)。

最少只需要完成三件事：

1. 把项目上传到 GitHub。
2. 在 GitHub 仓库里开启 Pages。
3. 在 GitHub Secrets 里填写 `ANTHROPIC_API_KEY`。

## 云端任务时间

以下时间均为北京时间：

| 任务 | 时间 | 文件 |
| --- | --- | --- |
| 每日运营报告 | 07:00 | `.github/workflows/daily_report.yml` |
| 关键词排名检查 | 09:00 | `.github/workflows/keyword_monitor.yml` |
| 报告归档 | 07:30 | `.github/workflows/save_reports.yml` |

## 本地检查

如果只是确认项目结构，不需要安装依赖。

如果要在本地测试 Python 环境，可以运行：

```bash
python3 scripts/test_run.py
```

如果提示缺少依赖，说明本机还没安装完整 Python 包。低配置电脑建议优先使用云端运行，不急着在本地安装。

## 重要文件

| 文件 | 用途 |
| --- | --- |
| `config/settings.yaml` | 品牌、关键词、预警阈值配置 |
| `.env.example` | 本地密钥模板，不要填写真实密钥后上传 |
| `docs/index.html` | GitHub Pages 在线看板 |
| `scripts/daily_report.py` | 每日报告生成 |
| `src/market_monitor/keyword_check.py` | 关键词监控 |
| `src/storage/report_storage.py` | 报告归档 |

## 密钥清单

第一阶段只需要：

- `ANTHROPIC_API_KEY`：AI 生成日报用，必填

后续接入真实业务数据时再逐步添加：

- `NOTION_TOKEN`
- `AMAZON_CLIENT_ID`
- `AMAZON_CLIENT_SECRET`
- `AMAZON_REFRESH_TOKEN`
- `SHOPIFY_ACCESS_TOKEN`
- `SHOPIFY_SHOP_URL`
- `HELIUM10_API_KEY`
- `WECHAT_WEBHOOK_URL`
