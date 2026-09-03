import os

# 1. 创建 LLM 客户端（使用你现有的环境变量）
# 注意：这里直接使用你的 LLMClient 中的配置，或者直接读取 .env
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# 从环境变量读取配置（与你的 LLMClient 保持一致）
base_url = os.getenv("LLM_BASE_URL") or os.getenv("OLLAMA_BASE_URL")
api_key = os.getenv("LLM_API_KEY") or "ollama"
model_name = os.getenv("LLM_DEFAULT_MODEL") or os.getenv("OLLAMA_MODEL") or "qwen2.5:7b"

# 2. 创建 ChatOpenAI 实例（兼容 DeepSeek / Ollama）
llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model_name,
    temperature=0.7,
)

# 3. 定义 Prompt 模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位知识渊博的科普专家，擅长用一句话解释复杂概念。"),
        ("human", "请用一句话解释什么是 {topic}。"),
    ]
)

# 4. 创建输出解析器（将 LLM 的 AIMessage 转为纯字符串）
parser = StrOutputParser()

# 5. 用管道符 `|` 组装链条
chain = prompt | llm | parser

# 6. 执行链条
result = chain.invoke({"topic": "大语言模型"})
print(result)
