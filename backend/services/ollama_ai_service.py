
import requests
from models.chat_models import ChatMessageForOllama


baseUrl = "http://localhost:11434/api/chat"

def chat_with_ollama(payload: ChatMessageForOllama):
    response = requests.post(baseUrl, json=payload.model_dump())
    return response