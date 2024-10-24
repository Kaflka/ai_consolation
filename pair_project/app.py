import streamlit as st
from spark_chat_ai import SparkChatAI

# Streamlit 页面配置
st.title("映月")
st.write("月出皎兮，佼人僚兮。舒窈纠兮，劳心悄兮。月出皓兮，佼人懰兮。舒忧受兮，劳心慅兮。月出照兮，佼人燎兮。舒夭绍兮，劳心惨兮。")

# API 凭据输入框
st.sidebar.title("设置API凭据")
app_id = st.sidebar.text_input("SPARKAI_APP_ID")
api_secret = st.sidebar.text_input("SPARKAI_API_SECRET", type="password")
api_key = st.sidebar.text_input("SPARKAI_API_KEY", type="password")

# 检查是否填入了 API 凭据
if not app_id or not api_secret or not api_key:
    st.sidebar.warning("请输入所有API凭据才能继续。")
else:
    # 初始化后端模型
    chat_ai = SparkChatAI(app_id, api_secret, api_key)

    # 用户输入框
    user_input = st.text_area("请与映月分享你的故事，我会好好倾听", height=150)

    # 响应提交的按钮
    if st.button("提交"):
        if user_input:
            # 调用后端模型获取回复
            response = chat_ai.get_response(user_input)
            # 显示模型的回答
            st.text_area("AI 的回答", response, height=200)
        else:
            st.warning("请输入一个问题再提交！")