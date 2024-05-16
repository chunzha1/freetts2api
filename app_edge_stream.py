from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import edge_tts
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = ["*"]

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
    model: Optional[str] = "default"

@app.post("/v1/audio/speech")
async def speech(speech_request: SpeechRequest, api_key: str = Depends(get_api_key)):
    text = speech_request.input
    voice = speech_request.voice
    model = speech_request.model
    if voice == 'alloy': voice = "en-GB-SoniaNeural"

    async def generate_speech():
        communicate = edge_tts.Communicate(text, voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]
            elif chunk["type"] == "WordBoundary":
                pass
                # print(f"WordBoundary: {chunk}")

    try:
        return StreamingResponse(generate_speech(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_edge_stream:app", host="0.0.0.0", port=8083, reload=False)
