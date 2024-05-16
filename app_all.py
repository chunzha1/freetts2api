from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import subprocess
import edge_tts
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any


app = FastAPI()

# 配置CORS
origins = ["*"]  # 允许所有源

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "your_api_key_here"
bearer_scheme = HTTPBearer()


async def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )


class SpeechRequest(BaseModel):
    input: str
    voice: Optional[str] = "en-GB-SoniaNeural"
    model: Optional[str] = "tts-1"  # 添加了一个新的字段


@app.post("/v1/audio/speech")
async def speech(speech_request: SpeechRequest, api_key: str = Depends(get_api_key)):
    text = speech_request.input
    voice = speech_request.voice
    model = speech_request.model  # 使用新的字段

    try:
        if model == "tts-1":
            if voice == 'alloy': voice = "en-GB-SoniaNeural"
            # 使用edge-tts生成语音
            # 这里需要调用edge-tts的API或者库来生成语音
            # 例如：
            output_file = 'speech.mp3'  # 使用.aiff格式，因为.mp3在macOS上可能不兼容

            async def generate_speech():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_file)

            try:
                await generate_speech()
                # 读取文件内容
                with open(output_file, 'rb') as f:
                    audio_data = f.read()
                # 删除文件
                os.remove(output_file)
                # 返回音频数据
                return Response(content=audio_data, media_type="audio/mpeg")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            # raise HTTPException(status_code=501, detail="edge-tts is not implemented")
        else:
            if voice == 'alloy': voice = 'Cellos'
            output_file = 'speech.m4a'  # 使用.aiff格式，因为.mp3在macOS上可能不兼容
            # 使用subprocess运行say命令
            subprocess.run(['say', '-o', output_file, '-v', voice, '-f', '-'], input=text.encode(), check=True)

            # 使用ffmpeg将.aiff转换为.mp3
            mp3_output_file = 'speech.mp3'
            subprocess.run(['ffmpeg', '-i', output_file, '-acodec', 'libmp3lame', '-ab', '192k', mp3_output_file],
                           check=True)

            # 读取文件内容
            with open(mp3_output_file, 'rb') as f:
                audio_data = f.read()
            # 删除文件
            os.remove(output_file)
            os.remove(mp3_output_file)
            # 返回音频数据
            return Response(content=audio_data, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/siri")
async def list_voices():
    # 使用 subprocess 执行 say -v "?" 命令
    result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)

    # 解析命令的输出
    voices = result.stdout.strip().split('\n')
    voice_list = []
    for voice in voices:
        # 使用正则表达式匹配语音名称和语言代码
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
    return JSONResponse(content=voice_list)

@app.get("/edge")
async def list_edge_tts_voices():
    try:
        # 调用edge-tts库中的list_voices函数
        voices = await edge_tts.list_voices()
        # 假设list_voices函数返回的是一个字典列表，每个字典包含语音的属性
        # 你需要根据实际返回的数据结构来解析和格式化
        voice_list = [
            {   'voice': voice['ShortName'],
                'gender': voice['Gender'],
                'FriendlyName': voice['FriendlyName']
                # 'name': voice['Name'],  # 假设每个语音有一个'Name'属性
                # 'language_code': voice['Locale'],  # 假设每个语音有一个'Locale'属性
                # 添加其他属性，如果需要的话
            }
            for voice in voices
        ]
        # 返回 JSON 格式的响应
        return JSONResponse(content=voice_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app_all:app", host="0.0.0.0", port=8083, reload=False)
