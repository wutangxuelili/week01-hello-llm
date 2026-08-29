from llm_client import LLMClient

# 此文件是用于上下文多轮次对话使用
client = LLMClient()

messages = [
    {"role": "system", "content": "你是一个乐观幽默的助手，总是用轻松的语调回答。"}
]

while True:
    content = input("右边:")
    if content in ("exit", "quit"):
        break
    messages.append({"role": "user", "content": content})
    reply = client.chat(messages, temperature=0.7)
    print("AI:", reply)
    messages.append({"role": "assistant", "content": reply})
