import os

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

load_dotenv(override=True)  # .env 优先，确保修改 LLM_PROVIDER 后重启即生效
# llm的标准类


class LLMClient:
    def __init__(self):
        # 只改 .env 里的 LLM_PROVIDER 即可切换，支持 deepseek / ollama
        provider = (os.getenv("LLM_PROVIDER") or "deepseek").strip().lower()
        self.provider = provider

        if provider == "deepseek":
            self.base_url = os.getenv("LLM_BASE_URL")
            self.api_key = os.getenv("LLM_API_KEY")
            self.default_model = os.getenv("LLM_DEFAULT_MODEL")
        elif provider == "ollama":
            self.base_url = os.getenv("OLLAMA_BASE_URL")
            self.api_key = (
                "ollama"  # Ollama 本地服务不需要真实 key，但 OpenAI SDK 需要非空字符串
            )
            self.default_model = os.getenv("OLLAMA_MODEL")
        else:
            raise ValueError(
                f"不支持的 LLM_PROVIDER: {provider}，只支持 deepseek / ollama"
            )

        if not self.base_url or not self.default_model:
            raise ValueError(
                f"配置缺失：请检查 .env 中 {provider.upper()}_BASE_URL 和 {provider.upper()}_MODEL"
            )
        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=60.0,  # 设置全局超时 60 秒
        )
        print(
            f"[LLMClient] provider={self.provider}, "
            f"base_url={self.base_url}, model={self.default_model}"
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
        }
        if temperature is not None:
            params["temperature"] = temperature
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

    def chat_stream(
        self, messages, model=None, temperature=0.7, max_tokens=None, stop=None
    ):
        model_to_use = model or self.default_model
        if not model_to_use:
            raise ValueError(
                "No model specified. Set LLM_DEFAULT_MODEL or pass model argument."
            )
        params = {
            "model": model_to_use,
            "messages": messages,
            "stream": True,
        }
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if stop is not None:
            params["stop"] = stop

        # 调用 API，返回一个迭代器（stream）
        stream = self._client.chat.completions.create(**params)

        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content
