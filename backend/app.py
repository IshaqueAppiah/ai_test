from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Application Developer Labs", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "AI Application Developer Labs Backend"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(chat_message: ChatMessage) -> ChatResponse:
    message = chat_message.message
    
    response = f"Echo: {message}"
    
    return ChatResponse(response=response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)