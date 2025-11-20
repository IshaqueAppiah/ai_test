from google import genai
from typing import Any

client = genai.Client()

from typing import List, Dict
_gemini_conversation_history: List[Dict[str, str]] = []


def gemini_ai_client_response(users_input: str) -> str:
    _gemini_conversation_history.append({"role": "user", "content": users_input})

    conversation_str = "\n".join([
        f"{msg['role']}: {msg['content']}" for msg in _gemini_conversation_history
    ])

    models: Any = getattr(client, 'models')
    generate_content: Any = getattr(models, 'generate_content')
    response = generate_content(
        model="gemini-2.5-flash", contents=conversation_str
    )
    _gemini_conversation_history.append({"role": "assistant", "content": str(response.text)})
    return str(response.text)

