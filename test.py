# import requests
#
# def text_to_speech(text, voice):
#     url = 'http://localhost:8083/tts'  # 假设 Flask 应用运行在本地的 8083 端口
#     data = {
#         'text': text,
#         'voice': voice
#     }
#     response = requests.post(url, data=data)
#
#     if response.status_code == 200:
#         # 处理返回的音频文件，例如保存到本地
#         with open('output.m4a', 'wb') as f:
#             f.write(response.content)
#         print("Audio file saved as output.m4a")
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#
# # 使用示例
# text_to_speech("Hello, world!", "Samantha")

import requests
import json

# 设置 Flask 应用的 API 地址
api_url = 'http://localhost:8083/v1/audio/speech'

# 设置 API 密钥
api_key = 'your_api_key_here'

# 要转换为语音的文本
text_to_speech = 'Hello, world!'

# 设置语音选项，例如 'Alex'
voice_option = 'Cello'

# 创建一个包含请求数据的 JSON 字典
data = {
    'input': text_to_speech,
    'voice': voice_option,
    # 可选的 model 参数，如果不需要可以省略
    'model': 'default'
}

# 将数据转换为 JSON 字符串
json_data = json.dumps(data)

# 设置请求头，包括 Content-Type 和 Authorization
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# 发送 POST 请求
response = requests.post(api_url, data=json_data, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 如果请求成功，保存接收到的 MP3 文件
    with open('output.mp3', 'wb') as f:
        f.write(response.content)
    print('语音文件已保存为 output.mp3')
else:
    # 如果请求失败，打印错误信息
    print(f'请求失败，状态码：{response.status_code}, 错误信息：{response.text}')
