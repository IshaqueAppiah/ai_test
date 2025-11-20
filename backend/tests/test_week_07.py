from fastapi.testclient import TestClient
from app import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))


def test_chat_with_gemini_success(monkeypatch):
    client = TestClient(app)
    # Patch the gemini_ai_client_response in the route module
    monkeypatch.setattr(
        "routes.chat_routes.gemini_ai_client_response",
        lambda message: f"Gemini response to: {message}"
    )
    payload = {"message": "Hello Gemini!"}
    response = client.post("/chat_with_gemini", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["response"].startswith("Gemini response to: ")


def test_chat_with_gemini_error(monkeypatch):
    client = TestClient(app)
    # Patch the gemini_ai_client_response in the route module to raise an exception
    def raise_error(message):
        raise Exception("Gemini error occurred")
    monkeypatch.setattr(
        "routes.chat_routes.gemini_ai_client_response",
        raise_error
    )
    payload = {"message": "Hello Gemini!"}
    response = client.post("/chat_with_gemini", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["response"].startswith("Error: Gemini error occurred")
