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
       
       if hasattr(event, "type"):
           if event.type == "response.output_text.delta":
                delta = getattr(event, "delta", None) # type: ignore
                print(delta) # type: ignore
                if delta:
                    yield f"data: {delta}\n\n" 
           
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")


           
@router.post("/chat/reasoning")
async def reasoning_chat(chat_message: ChatMessage):
    message = chat_message.message
    stream_response = resonining_from_openai(message)

    async def event_generator():
        for event in stream_response:
            if hasattr(event, "type"):

                if event.type == "response.reasoning_summary_text.delta":
                    delta = getattr(event, "delta", None)
                    if delta:
                        yield f"event: reasoning\ndata: {delta}\n\n"

                if event.type == "response.output_text.delta":
                    delta = getattr(event, "delta", None)
                    if delta:
                        yield f"event: output\ndata: {delta}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )

