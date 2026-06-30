"""Amazon Listing 智能生成器 - 标题、Bullet Points、描述、A+文案"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@dataclass
class ProductInfo:
    name: str
    ingredients: list[str]
    benefits: list[str]
    target_animal: str       # dog / cat / all pets
    weight_size: str
    unique_selling_point: str
    competitor_asins: list[str] = None


def generate_amazon_listing(product: ProductInfo, marketplace: str = "us") -> dict:
    """生成完整的 Amazon Listing 内容"""

    lang_map = {"us": "英语（美式）", "uk": "英语（英式）", "de": "德语", "fr": "法语", "jp": "日语"}
    language = lang_map.get(marketplace, "英语（美式）")

    prompt = f"""你是亚马逊宠物保健品类目的资深运营专家。请为以下产品生成完整的 Amazon Listing。

产品信息：
- 产品名称：{product.name}
- 目标动物：{product.target_animal}
- 核心成分：{', '.join(product.ingredients)}
- 主要功效：{', '.join(product.benefits)}
- 规格/重量：{product.weight_size}
- 核心卖点：{product.unique_selling_point}
- 输出语言：{language}

请生成以下内容（严格遵守亚马逊规则，不得有医疗声明）：

【标题】（200字符内，包含核心关键词，格式：品牌+核心词+规格+功效）

【Bullet Point 1 - 核心功效】（以大写开头，150字符内）

【Bullet Point 2 - 成分特色】（以大写开头，150字符内）

【Bullet Point 3 - 适用对象】（以大写开头，150字符内）

【Bullet Point 4 - 品质保证】（以大写开头，150字符内）

【Bullet Point 5 - 使用方法】（以大写开头，150字符内）

【产品描述】（2000字符内，SEO友好，自然融入关键词）

【Search Terms 建议】（250字节内，后台关键词，空格分隔）

输出时请用【】标注每个部分，内容之间空一行。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "marketplace": marketplace,
        "product_name": product.name,
        "content": message.content[0].text,
    }


def optimize_existing_title(current_title: str, keywords: list[str]) -> str:
    """优化现有 Amazon 标题"""
    prompt = f"""你是亚马逊 SEO 专家。请优化以下宠物保健品标题：

当前标题：{current_title}
需要融入的关键词：{', '.join(keywords)}

要求：
1. 200字符以内
2. 核心关键词放在前80字符
3. 包含规格/数量信息
4. 自然流畅，不堆砌关键词
5. 符合亚马逊标题规范

请直接输出优化后的标题（不需要解释）："""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


if __name__ == "__main__":
    product = ProductInfo(
        name="PetVita Omega-3 Fish Oil",
        ingredients=["Wild Alaskan Salmon Oil", "Vitamin E", "EPA", "DHA"],
        benefits=["关节健康", "毛发光泽", "皮肤保湿", "免疫增强"],
        target_animal="dog",
        weight_size="16 oz / 180 softgels",
        unique_selling_point="Wild-caught Alaska salmon, third-party tested, no fishy smell",
    )

    result = generate_amazon_listing(product, "us")
    print(result["content"])
