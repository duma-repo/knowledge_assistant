
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="填写您自己的APIKey") # 填写您自己的APIKey

# history = [
#     # {"role": "system",
#     #  "content": f"""你是擅长文档阅读的好帮手，请你基于我提供的文档进行分析总结，获取关键内容，回答我的问题。
#     #             现在，我会将需要阅读的文档以文字的形式提供给你，具体内容如下:
#     #             {text}
#     #             """},
# ]

# {"role": "system",
#              "content": f"""你是擅长代码阅读的好帮手，请你基于我提供的代码进行分析总结，获取关键内容，回答我的问题。
#                         现在，我会将需要阅读的代码以文字的形式提供给你，具体内容如下:
#                         {local_text}
#                         """},


def chat(question, history, local_text):
    chat_history = []
    if local_text:
        # 长文本 prompt 及 文本内容
        chat_history.append(
            {"role": "system",
             "content": f"""你是擅长论文阅读的好帮手，请你基于我提供的论文进行分析总结，获取关键内容，回答我的问题。
                        现在，我会将需要阅读的论文以文字的形式提供给你，有多个文件。具体内容如下:
                        {local_text}
                        """},
        )
    for hist_item in history:
        chat_history.append({'role': 'user', 'content': hist_item[0]})
        if hist_item[1] != '':
            chat_history.append({'role': 'assistant', 'content': hist_item[1]})

    print(chat_history)
    completion = client.chat.completions.create(
        model="glm-4-long", # 智谱100万上下文长文大模型
        messages=chat_history,
        top_p=0.7,
        temperature=0.95,
        tools=[{"type": "web_search",
                "web_search": {"search_result": False}}],
        stream=True
    )
    for chunk in completion:
        yield chunk.choices[0].delta.content