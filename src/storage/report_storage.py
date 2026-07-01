"""报告归档存储 - 自动保存每日报告到 GitHub + Notion"""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def save_report_local(report: str, report_type: str = "daily") -> str:
    """保存报告到本地/GitHub 归档"""
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    save_dir = Path(f"data/reports/{month}")
    save_dir.mkdir(parents=True, exist_ok=True)

    filepath = save_dir / f"{report_type}_{today}.md"

    content = f"""# {report_type.upper()} Report - {today}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{report}
"""
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def save_to_notion(data: dict, database_id: str, title: str) -> bool:
    """保存数据到 Notion 数据库"""
    notion_token = os.environ.get("NOTION_TOKEN")
    if not notion_token or notion_token == "pending":
        print("⚠️  Notion Token 未配置，跳过 Notion 存储")
        return False

    try:
        from notion_client import Client
        notion = Client(auth=notion_token)

        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
                "Status": {"select": {"name": "完成"}},
            },
            children=[{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": str(data)[:2000]}}]
                }
            }]
        )
        return True
    except Exception as e:
        print(f"Notion 存储失败: {e}")
        return False


def load_report(date: str = None, report_type: str = "daily") -> str:
    """读取历史报告"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    month = date[:7]
    filepath = Path(f"data/reports/{month}/{report_type}_{date}.md")
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    return f"未找到 {date} 的报告"


if __name__ == "__main__":
    test_report = "这是一份测试报告，云端存储系统运行正常。"
    path = save_report_local(test_report, "daily")
    print(f"✅ 报告已保存至：{path}")
