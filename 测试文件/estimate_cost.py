import json

from dependencies import count_tokens, redis_client

# 模拟计算1000次对话所花费的token
# 1. 选择要分析的 session_id
SESSION_ID = "u1"
history_key = f"chat:history:{SESSION_ID}"

# 2. 从 Redis 读取全部历史消息（已经是 Python 字典列表）
raw = redis_client.lrange(history_key, 0, -1)
history = [json.loads(msg) for msg in raw]

# 3. 初始化统计变量
input_tokens = []  # 每次请求的输入 Token 数
output_tokens = []  # 每次请求的输出 Token 数

# 4. 遍历历史，模拟 API 请求
messages = []  # 累积消息列表（不含 system，或包含 system，根据你的实际数据）
system_prompt = None

# 先提取 system 消息（如果有）
for msg in history:
    if msg["role"] == "system":
        system_prompt = msg
        break

# 然后遍历 user/assistant 对
i = 0
while i < len(history):
    if history[i]["role"] == "user":
        # 构建当前累积的 messages（包括 system 和之前的对话）
        cur_messages = []
        if system_prompt:
            cur_messages.append(system_prompt)
        # 添加之前已处理过的 user/assistant 对（即从 0 到 i-1）
        cur_messages.extend([msg for msg in history[:i] if msg["role"] != "system"])
        # 添加当前 user 消息
        cur_messages.append(history[i])

        # 计算输入 Token
        input_tokens.append(count_tokens(cur_messages))

        # 查找紧接着的 assistant（可能隔了几个位置，但通常紧接着）
        j = i + 1
        while j < len(history) and history[j]["role"] != "assistant":
            j += 1
        if j < len(history):
            output_tokens.append(count_tokens([history[j]]))
            i = j + 1  # 跳过 assistant
            continue
        else:
            # 没有对应的 assistant（可能是最后一条 user 还没被回复），忽略
            break
    else:
        i += 1

# 5. 计算平均值
avg_input = sum(input_tokens) / len(input_tokens) if input_tokens else 0
avg_output = sum(output_tokens) / len(output_tokens) if output_tokens else 0

# 6. 价格设定（以 DeepSeek-V4 为例，单位：元/1M Token）
price_input = 8.0
price_output = 8.0

# 7. 计算单次成本
cost_per_conversation = (avg_input * price_input / 1_000_000) + (
    avg_output * price_output / 1_000_000
)

# 8. 估算 1000 次
cost_1000 = cost_per_conversation * 1000

print(f"平均输入 Token: {avg_input:.0f}")
print(f"平均输出 Token: {avg_output:.0f}")
print(f"单次对话成本: ¥{cost_per_conversation:.6f}")
print(f"1000 次对话预估成本: ¥{cost_1000:.4f}")
