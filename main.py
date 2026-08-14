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
