from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage
from Cxk import Cxk_text
from DingZhen import DingZhen_text
from LeiJun import LeiJun_text
from XueJie import ADXueJie_text
from CCTV import CCTV_text


class SparkChatAI:
    def __init__(self, app_id, api_secret, api_key):
        # 初始化SparkLLM
        self.spark = ChatSparkLLM(
            spark_api_url='wss://spark-api.xf-yun.com/v4.0/chat',
            spark_app_id=app_id,
            spark_api_key=api_key,
            spark_api_secret=api_secret,
            spark_llm_domain='4.0Ultra',
            streaming=False,
        )

    def get_response(self, user_input, model_name):
        # 构建消息
        system_template_text = LeiJun_text #默认选择雷军
        if model_name == "雷军":
            system_template_text = LeiJun_text
        elif model_name == "丁真":
            system_template_text = DingZhen_text
        elif model_name == "学姐":
            system_template_text = ADXueJie_text
        elif model_name == "央视配音":
            system_template_text = CCTV_text
        else:
            system_template_text = Cxk_text
        messages = [
            ChatMessage(role="system", content=system_template_text),
            ChatMessage(role="user", content=user_input),
        ]

        # 调用模型生成回答
        response = self.spark.generate([messages])

        # 只输出 message 的内容
        answer = response.generations[0][0].message.content
        return answer