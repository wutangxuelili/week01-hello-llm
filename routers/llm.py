from fastapi import APIRouter, HTTPException

from llm_client import LLMClient
from schemas.llm import ChatRequest, ChatResponse

router = APIRouter(prefix="/llm", tags=["LLM"])
llm_client = LLMClient()


@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    接受用户输入的 prompt，调用 LLM 并返回回复。
    """
    try:
        # 构建消息列表
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        # 调用 LLMClient 的 chat 方法
        reply = llm_client.chat(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return ChatResponse(response=reply)

    except Exception as e:  # noqa: BLE001
        # 将底层异常转换为 HTTP 500 错误
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {e}")
