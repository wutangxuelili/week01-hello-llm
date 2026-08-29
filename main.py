from datetime import datetime

import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import llm, upload, user

redis_client = redis.Redis(
    host="localhost", port=6379, decode_responses=True, protocol=2
)
app = FastAPI()

# ----- 添加 CORS 中间件 -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # 允许所有来源（开发阶段）
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET, POST, PUT, DELETE...）
    allow_headers=["*"],  # 允许所有请求头
)


# ----- 统一错误格式处理 -----
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),  # noqa: DTZ005
        },
    )


app.include_router(user.router)
app.include_router(upload.router)
app.include_router(llm.router)


@app.get("/")
def read_root():
    return {"Hello": "sb"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/logout")
def logout(token: str):
    # key 的命名规范：blacklist: + 具体 token
    key = f"blacklist:{token}"
    # 存入 Redis，设置过期时间为 60 秒
    # 正确写法（推荐使用 set 替代 setex）
    redis_client.set(key, "blacklisted", ex=60)
    return {"message": "Token 已加入黑名单，将在 60 秒后自动失效"}


@app.get("/protected")
def protected_resource(token: str):
    """
    模拟一个需要登录才能访问的资源
    """
    key = f"blacklist:{token}"

    # 检查这个 token 是否在黑名单中
    if redis_client.exists(key):
        # exists 返回 1 表示存在，0 表示不存在
        return JSONResponse(
            status_code=401, content={"error": "Token 已被拉黑，拒绝访问"}
        )
    return {"message": "Token 有效，欢迎访问受保护资源！"}
