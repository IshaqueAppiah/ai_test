from fastapi import APIRouter
from models.chat_models import ChatMessage, ChatResponse
from services.open_ai_service import basic_chat_open_ai
router = APIRouter()

@router.post("/chat")
async def chat(chat_message: ChatMessage) -> ChatResponse:
    message = chat_message.message
    
    response = basic_chat_open_ai(message)
    
    return ChatResponse(response=response)

