"""关键词排名检查占位脚本（接入 Helium10 API 后启用真实数据）"""

import os
import yaml
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def load_config():
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_keywords():
    config = load_config()
    keywords = config["amazon"]["core_keywords"]
    print(f"[{datetime.now()}] 检查 {len(keywords)} 个关键词排名...")
    for kw in keywords:
        print(f"  - {kw}: 待接入 Helium10 API")
    print("关键词检查完成（请配置 HELIUM10_API_KEY 后启用真实数据）")


if __name__ == "__main__":
    check_keywords()
