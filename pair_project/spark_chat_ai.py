from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage
from prompt_templated import system_template_text

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

    def get_response(self, user_input):
        # 构建消息
        messages = [
            ChatMessage(role="system", content=system_template_text),
            ChatMessage(role="user", content=user_input),
        ]

        # 调用模型生成回答
        response = self.spark.generate([messages])

        # 只输出 message 的内容
        answer = response.generations[0][0].message.content
        return answer