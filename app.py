import streamlit as st
from spark_chat_ai import SparkChatAI
import requests

# Streamlit 页面配置
st.title("映月")
st.write("月出皎兮，佼人僚兮。舒窈纠兮，劳心悄兮。月出皓兮，佼人懰兮。舒忧受兮，劳心慅兮。月出照兮，佼人燎兮。舒夭绍兮，劳心惨兮。")

# API 凭据输入框
st.sidebar.title("设置API凭据")
app_id = st.sidebar.text_input("SPARKAI_APP_ID")
api_secret = st.sidebar.text_input("SPARKAI_API_SECRET", type="password")
api_key = st.sidebar.text_input("SPARKAI_API_KEY", type="password")
fish_api_key = st.sidebar.text_input("Fish Audio API Key", type="password")

# 定义模型选项和对应的ID
model_options = {
    "雷军": "738d0cc1a3e9430a9de2b544a466a7fc",
    "学姐": "7f92f8afb8ec43bf81429cc1c9199cb1",
    "央视配音": "59cb5986671546eaa6ca8ae6f29f6d22",
    "蔡徐坤": "e4642e5edccd4d9ab61a69e82d4f8a14",
    "丁真":"54a5170264694bfc8e9ad98df7bd89c3"
}

# 文本到语音转换函数
def text_to_speech(text, reference_id, fish_api_key):
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {fish_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "reference_id": reference_id,
        "chunk_length": 200,
        "normalize": True,
        "format": "mp3",  # 可根据需求调整为 "wav" 或其他格式
        "mp3_bitrate": 64,
        "latency": "normal"
    }

    # 发送 POST 请求到 Fish Audio API
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # 保存生成的语音文件
        with open("output.mp3", "wb") as output_file:
            output_file.write(response.content)
        return "output.mp3"
    else:
        st.error(f"生成语音时出错: {response.status_code}, {response.content}")
        return None

# 检查是否填入了 API 凭据
if all([app_id, api_secret, api_key, fish_api_key]):
    # 初始化星火大模型
    chat_ai = SparkChatAI(app_id, api_secret, api_key)

    # 用户通过下拉选项选择模型
    model_name = st.sidebar.selectbox("请选择一个音色模型", options=list(model_options.keys()))
    selected_model_id = model_options[model_name]
    st.sidebar.write(f"已选择模型: {model_name}")


    # 用户输入框
    user_input = st.text_area(f"你已经选择了模型，可以开始与你的好友{model_name}聊天啦", height=150)

    # 响应提交的按钮
    if st.button("提交"):
        if user_input:
            # 调用星火大模型获取回复
            response = chat_ai.get_response(user_input, model_name)

            # 显示星火大模型的回答
            st.text_area(f"{model_name}:", response, height=200)

            # 使用星火大模型的回答调用 Fish Audio 进行文本到语音转换
            st.write("正在生成语音...")

            # 使用用户选择的模型 ID 生成语音
            audio_file = text_to_speech(response, selected_model_id, fish_api_key)

            if audio_file:
                # 播放生成的语音
                st.audio(audio_file, format='audio/mp3')
            else:
                st.error("语音生成失败")
        else:
            st.warning("请输入一个问题再提交！")
else:
    st.sidebar.warning("请填入所有 API 凭据才能继续。")
