import openai
import streamlit as st

# 讀key跟建立
client = openai.OpenAI(api_key='')

# 初始化對話
if 'history' not in st.session_state:
    st.session_state['history'] = []

# 聊天
def chat_with_gpt(message):
    # 前置角色設定
    if not st.session_state['history']:
        initial_system_message = {
            "role": "system", 
            "content": "沈浸式的徹底扮演專業的四柱八字天干地支全方位命理師，別叫人去諮詢專業人士，因為你已經是了，包含回應的風格語氣都必須徹頭徹尾的完美扮演，請全心投入，用戶發送的所有疑問都要試圖從命理的角度來回答，使用繁體中文(zh-tw)解答所有問題"
        }
    else:
        initial_system_message = None

    # 給 API 的訊息列表
    messages_to_send = [initial_system_message] if initial_system_message else []
    messages_to_send += [{"role": "user", "content": message}]
    messages_to_send += [{"role": h[0], "content": h[1]} for h in st.session_state['history']]

    # 指定模型
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages_to_send
    )
    gpt_response = response.choices[0].message.content

    # 把人跟AI 的對話訊息加到歷史顯示
    st.session_state['history'].append(["user", message])
    st.session_state['history'].append(["assistant", gpt_response])

# 清空對話歷史
def clear_history():
    st.session_state['history'] = []

# 界面設定
st.set_page_config(page_title="命理GPT Beta Preview", layout="wide")

# 後面的css
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
        background-color: #919191;
    }
    .assistant-message {
        background-color: #F88379;
    }
    .input_prompt {
        font-size: 20px;
        font-weight: bold;
    }
    .sidebar .markdown-text {
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 標題
st.title("命理GPT Beta Preview")

# 側欄
with st.sidebar:
    st.markdown("""
        **核心技術:** Fine-Tuning(微調)
    """)
    st.markdown("  \n")
    st.markdown("有任何意見或建議，歡迎填寫  \n[意見表單](https://forms.gle/cC6c3jgv4tkxFqL97)")
    st.markdown("---")
    st.markdown("**目前版本:** 1.14.0")

# 輸入框上面的字
st.markdown('<p class="input_prompt">輸入您的疑惑：</p>', unsafe_allow_html=True)

# 輸入
user_input = st.text_input("", key="user_input")

# 按鈕放容器裡預防動到後面排版(歪掉)
with st.container():
    col1, col2 = st.columns([12, 2])

    with col1:
        if st.button("解惑"):
            chat_with_gpt(user_input)

    with col2:
        if st.button("清除歷史"):
            clear_history()

# 空columns再預防上面動到排版
st.columns(1)

# 對話歷史
if 'history' in st.session_state:
    for role, message in st.session_state['history']:
        key = f"{role}-{hash(message)}"
        label = "你" if role == "user" else "命理師"
        # 保持api訊息格式(輸出正常換行之類)
        formatted_message = f"<pre>{message}</pre>"
        message_class = "user-message" if role == "user" else "assistant-message"
        # 保留格式的訊息替代原始 message
        st.markdown(f"<div class='message {message_class}'><span class='message-label'>{label}:</span>{formatted_message}</div>", unsafe_allow_html=True)
