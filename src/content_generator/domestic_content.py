"""国内平台内容生成器 - 淘宝/天猫/抖音"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@dataclass
class DomesticProductInfo:
    name_cn: str
    ingredients_cn: list[str]
    benefits_cn: list[str]
    target_animal: str
    price: float
    original_price: float
    selling_points: list[str]


def generate_taobao_title(product: DomesticProductInfo, keywords: list[str]) -> str:
    """生成淘宝/天猫标题（30字内，含核心搜索词）"""
    prompt = f"""请为以下宠物保健品生成淘宝/天猫搜索标题。

产品：{product.name_cn}
功效：{', '.join(product.benefits_cn)}
目标动物：{product.target_animal}
需要包含的关键词：{', '.join(keywords)}

要求：
1. 严格控制在30个字以内
2. 核心关键词放前面
3. 包含功效词和人群词
4. 符合淘宝搜索算法逻辑
5. 不得有夸大宣传词

直接输出标题，不要解释："""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def generate_douyin_script(product: DomesticProductInfo, duration: str = "60s") -> str:
    """生成抖音带货视频脚本"""
    prompt = f"""你是专业的抖音宠物品类带货文案专家。请为以下产品生成{duration}带货视频脚本。

产品：{product.name_cn}
成分：{', '.join(product.ingredients_cn)}
功效：{', '.join(product.benefits_cn)}
售价：¥{product.price}（原价¥{product.original_price}）
核心卖点：{', '.join(product.selling_points)}

脚本结构（{duration}）：
- 0-3秒：钩子/痛点开场（抓住铲屎官的心）
- 3-15秒：问题共鸣（宠物常见烦恼）
- 15-40秒：产品介绍+成分故事
- 40-55秒：效果展示+用户证言
- 55-60秒：限时价格+行动号召

要求：
1. 口语化，自然真实
2. 情感共鸣，有画面感
3. 价格要在结尾自然引出
4. 符合广告法，不夸大功效

请生成完整脚本（标注时间轴）："""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_detail_page_copy(product: DomesticProductInfo) -> str:
    """生成天猫/淘宝详情页文案"""
    prompt = f"""请为以下宠物保健品生成手机端详情页文案（天猫/淘宝）。

产品：{product.name_cn}
成分：{', '.join(product.ingredients_cn)}
功效：{', '.join(product.benefits_cn)}
卖点：{', '.join(product.selling_points)}

请生成以下模块文案（每模块30字内标题 + 80字内说明）：

1. 首屏焦点图文案（痛点直击）
2. 产品核心卖点（3个，图文对应）
3. 成分解析模块（每个成分一句话）
4. 适用场景（3种场景）
5. 使用方法（3步骤）
6. 品质背书（认证/检测说明）
7. 用户评价引导语

要求：简洁有力，情感化，手机阅读友好，符合国家广告法。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


if __name__ == "__main__":
    product = DomesticProductInfo(
        name_cn="宠爱生活 宠物深海鱼油软胶囊",
        ingredients_cn=["阿拉斯加深海鳕鱼油", "EPA", "DHA", "天然维生素E"],
        benefits_cn=["改善毛发光泽", "关节灵活", "皮肤保湿", "提升免疫力"],
        target_animal="猫咪/狗狗通用",
        price=89.9,
        original_price=158.0,
        selling_points=["无腥味配方", "第三方检测", "30天效果保证"],
    )

    print("=== 淘宝标题 ===")
    title = generate_taobao_title(product, ["宠物鱼油", "猫咪保健品", "狗狗营养"])
    print(title)

    print("\n=== 抖音脚本 ===")
    script = generate_douyin_script(product, "60s")
    print(script)
