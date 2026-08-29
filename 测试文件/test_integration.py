# import pytest
# import redis
# from fastapi.testclient import TestClient

# from dependencies import get_db
# from main import app

# # 初始化测试客户端
# client = TestClient(app)

# # 连接 Redis（用于清理黑名单）
# r = redis.Redis(host="localhost", port=6379, decode_responses=True, protocol=2)


# def test_cleanup():
#     """测试前置清理：清空 fake_db 和 Redis 黑名单"""
#     # 1. 清空内存数据库
#     db = get_db()
#     db.clear()

#     # 2. 清空 Redis 中所有 blacklist: 开头的键
#     for key in r.scan_iter("blacklist:*"):
#         r.delete(key)

#     print("✅ 测试环境已清理（fake_db 已清空，Redis 黑名单已清除）")


# def test_full_user_flow():
#     """
#     完整业务流程测试：
#     注册 -> 访问受保护资源 -> 登出 -> 再次访问被拒绝
#     """
#     # ----- 1. 注册用户 -----
#     reg_resp = client.post(
#         "/users", json={"username": "flow_test_user", "password": "123456"}
#     )
#     assert reg_resp.status_code == 200
#     user_data = reg_resp.json()

#     # 注意：根据你的 `/users` 返回格式，这里可能需要调整
#     # 如果你的返回是 {"id": 1, "message": "欢迎..."}，就取 user_data["id"]
#     # 如果你的返回是 {"id": 1}，也一样取 user_data["id"]
#     user_id = user_data.get("id")
#     assert user_id is not None, "注册返回的 JSON 中没有 id 字段"

#     token = str(user_id)  # 用用户 ID 作为 Token（模拟 JWT）

#     # ----- 2. 第一次访问受保护资源（应该成功） -----
#     resp1 = client.get(f"/protected?token={token}")
#     assert resp1.status_code == 200
#     assert resp1.json()["message"] == "Token 有效，欢迎访问受保护资源！"

#     # ----- 3. 登出（加入黑名单） -----
#     resp2 = client.post(f"/logout?token={token}")
#     assert resp2.status_code == 200
#     assert "已加入黑名单" in resp2.json()["message"]

#     # ----- 4. 再次访问受保护资源（应该被拒绝） -----
#     resp3 = client.get(f"/protected?token={token}")
#     assert resp3.status_code == 401
#     assert "已被拉黑" in resp3.json()["error"]
#     print("=== 实际响应 ===")
#     print(f"状态码: {resp3.status_code}")
#     print(f"响应体: {resp3.json()}")
#     print("✅ 完整流程测试通过：注册 -> 访问 -> 登出 -> 被拒")
