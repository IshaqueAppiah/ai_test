from fastapi import APIRouter
from models.chat_models import ChatMessage, ChatResponse
from services.open_ai_service import basic_chat_open_ai, streamed_chat
from fastapi.responses import StreamingResponse
router = APIRouter()

@router.post("/chat")
async def chat(chat_message: ChatMessage) -> ChatResponse:
    message = chat_message.message
    
    response = basic_chat_open_ai(message)
    
    return ChatResponse(response=response) 

@router.post("/chat/stream")
async def stream_chat(chat_message:ChatMessage):
    message = chat_message.message
    stream_response =streamed_chat(message)
    async def event_generator():
     for event in stream_response:
        if isinstance(event, dict) and 'type' in event and event['type']=='response.output_text.delta':
            delta = event.get('delta')  # type: ignore
            if delta:
                    yield f"data: {delta}\n\n" 
           
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")
