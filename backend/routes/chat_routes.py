from fastapi import APIRouter
from services.ollama_ai_service import chat_with_ollama
from services.gemini_ai_service import gemini_ai_client_response
from models.chat_models import ChatMessage, ChatMessageForOllama, ChatResponse, OllamaJustMessage
from services.open_ai_service import basic_chat_open_ai, resonining_from_openai, streamed_chat
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat(chat_message: ChatMessage) -> ChatResponse:
    message = chat_message.message
    
    response = basic_chat_open_ai(message)
    
    return ChatResponse(response=response) 

@router.post("/stream")
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


           
@router.post("/reasoning")
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


@router.post('/chat_with_gemini')
def chat_with_gemini(chat_message: ChatMessage):
    message = chat_message.message
    try:
        response = gemini_ai_client_response(message)
        return ChatResponse(response=response)
    except Exception as exc:
        return ChatResponse(response=f"Error: {str(exc)}")
    
@router.post("/ollama")
def chat_with_ollam(chat_message: ChatMessage):
    message = chat_message.message
    payload = ChatMessageForOllama(
        model="gemma3:1b", 
        messages=[OllamaJustMessage(role="user", content=message)],
        stream=False,
    )
    response = chat_with_ollama(payload)
    data = response.json()
    return {
        "content": data.get("message", {}).get("content", ""),
        "model": data.get("model", "")
    }