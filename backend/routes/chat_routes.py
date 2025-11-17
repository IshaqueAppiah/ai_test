from fastapi import APIRouter
from models.chat_models import ChatMessage, ChatResponse
from services.open_ai_service import basic_chat_open_ai, resonining_from_openai, streamed_chat
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


           

@router.post("/chat/reasoning")
async def reasoning_chat(chat_message: ChatMessage):
    message = chat_message.message
    reasoning_response = resonining_from_openai(message)

    async def event_generator():
        summary_sent = False
        for event in reasoning_response: # type: ignore
            if (
                isinstance(event, dict)
                and "type" in event
            ):
                if event["type"] == "response.reasoning_summary_text.delta" and not summary_sent:
                    delta = event.get("delta") # type: ignore
                    if delta:
                        yield f"data: {delta}\n\n"
                        summary_sent = True
                elif event["type"] == "response.output_text.delta":
                    delta = event.get("delta") # type: ignore
                    if delta:
                        yield f"data: {delta}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

    
