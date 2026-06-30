"""竞品监控 - 追踪竞品价格、评分、BSR变化"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def analyze_competitor_data(competitors: list[dict]) -> str:
    """用 Claude 分析竞品数据，给出策略建议"""
    prompt = f"""你是宠物保健品跨境电商竞品分析专家。请分析以下竞品数据并给出策略建议。

竞品数据（{datetime.now().strftime('%Y-%m-%d')}）：
{json.dumps(competitors, ensure_ascii=False, indent=2)}

请提供：
1. 竞品格局总结（市场份额分布）
2. 价格战情报（谁在降价/促销）
3. 评分/口碑变化（有无差评危机）
4. 你的机会点（可以超越的薄弱环节）
5. 紧急预警（需要立即响应的变化）

用中文输出，重点突出，可操作性强。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def analyze_review_sentiment(reviews: list[dict], product_name: str) -> dict:
    """分析评论情感，提取改进点"""
    reviews_text = "\n".join(
        [f"- {'⭐'*r.get('rating',5)} {r.get('text','')}" for r in reviews[:20]]
    )

    prompt = f"""请分析以下 Amazon 评论，找出产品改进方向。

产品：{product_name}
评论样本：
{reviews_text}

请提供：
1. 主要好评点（TOP3）
2. 主要差评点（TOP3）
3. 用户最关心的功能
4. 改进产品的具体建议
5. Listing 优化方向（根据评论反馈）

用中文输出，每点一句话。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "product": product_name,
        "analysis": message.content[0].text,
        "analyzed_at": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    # 示例竞品数据（实际使用时从 Helium10/Keepa API 获取）
    sample_competitors = [
        {"asin": "B001EXAMPLE", "title": "Competitor A Fish Oil", "price": 24.99, "bsr": 1205, "rating": 4.3, "reviews": 2341},
        {"asin": "B002EXAMPLE", "title": "Competitor B Omega", "price": 19.99, "bsr": 890, "rating": 4.1, "reviews": 5678},
    ]
    print(analyze_competitor_data(sample_competitors))
