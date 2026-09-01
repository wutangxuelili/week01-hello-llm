import ast
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from dependencies import count_tokens, redis_client
from llm_client import LLMClient
from prompt_loader import load_prompt
from schemas.llm import ChatRequest, ChatResponse

router = APIRouter(prefix="/llm", tags=["LLM"])
llm_client = LLMClient()
MAX_TOKENS = 4000


@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    接受用户输入的 prompt，调用 LLM 并返回回复。
    """
    try:
        # 模板的使用
        default_system_prompt = load_prompt("ceshibanben", llm_client.default_model)
        effective_system_prompt = request.system_prompt or default_system_prompt
        # 构建消息列表
        session_id = request.session_id
        history_key = f"chat:history:{session_id}"

        user_msg = json.dumps(
            {"role": "user", "content": request.prompt}, ensure_ascii=False
        )  # python转为JSON字符串
        redis_client.rpush(history_key, user_msg)

        raw_history = redis_client.lrange(history_key, 0, -1)
        history = [json.loads(msg) for msg in raw_history]

        messages = []
        if effective_system_prompt:
            messages.append({"role": "system", "content": effective_system_prompt})
        messages.extend(history)

        # 上下文截断
        total_tokens = count_tokens(messages)  # 计算当前总token

        while total_tokens > MAX_TOKENS and len(messages) > 1:
            print(len(messages), total_tokens)
            if len(messages) >= 3:
                del messages[1:3]
            else:
                messages.pop(1)
            total_tokens = count_tokens(messages)

        # 调用 LLMClient 的 chat 方法
        reply = llm_client.chat(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        assistant_msg = json.dumps(
            {"role": "assistant", "content": reply}, ensure_ascii=False
        )  # 追加
        redis_client.rpush(history_key, assistant_msg)

        # ----- 清洗回复 -----
        # 1. 尝试去除可能的 Markdown 代码块标记
        cleaned = reply.strip()
        cleaned = cleaned.removeprefix("```json")
        cleaned = cleaned.removeprefix("```")
        cleaned = cleaned.removesuffix("```")
        cleaned = cleaned.strip()

        # 2. 尝试用 ast.literal_eval 解析 Python 字面量（可处理单引号、None等）
        try:
            data = ast.literal_eval(cleaned)
            # 如果解析结果是字典，再将其转为 JSON 字符串
            if isinstance(data, dict):
                cleaned = json.dumps(data, ensure_ascii=False)
        except (SyntaxError, ValueError):
            # 如果解析失败，尝试直接解析为 JSON（可能已经是 JSON 格式）
            try:
                data = json.loads(cleaned)
                cleaned = json.dumps(data, ensure_ascii=False)
            except json.JSONDecodeError:
                # 如果都失败，保留原始回复
                pass
        return ChatResponse(response=cleaned)

    except Exception as e:  # noqa: BLE001
        # 将底层异常转换为 HTTP 500 错误
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")


@router.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):
    """
    流式对话接口，返回 SSE 事件流。
    """
    try:
        # 1. 加载系统 Prompt
        default_system_prompt = load_prompt("ceshibanben", llm_client.default_model)
        effective_system_prompt = request.system_prompt or default_system_prompt

        # 2. 处理历史（同 /chat 逻辑）
        session_id = request.session_id
        history_key = f"chat:history:{session_id}"

        # 追加用户消息到 Redis
        user_msg = json.dumps(
            {"role": "user", "content": request.prompt}, ensure_ascii=False
        )
        redis_client.rpush(history_key, user_msg)

        # 读取全部历史
        raw_history = redis_client.lrange(history_key, 0, -1)
        history = [json.loads(msg) for msg in raw_history]

        # 构建 messages
        messages = []
        if effective_system_prompt:
            messages.append({"role": "system", "content": effective_system_prompt})
        messages.extend(history)

        # 3. 截断逻辑（你已实现，保持不变）
        # ...（你的截断代码）此处没写出来来

        # 4. 定义生成器函数（负责流式输出 + 保存完整回复）
        def event_generator():
            full_reply = ""  # 用于拼接完整回复，以便存储到 Redis
            # 调用流式 API
            for chunk in llm_client.chat_stream(
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                full_reply += chunk
                # 将每个片段包装成 SSE 格式
                yield f"data: {chunk}\n\n"
            # 流结束，发送结束标记（可选）
            yield f"data: [DONE]\n\n"  # noqa: F541

            # 将完整回复追加到 Redis（记忆存储）
            assistant_msg = json.dumps(
                {"role": "assistant", "content": full_reply}, ensure_ascii=False
            )
            redis_client.rpush(history_key, assistant_msg)

        # 5. 返回 StreamingResponse（必须在生成器外面返回，不能在生成器内部 return）
        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"LLM 流式调用失败: {e}")
