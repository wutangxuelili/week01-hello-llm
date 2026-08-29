# from fastapi.testclient import TestClient

# from main import app

# # 1. 创建模拟客户端（在内存中模拟请求，不占用真实端口）
# client = TestClient(app)


# def test_create_user():
#     payload = {"username": "test_01", "password": "123456", "age": 20}

#     response = client.post("/users", json=payload)

#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data


# def test_get_users():
#     response = client.get("/users")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) > 0
#     assert data[-1]["username"] == "test_01"
