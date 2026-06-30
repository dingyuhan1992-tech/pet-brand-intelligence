# 🐾 宠物保健品品牌智能管理系统

跨境电商全平台（Amazon / Shopify / 淘宝 / 天猫 / 抖音）智能化运营大脑。

## 功能模块

| 模块 | 功能 | 状态 |
|------|------|------|
| 每日智能报告 | 全平台数据汇总 + AI分析 | ✅ 已配置 |
| Amazon Listing 生成 | 标题/Bullet/描述/A+ | ✅ 已配置 |
| 国内平台文案 | 淘宝标题/抖音脚本/详情页 | ✅ 已配置 |
| 竞品监控 | 价格/BSR/评论追踪 | ✅ 已配置 |
| 关键词监控 | 排名变化每日推送 | ✅ 已配置 |
| 库存预警 | 低于阈值自动提醒 | 🔧 待接入API |

## 快速开始

1. 复制环境变量文件：`cp .env.example .env`
2. 填写 `.env` 中的 API 密钥
3. 修改 `config/settings.yaml` 中的品牌信息和关键词
4. 在 GitHub Actions 中设置 Secrets
5. 手动触发或等待定时执行

## 自动化任务时间（北京时间）

- 07:00 每日运营报告
- 09:00 关键词排名检查
- 10:00 竞品动态监控

## GitHub Actions Secrets 配置清单

- `ANTHROPIC_API_KEY` - Claude AI 密钥（必填）
- `NOTION_TOKEN` - Notion 集成密钥
- `AMAZON_CLIENT_ID` / `CLIENT_SECRET` / `REFRESH_TOKEN`
- `SHOPIFY_ACCESS_TOKEN` / `SHOPIFY_SHOP_URL`
- `WECHAT_WEBHOOK_URL` - 企业微信通知
