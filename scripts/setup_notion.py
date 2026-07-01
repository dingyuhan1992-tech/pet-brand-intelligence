"""一键创建 Notion 数据看板 - 全平台数据库结构"""

import os
import json
from notion_client import Client

NOTION_TOKEN = "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"
notion = Client(auth=NOTION_TOKEN)


def get_or_create_page(title: str) -> str:
    """在根目录创建页面"""
    results = notion.search(query=title, filter={"property": "object", "value": "page"})
    for r in results["results"]:
        if r.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text") == title:
            return r["id"]

    page = notion.pages.create(
        parent={"type": "workspace", "workspace": True},
        properties={"title": {"title": [{"text": {"content": title}}]}},
        icon={"type": "emoji", "emoji": "🐾"},
    )
    return page["id"]


def create_database(parent_id: str, title: str, emoji: str, properties: dict) -> str:
    db = notion.databases.create(
        parent={"type": "page_id", "page_id": parent_id},
        title=[{"type": "text", "text": {"content": title}}],
        icon={"type": "emoji", "emoji": emoji},
        properties=properties,
    )
    return db["id"]


def setup_all():
    print("🐾 正在创建宠物保健品智能看板...")

    # 创建主页面
    print("  创建主页面...")
    parent_id = get_or_create_page("🐾 宠物保健品智能大脑")

    db_ids = {}

    # 1. 每日销售看板
    print("  📊 创建销售数据库...")
    db_ids["sales"] = create_database(parent_id, "📊 每日销售看板", "📊", {
        "日期":        {"date": {}},
        "平台":        {"select": {"options": [
                            {"name": "Amazon US", "color": "orange"},
                            {"name": "Amazon UK", "color": "yellow"},
                            {"name": "Shopify",   "color": "green"},
                            {"name": "天猫",       "color": "red"},
                            {"name": "淘宝",       "color": "pink"},
                            {"name": "抖音",       "color": "purple"},
                        ]}},
        "订单数":      {"number": {"format": "number"}},
        "销售额":      {"number": {"format": "dollar"}},
        "广告花费":    {"number": {"format": "dollar"}},
        "ACoS%":      {"number": {"format": "percent"}},
        "退款数":      {"number": {"format": "number"}},
        "备注":        {"rich_text": {}},
        "Name":        {"title": {}},
    })

    # 2. 关键词排名
    print("  🔍 创建关键词数据库...")
    db_ids["keywords"] = create_database(parent_id, "🔍 关键词排名追踪", "🔍", {
        "关键词":      {"title": {}},
        "日期":        {"date": {}},
        "平台":        {"select": {"options": [
                            {"name": "Amazon US", "color": "orange"},
                            {"name": "淘宝",       "color": "red"},
                            {"name": "抖音",       "color": "purple"},
                        ]}},
        "当前排名":    {"number": {"format": "number"}},
        "排名变化":    {"number": {"format": "number"}},
        "搜索量":      {"number": {"format": "number"}},
        "状态":        {"select": {"options": [
                            {"name": "上升 ↑", "color": "green"},
                            {"name": "稳定 →", "color": "yellow"},
                            {"name": "下降 ↓", "color": "red"},
                        ]}},
    })

    # 3. 竞品监控
    print("  🕵️ 创建竞品数据库...")
    db_ids["competitors"] = create_database(parent_id, "🕵️ 竞品监控", "🕵️", {
        "竞品名称":    {"title": {}},
        "日期":        {"date": {}},
        "ASIN":        {"rich_text": {}},
        "价格":        {"number": {"format": "dollar"}},
        "BSR排名":     {"number": {"format": "number"}},
        "评分":        {"number": {"format": "number"}},
        "评价数":      {"number": {"format": "number"}},
        "威胁等级":    {"select": {"options": [
                            {"name": "高",  "color": "red"},
                            {"name": "中",  "color": "yellow"},
                            {"name": "低",  "color": "green"},
                        ]}},
    })

    # 4. 库存预警
    print("  📦 创建库存数据库...")
    db_ids["inventory"] = create_database(parent_id, "📦 库存预警", "📦", {
        "产品名称":    {"title": {}},
        "SKU":         {"rich_text": {}},
        "平台":        {"select": {"options": [
                            {"name": "Amazon FBA", "color": "orange"},
                            {"name": "Shopify",    "color": "green"},
                            {"name": "国内仓",     "color": "blue"},
                        ]}},
        "当前库存":    {"number": {"format": "number"}},
        "预计售完天数": {"number": {"format": "number"}},
        "预警状态":    {"select": {"options": [
                            {"name": "🟢 充足",   "color": "green"},
                            {"name": "🟡 注意",   "color": "yellow"},
                            {"name": "🔴 紧急",   "color": "red"},
                        ]}},
        "更新日期":    {"date": {}},
    })

    # 5. 每日报告
    print("  📝 创建报告数据库...")
    db_ids["reports"] = create_database(parent_id, "📝 每日智能报告", "📝", {
        "报告标题":    {"title": {}},
        "日期":        {"date": {}},
        "类型":        {"select": {"options": [
                            {"name": "每日报告",   "color": "blue"},
                            {"name": "关键词报告", "color": "green"},
                            {"name": "竞品报告",   "color": "orange"},
                            {"name": "库存报告",   "color": "red"},
                        ]}},
        "内容":        {"rich_text": {}},
        "状态":        {"select": {"options": [
                            {"name": "✅ 完成", "color": "green"},
                            {"name": "⚠️ 异常", "color": "red"},
                        ]}},
    })

    # 保存数据库 ID 到配置文件
    with open("config/notion_databases.json", "w", encoding="utf-8") as f:
        json.dump(db_ids, f, ensure_ascii=False, indent=2)

    print("\n✅ Notion 看板创建完成！")
    print(f"\n数据库 ID 已保存至 config/notion_databases.json")
    print("\n各数据库：")
    for name, db_id in db_ids.items():
        print(f"  {name}: {db_id}")

    return db_ids


if __name__ == "__main__":
    setup_all()
