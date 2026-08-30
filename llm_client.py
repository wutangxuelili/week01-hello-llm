import os

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

load_dotenv()
# llm的标准类


class LLMClient:
    def __init__(self):
        self.base_url = os.getenv("LLM_BASE_URL")
        self.api_key = os.getenv("LLM_API_KEY")
        self.default_model = os.getenv("LLM_DEFAULT_MODEL")

        if not self.api_key:
            raise ValueError("LLM_API_KEY is not set in environment variables.")

        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=60.0,  # 设置全局超时 60 秒
        )

    def chat(self, messages, model=None, temperature=0.7, max_tokens=None, stop=None):
        model_to_use = model or self.default_model
        if not model_to_use:
            raise ValueError(
                "No model specified. Set LLM_DEFAULT_MODEL or pass model argument."
            )

        # 构建参数
        params = {
            "model": model_to_use,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if stop is not None:
            params["stop"] = stop

        # 定义内部函数，用于重试
        @retry(
            stop=stop_after_attempt(3),  # 总共尝试 3 次（首次 + 2 次重试）
            wait=wait_exponential(
                multiplier=1, min=1, max=10
            ),  # 等待 1s, 2s, 4s (但不超过 10s)
            retry=retry_if_exception_type(
                (RateLimitError, APIConnectionError, APIStatusError)
            ),
            # 只对以上三种异常重试
            before_sleep=lambda retry_state: print(
                f"[重试] 第 {retry_state.attempt_number} 次失败，"
                f"异常: {retry_state.outcome.exception().__class__.__name__}，"
                f"等待 {retry_state.next_action.sleep} 秒后重试..."
            ),
        )
        def _call():
            return self._client.chat.completions.create(**params)

        completion = _call()
        return completion.choices[0].message.content
