#映月3.0
import streamlit as st
from spark_chat_ai import SparkChatAI
import requests
import ormsgpack

# Streamlit 页面配置
st.title("映月")
st.write("月出皎兮，佼人僚兮。舒窈纠兮，劳心悄兮。月出皓兮，佼人懰兮。舒忧受兮，劳心慅兮。月出照兮，佼人燎兮。舒夭绍兮，劳心惨兮。")

# API 凭据输入框
st.sidebar.title("设置API凭据")
app_id = st.sidebar.text_input("SPARKAI_APP_ID")
api_secret = st.sidebar.text_input("SPARKAI_API_SECRET", type="password")
api_key = st.sidebar.text_input("SPARKAI_API_KEY", type="password")

fish_api_key = st.sidebar.text_input("Fish Audio API Key", type="password")

# 检查是否填入了 API 凭据
if not app_id or not api_secret or not api_key or not fish_api_key:
    st.sidebar.warning("请输入所有API凭据才能继续。")
else:
    # 初始化星火大模型
    chat_ai = SparkChatAI(app_id, api_secret, api_key)

    # 用户输入框
    user_input = st.text_area("请与映月分享你的故事，我会好好倾听", height=150)

    # 响应提交的按钮
    if st.button("提交"):
        if user_input:
            # 调用星火大模型获取回复
            response = chat_ai.get_response(user_input)

            # 显示模型的回答
            st.text_area("AI 的回答", response, height=200)

            # 将模型的回答发送到 Fish Audio API 转换为语音
            st.write("正在生成语音...")


            def text_to_speech_fish(text, fish_api_key):
                # Fish Audio TTS API 终端地址
                url = "https://api.fish.audio/v1/tts"
                headers = {
                    "authorization": f"Bearer {fish_api_key}",
                    "content-type": "application/msgpack"
                }

                # 请求体
                request_payload = {
                    "text": text,
                    "format": "mp3",
                    "mp3_bitrate": 128,
                    "normalize": True,
                    "latency": "normal"
                }

                # 打包请求体
                packed_data = ormsgpack.packb(request_payload)

                # 发送请求到 Fish Audio API
                with requests.post(url, data=packed_data, headers=headers, stream=True) as response:
                    if response.status_code == 200:
                        # 创建音频文件并写入
                        with open("output.mp3", "wb") as output_file:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    output_file.write(chunk)
                        return "output.mp3"
                    else:
                        st.error("生成语音时出错")
                        return None


            # 调用函数进行文本到语音转换
            audio_file = text_to_speech_fish(response, fish_api_key)

            if audio_file:
                # 播放生成的语音
                st.audio(audio_file, format='audio/mp3')
            else:
                st.error("语音生成失败")
        else:
            st.warning("请输入一个问题再提交！")