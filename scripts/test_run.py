"""系统测试脚本 - 无需 API Key，验证环境是否正常"""

import sys
import importlib.util

def check_module(name):
    spec = importlib.util.find_spec(name)
    status = "✅" if spec else "❌"
    print(f"  {status} {name}")
    return spec is not None

print("\n🐾 宠物保健品智能系统 - 环境检测")
print("=" * 40)

modules = ["anthropic", "requests", "dotenv", "schedule", "pandas", "notion_client", "rich", "yaml"]
results = [check_module(m) for m in modules]

print("=" * 40)
if all(results):
    print("✅ 所有依赖安装成功！系统就绪。")
    print("\n下一步：填写 .env 文件中的 API Key")
    print("  cp .env.example .env")
    print("  nano .env  # 填写 ANTHROPIC_API_KEY")
else:
    print("⚠️  部分依赖缺失，请运行：pip install -r requirements.txt")

print()
