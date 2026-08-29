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

# 用字典dict统计词频
# ceshi = "qwerytusauhduiqwbiqzxcqwdvxcbdvsibqwueih"
# dict1 = {"a": 0, "q": 0}
# for i in ceshi:
#     if i == "a":
#         dict1["a"] += 1
#     elif i == "q":
#         dict1["q"] += 1
# print(dict1.items())

# 封装CSV读取函数
# def duqucsv():
#     with open(input("请输入要读取的CSV文件路径:"), "r") as f:
#         list1 = f.readlines()
#         list2 = [i.strip() for i in list1]
#         print(list2)
# duqucsv()


# from utils import read_csv, read_csv1

# # ----- 读取测试 -----
# header, data = read_csv(
#     "data.csv", encoding="gbk", has_header=False
# )  # 如果你的文件是GBK编码，这里改
# print("表头:", header)
# print("数据行:", data)

# 如果你只要数据行，不要表头，调用时用 has_header=False
# header, data = read_csv('data.csv', has_header=False, encoding='gbk')

# ----- 写入测试-----
# new_data = [["橙子", 4, "水果"], ["葡萄", 6, "水果"]]
# write_csv("output.csv", new_data, header=["名称", "数量", "类别"])
# print("写入完成")
# read_csv1("output.csv")

# from pathlib import Path

# p = Path(".venv")
# for entry in p.iterdir():
#     print(entry.name)

# 批量重命名脚本
# p = Path("ceshi")
# for file in p.glob("*.txt"):
#     new_name = f"new_{file.name}"
#     new_path = file.parent / new_name
#     file.rename(new_path)

# 定义一个Document类(title,content)
# class Document:
#     """
#     :Document:文件
#     :title:标题
#     :content:内容
#     """

#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# ceshi = Document("测试用瞄", "卡拉比丘死了瞄")
# print(ceshi.title)
# print(ceshi.content)

# json文件的读写
# import json
# from pathlib import Path

# path = Path("user_info.json")
# user = {}  # python中dict对应的是json中的对象obj 字典的键一定得是字符串
# user["name"] = input("请输入姓名")
# user["age"] = int(input("年龄:"))

# contents = json.dumps(user)  # contents内容 将user字典转化为json字符串
# path.write_text(contents, encoding="utf-8")
# print(f"信息已存入到{path}中")

# import datetime

# now = datetime.datetime.now()
# print(now)

# import requests

# requests请求  response回应

# url = "https://jsonplaceholder.typicode.com/posts"
# resp = requests.get(url, params={"userId": 1})
# # status 状态 code 代码
# print(resp.status_code)
# print(resp.url)
# data = resp.json()
# print(len(data))

# import requests

# url = "https://httpbin.org/post"
# my_data = {"name": "小D", "task": "学习POST"}
# requ = requests.post(url, json=my_data)
# print(requ.status_code)
# result = requ.json()
# print(result)


# class car:
#     def __init__(self, yanse, siyou):
#         self.yanse = yanse
#         self.__siyou = siyou


# a = car("hongse", "kandedaoma")
# print(a.yanse)
# print(a._car__siyou)

# from pydantic import BaseModel


# class appconfig(BaseModel):
#     app_name: str
#     version: float
#     debug: bool


# raw_data = {"app_name": "MyLLM", "version": "1.0", "debug": True}
# config = appconfig(**raw_data)
# print(config.app_name)

# 用pydantic校验

# import json
# from pathlib import Path

# from pydantic import BaseModel, ValidationError

# try:
#     content_path = Path("user_info.json")
#     with open(content_path, "r", encoding="utf-8") as f:
#         config = json.load(f)
#         print(config)

#     class jiance(BaseModel):
#         name: str
#         age: int
#         debug: bool

#     a = jiance(**config)
#     print(a)
# except ValidationError as e:
#     print("shibai")
#     print(e)

# cli
# import argparse


# def main():
#     parser = argparse.ArgumentParser(description="纯文本行过滤工具（无 CSV）")

#     # 位置参数：输入文件（必填）
#     parser.add_argument("input_file", type=str, help="要读取的文本文件路径")

#     # 可选参数：输出文件（缺省 output.txt）
#     parser.add_argument(
#         "--output",
#         type=str,
#         default="output.txt",
#         help="输出文件路径（默认 output.txt）",
#     )

#     # 可选参数：关键词（缺省为空字符串，表示不过滤）
#     parser.add_argument(
#         "--keyword", type=str, default="", help="只保留包含该关键词的行（默认不过滤）"
#     )

#     # 可选参数：详细模式（布尔开关）
#     parser.add_argument("--verbose", action="store_true", help="打印处理行数")

#     args = parser.parse_args()

#     # ----- 核心逻辑（纯文本读写）-----
#     # 步骤1：读取输入文件的所有行
#     with open(args.input_file, "r", encoding="utf-8") as f:
#         lines = f.readlines()  # 返回 list，每个元素是带换行符的字符串

#     # 步骤2：根据关键词过滤
#     if args.keyword == "":
#         # 不过滤：保留所有行
#         filtered_lines = lines
#     else:
#         # 过滤：只保留包含关键词的行
#         filtered_lines = [line for line in lines if args.keyword in line]

#     # 步骤3：写入输出文件
#     with open(args.output, "w", encoding="utf-8", newline="") as f:
#         f.writelines(filtered_lines)  # 写入列表，每个元素作为一行

#     # 步骤4：打印信息（如果 verbose 开启）
#     if args.verbose:
#         print(f"读取总行数：{len(lines)}")
#         print(f"过滤后行数：{len(filtered_lines)}")
#         print(f"结果已写入：{args.output}")


# if __name__ == "__main__":
#     main()

# 以下是FastAPI的测试
