import openai
import streamlit as st

# 創建 OpenAI 客戶端
client = openai.OpenAI(api_key='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')

# 初始化對話歷史
if 'history' not in st.session_state:
    st.session_state['history'] = []

# 聊天功能
def chat_with_gpt(message):
    # 初始化系統訊息（不顯示在界面上）
    if not st.session_state['history']:
        initial_system_message = {
            "role": "system", 
            "content": "沈浸式的徹底扮演2023年的專業星座、四柱八字命理師，也別叫人去諮詢專業人士，因為你已經是了，必須徹頭徹尾的完美扮演，並且使用繁體中文解答所有問題"
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

# 清空對話歷史
def clear_history():
    st.session_state['history'] = []

# Streamlit 界面設置
st.set_page_config(page_title="命理GPT 2023.1.12.2 Beta Preview", layout="wide")

# 自定義 CSS 以改變文字大小
st.markdown(
    """
    <style>
    .message {
        font-size: 16px;
        margin-bottom: 1em;
        padding: 0.5em;
        border-radius: 5px;
        border: 1px solid #E1E4E8;
        display: flex;
        align-items: center;
    }
    .message-label {
        font-weight: bold;
        margin-right: 10px;
    }
    .user-message {
        background-color: #E6E6FA;
    }
    .assistant-message {
        background-color: #ADD8E6;
    }
    .input_prompt {
        font-size: 20px;
        font-weight: bold;
    }
    .sidebar .markdown-text { /* 增加側邊欄的字體大小 */
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 標題
st.title("命理GPT Beta Preview")

# 側邊欄
with st.sidebar:
    st.markdown("""
        **核心技術:** Fine-Tuning(微調)  
        **指導老師:** 馬芳資  
        **成員:**  
        - REDACTED_NAME  
        - REDACTED_NAME  
        - REDACTED_NAME  
        - REDACTED_NAME  
        - REDACTED_NAME  
        - REDACTED_NAME  
        - REDACTED_NAME  
    """)
    # 添加一個指向 Google 表單的鏈接
    st.markdown("  \n")
    st.markdown("有任何意見或建議，歡迎填寫  \n[回饋表單](https://forms.gle/cC6c3jgv4tkxFqL97)")
    # 顯示版本號
    st.markdown("---")  # 分隔線
    st.markdown("**版本號:** 1.12.2") 
    # 這里可以添加更多側邊欄選項

# 在輸入框上方添加自定義的提示文字
st.markdown('<p class="input_prompt">輸入您的疑惑：</p>', unsafe_allow_html=True)

# 輸入框
user_input = st.text_input("", key="user_input")  # 空字符串作為標簽

# 在容器中創建放置按钮，防止影響後續排版
with st.container():
    col1, col2 = st.columns([12, 2])

    with col1:
        if st.button("解惑"):
            chat_with_gpt(user_input)

    with col2:
        if st.button("清除歷史"):
            clear_history()

# 這里添加一個空的 columns 調用，以結束之前的列布局影響
st.columns(1)

# 顯示對話歷史
if 'history' in st.session_state:
    for role, message in st.session_state['history']:
        key = f"{role}-{hash(message)}"
        label = "你" if role == "user" else "命理師"
        message_class = "user-message" if role == "user" else "assistant-message"
        st.markdown(f"<div class='message {message_class}'><span class='message-label'>{label}:</span>{message}</div>", unsafe_allow_html=True)
