from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

class ChatResponse(BaseModel):
    message: str
    session_id: str


class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.post("/chat",response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(message="Hello World", session_id=request.session_id)


