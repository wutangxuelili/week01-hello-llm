# import json
# from pathlib import Path

# path = Path("user_info.json")
# contents = path.read_text(encoding="utf-8")
# user = json.loads(contents)  # 字符串转字典
# user["database"]["port"] = 5454
# print(f"欢迎回来{user['database']['port']}")

# with open("user_info.json", "r", encoding="utf-8") as f:
#     config = json.load(f)


# config["database"]["port"] = 5434
# with open("user_info.json", "w", encoding="utf-8") as f:
#     json.dump(config, f, ensure_ascii=False, indent=2)
#     # ensure_ascii=False：让中文正常显示，而不是变成 \uXXXX 转义序列
#     # indent=2：美化输出，每个层级缩进2个空格，方便人阅读和手动编辑

# print(config["database"]["port"])
