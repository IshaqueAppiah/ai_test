from google import genai
from typing import Any
client = genai.Client()


def gemini_ai_client_response(users_input: str) -> str:
    """Legacy function for backward compatibility"""
    models: Any = getattr(client, 'models')
    generate_content: Any = getattr(models, 'generate_content')
    response = generate_content(
        model="gemini-2.5-flash", contents=users_input
    )
    return str(response.text)

