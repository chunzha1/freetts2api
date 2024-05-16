# from flask import Flask, request, send_file
# import subprocess
# import os
#
# app = Flask(__name__)
#
#
# @app.route('/tts', methods=['POST'])
# def text_to_speech():
#     text = request.form.get('text')
#     if not text:
#         return "Error: No text provided", 400
#
#     # 从请求中获取语音名称
#     voice = request.form.get('voice', 'Anna')  # 默认使用 'Samantha'
#
#     # 生成一个唯一的文件名
#     audio_file = f"output_{hash(text)}.m4a"
#
#     # 使用say命令将文本转换为语音，并保存到文件
#     try:
#         subprocess.run(['say', '-o', audio_file, '-v', voice, '-f', '-'], input=text.encode(), check=True)
#     except subprocess.CalledProcessError as e:
#         return f"Error: {e}", 500
#
#     # 返回音频文件给客户端
#     try:
#         return send_file(audio_file, mimetype='audio/x-aiff')
#     finally:
#         # 发送文件后立即删除
#         os.remove(audio_file)
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8083, debug=True)

from flask import Flask, request, send_file, jsonify, Response
import subprocess
import os
import hashlib
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 假设这里有一个用于验证的 API 密钥
API_KEY = 'your_api_key_here'


@app.route('/v1/audio/speech', methods=['POST'])
def text_to_speech():
    # 检查 API 密钥
    if 'Authorization' not in request.headers or not request.headers['Authorization'].startswith(f'Bearer {API_KEY}'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'input' not in data or 'voice' not in data or 'model' not in data:
        return jsonify({"error": "Invalid request"}), 400

    text = data['input']
    voice = data['voice']
    if voice == 'alloy':
        voice = 'Cellos'
    model = data['model']  # 这里可以忽略 model 参数，因为它不是必需的
    print(voice,":",text)
    # 生成一个唯一的文件名
    audio_file = f"output_{hashlib.md5(text.encode()).hexdigest()}.m4a"

    # 使用say命令将文本转换为语音，并保存到文件
    try:
        subprocess.run(['say', '-o', audio_file, '-v', voice, '-f', '-'], input=text.encode(), check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

    # 将 M4A 文件转换为 MP3 格式
    mp3_file = f"output_{hashlib.md5(text.encode()).hexdigest()}.mp3"
    try:
        subprocess.run(
            ['ffmpeg', '-i', audio_file, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', mp3_file],
            check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

    # 返回 MP3 文件给客户端
    try:
        return send_file(mp3_file, mimetype='audio/mpeg')
    finally:
        # 发送文件后立即删除
        os.remove(audio_file)
        os.remove(mp3_file)


@app.route('/voice', methods=['GET'])
def list_voice():
    # 使用 subprocess 执行 say -v "?" 命令
    result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
    # 将命令的输出内容从 latin1 编码转换为 utf-8 编码
    decoded_text = result.stdout  # .encode('utf-8')
    # 直接返回命令的输出内容
    return Response(decoded_text, content_type='text/plain')


@app.route('/voices', methods=['GET'])
def list_voices():
    # 使用 subprocess 执行 say -v "?" 命令
    result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)

    # 解析命令的输出
    voices = result.stdout.strip().split('\n')
    voice_list = []
    for voice in voices:
        # print(voice)
        # 假设每个语音选项的格式是 "Voice (Language Code) # Description"
        parts = voice.split('#')
        if len(parts) == 2:
            name = parts[0].strip()
            language_code = parts[1].rstrip(')').strip()
            voice_list.append({
                'name': name,
                'language_code': language_code,
                # 如果需要，可以添加更多信息，如描述等
            })

    # 返回 JSON 格式的响应
    return jsonify(voice_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=False)
# gunicorn -w 4 -b 0.0.0.0:8083 app:app