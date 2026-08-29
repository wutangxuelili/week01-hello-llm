from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None  # 可选系统提示
    temperature: float | None = None  # 可选温度，不传则用默认
    max_tokens: int | None = None  # 可选最大输出长度


class ChatResponse(BaseModel):
    response: str
