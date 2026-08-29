from llm_client import LLMClient

# ai测试脚本
client = LLMClient()

# system_prompt = "你是一个新闻摘要专家。"
# news = "2026年8月28日，DeepSeek 发布了一款全新的 AI 推理模型，性能超越 GPT-4，价格仅为十分之一，引发行业震动。"
# prompt = f"{system_prompt}\n请对以下新闻进行摘要并提取其tags：\n{news}"

# messages = []
# messages.append({"role": "user", "content": prompt})
# reply = client.chat(messages, temperature=0.3)

# print(reply)

# import json
# try:
#     data = json.loads(reply)
#     print(data["title"])
#     print(data["tags"][0])
# except json.JSONDecodeError as e:
#     print(f"JSON 解析失败：{e}")

from jinja2 import Template

# 定义模板（也可以从外部文件读取）
template_str = """
你是一个{{ role }}。
任务：{{ task }}。
请根据以下内容生成回复，并以 JSON 格式输出，包含 title、summary、tags 三个字段。
约束：回复不超过 {{ max_words }} 字，只输出 JSON，不要有其他文字。
"""

# 渲染 prompt
template = Template(template_str)
system_content = template.render(
    role="新闻摘要专家", task="对以下新闻进行摘要并提取 tags", max_words=500
)
news = input("我:")
# 构建 messages
messages = [
    {"role": "system", "content": system_content},
    {"role": "user", "content": "新闻内容：" + news},
]
reply = client.chat(messages, temperature=0.3)

print(reply)
