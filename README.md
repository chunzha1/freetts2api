
# Convert edge-tts and the macOS say command to the format of OpenAI's TTS API.
把免费的tts转换为openai的tts api格式


## usage

1. 安装必要的依赖

2. 执行
   python app_all.py
  包含了edge-tts以及macos say，
3. 调用方法如下：
  curl -X POST -H "Authorization: Bearer your_api_key_here" -H "Content-Type: application/json" -d '{"input": "The quick brown fox jumped over the lazy dog.", "voice": "Cellos", "model": "tts-1-hd"}' http://localhost:8083/v1/audio/speech --output speech.mp3

   model=tts-1,调用edge-tts;
   model为其他任意值,则调用say command;
5. voice list
查看say可用voice: http://localhost:8083/siri（say为macos命令行指令，需要在macos系统运行才支持）
查看edge-tts可用voice: http://localhost:8083/edge

say command to api:
python app.py

edge-tts to api:
python app_edge.py

### Thanks：
https://github.com/rany2/edge-tts

https://maithegeek.medium.com/having-fun-in-macos-with-say-command-d4a0d3319668

#### 该项目仅个人学习使用。
