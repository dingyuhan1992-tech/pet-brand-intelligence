"""数据模型 - 定义各平台数据结构，统一存储格式"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class DailySales:
    date: str
    platform: str        # amazon_us / shopify / tmall / taobao / douyin
    orders: int
    revenue: float
    currency: str        # USD / CNY
    units_sold: int
    refunds: int = 0
    ad_spend: float = 0.0
    acos: float = 0.0

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


@dataclass
class KeywordRanking:
    date: str
    keyword: str
    platform: str
    rank: int
    search_volume: int = 0
    asin: str = ""
    change: int = 0      # 与昨日相比排名变化


@dataclass
class CompetitorSnapshot:
    date: str
    asin: str
    title: str
    price: float
    bsr: int
    rating: float
    review_count: int
    platform: str = "amazon_us"


@dataclass
class InventoryAlert:
    date: str
    sku: str
    product_name: str
    current_stock: int
    days_remaining: int
    platform: str
    alert_level: str     # green / yellow / red


def save_daily_data(records: list, data_type: str) -> str:
    """统一保存各类数据到本地 JSON"""
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    save_dir = Path(f"data/{data_type}/{month}")
    save_dir.mkdir(parents=True, exist_ok=True)

    filepath = save_dir / f"{today}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([asdict(r) if hasattr(r, '__dataclass_fields__') else r
                   for r in records], f, ensure_ascii=False, indent=2)

    return str(filepath)
