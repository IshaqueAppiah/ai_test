from typing import List
from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


class OllamaJustMessage(BaseModel):
    role:str
    content:str

class ChatMessageForOllama(BaseModel):
    model:str
    messages: List[OllamaJustMessage]
    stream:bool