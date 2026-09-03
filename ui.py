import json

import requests
import streamlit as st

# 配置页面标题和图标
st.set_page_config(page_title="简易 ChatGPT", page_icon="🤖")
st.title("🤖 简易 ChatGPT")

# 1. 初始化 session_id（固定用户，或让用户输入）
if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit_user_001"

# 2. 初始化消息历史（前端显示用）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. 侧边栏显示当前配置（可选）
with st.sidebar:
    st.write("### 配置信息")
    st.write(f"Session ID: {st.session_state.session_id}")
    # 此处可添加一个刷新缓存或清除历史的按钮，暂不实现

# 4. 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 获取用户输入（阻塞式组件）
if prompt := st.chat_input("请输入你的问题..."):
    # 5.1 将用户消息添加到前端历史并显示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5.2 准备发送给后端的请求体
    payload = {
        "prompt": prompt,
        "session_id": st.session_state.session_id,
        "temperature": 0.7,
    }

    # 5.3 调用后端的流式接口（注意 URL 替换为你的实际地址）
    url = "http://127.0.0.1:8000/llm/chat/stream"

    # 5.4 在 assistant 气泡中准备显示流式回复
    with st.chat_message("assistant"):
        # 使用一个空的占位符，用于逐字填充
        placeholder = st.empty()
        full_response = ""

        # 发送 POST 请求，启用流式
        try:
            response = requests.post(url, json=payload, stream=True)
            if response.status_code != 200:
                st.error(f"后端错误: {response.status_code}")
                full_response = "请求失败"
            else:
                # 解析 SSE 数据流
                for line in response.iter_lines():
                    if line:
                        decoded = line.decode("utf-8")
                        if decoded.startswith("data: "):
                            data = decoded[6:]  # 去除 "data: " 前缀
                            if data == "[DONE]":
                                break
                            # 逐字追加到显示
                            full_response += data
                            placeholder.markdown(
                                full_response + "▌"
                            )  # 加一个闪烁光标效果
                # 移除最终光标，显示完整内容
                placeholder.markdown(full_response)
        except Exception as e:  # noqa: BLE001
            st.error(f"连接失败: {e}")
            full_response = "连接失败"

        # 将助手的回复存入前端历史
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    # 可选：滚动到底部（Streamlit 默认不会自动滚动，但最新版支持，无需额外处理）
    st.rerun()
