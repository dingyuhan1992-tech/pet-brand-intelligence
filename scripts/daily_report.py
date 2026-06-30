"""每日智能报告生成器 - 汇总全平台数据，由 Claude AI 分析并推送"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def get_placeholder_data():
    """占位数据 - 接入真实API后替换"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return {
        "date": yesterday,
        "amazon": {
            "orders": 0,
            "revenue": 0,
            "acos": 0,
            "bsr_changes": [],
            "new_reviews": [],
            "inventory_alerts": [],
        },
        "shopify": {
            "orders": 0,
            "revenue": 0,
            "sessions": 0,
            "conversion_rate": 0,
        },
        "domestic": {
            "taobao_orders": 0,
            "tmall_orders": 0,
            "douyin_orders": 0,
            "total_gmv": 0,
        },
    }


def generate_daily_report(data: dict) -> str:
    """调用 Claude 生成智能分析报告"""
    prompt = f"""你是一位专业的跨境电商运营分析师，专注于宠物保健品赛道。

以下是今日（{data['date']}）全平台运营数据：

【海外平台】
- Amazon: 订单 {data['amazon']['orders']} 单，营业额 ${data['amazon']['revenue']}，广告ACoS {data['amazon']['acos']}%
- Shopify: 订单 {data['shopify']['orders']} 单，营业额 ${data['shopify']['revenue']}，访问量 {data['shopify']['sessions']}，转化率 {data['shopify']['conversion_rate']}%

【国内平台】
- 淘宝: {data['domestic']['taobao_orders']} 单
- 天猫: {data['domestic']['tmall_orders']} 单
- 抖音: {data['domestic']['douyin_orders']} 单
- 国内总GMV: ¥{data['domestic']['total_gmv']}

请生成一份简洁的每日运营报告，包含：
1. 📊 今日业绩总结（100字内）
2. ⚠️ 需要立即处理的问题（如有）
3. 💡 今日运营建议（3条）
4. 🎯 明日重点任务

用中文输出，语气专业简洁。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def send_report(report: str):
    """发送报告（目前打印到控制台，可接入邮件/企业微信）"""
    print("\n" + "=" * 60)
    print(f"🐾 宠物保健品智能日报 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print(report)
    print("=" * 60 + "\n")


def main():
    print("正在生成每日报告...")
    data = get_placeholder_data()
    report = generate_daily_report(data)
    send_report(report)


if __name__ == "__main__":
    main()
