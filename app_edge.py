from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import edge_tts
import os
from fastapi.middleware.cors import CORSMiddleware

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
    model: Optional[str] = "default"  # 添加了一个新的字段

@app.post("/v1/audio/speech")
async def speech(speech_request: SpeechRequest, api_key: str = Depends(get_api_key)):
    text = speech_request.input
    voice = speech_request.voice
    model = speech_request.model  # 使用新的字段

    output_file = 'speech.mp3'

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_edge:app", host="0.0.0.0", port=8083, reload=False)


# uvicorn app:app --reload --port=8098 --host="0.0.0.0"

# curl -X POST "http://localhost:8099/v1/audio/speech" \
#      -H "Authorization: mysecretapikey" \
#      -H "Content-Type: application/json" \
#      -d '{"input": "Hello, world!", "voice": "en-GB-SoniaNeural", "model": "default"}'
