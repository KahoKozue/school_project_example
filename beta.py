import openai
import streamlit as st

#創建 OpenAI 客戶端
client = openai.OpenAI(api_key='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')

#初始化對話歷史
if 'history' not in st.session_state:
    st.session_state['history'] = []

#聊天功能
def chat_with_gpt(message):
    # 添加初始化的系統消息（不顯示在界面上）
    if not st.session_state['history']:
        initial_system_message = {
            "role": "system", 
            "content": "沉浸式的徹底扮演專業的命理師，遇到與命理無關的問題時一律拒絕回答，不許講出任何無關命理的話語，並且使用繁體中文解答所有問題"
        }
    else:
        initial_system_message = None

    # 準備要發送給 API 的消息列表
    messages_to_send = [initial_system_message] if initial_system_message else []
    messages_to_send += [{"role": "user", "content": message}]
    messages_to_send += [{"role": h[0], "content": h[1]} for h in st.session_state['history']]

    # 發送消息並獲取回應
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )
    gpt_response = response.choices[0].message.content

    # 將用戶和 AI 的消息添加到歷史（用於顯示）
    st.session_state['history'].append(["user", message])
    st.session_state['history'].append(["assistant", gpt_response])

#Streamlit 界面
st.title("命理GPT 2023.1.12.2 Beta Preview")
st.write("命理方面 Fine-tuning chatgpt 早期專題研討會用預覽")

#輸入框
user_input = st.text_input("輸入您的疑惑：", key="user_input")

#提交按鈕
if st.button("解惑"):
    chat_with_gpt(user_input)

#顯示對話歷史
if 'history' in st.session_state:
    for role, message in st.session_state['history']:
        st.text_area("", value=message, key=message)