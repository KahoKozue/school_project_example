# 八字命理諮詢機器人（Demo）

四柱八字命理聊天機器人，2023 年資訊研討會暨專題競賽展示作品。以 GPT-4 為後端，提供沉浸式命理問答體驗。

## 版本

| 檔案 | 介面 | 說明 |
|------|------|------|
| `beta_st.py` | Streamlit（Web） | 瀏覽器介面，適合展示 |
| `beta_pc.py` | Tkinter（桌面） | 本機桌面視窗版 |

## 執行

```bash
pip install openai streamlit
# 在程式碼中填入 OpenAI API Key 後執行：
streamlit run beta_st.py
```

## 技術

- Python 3
- OpenAI API（GPT-4）
- Streamlit / Tkinter
