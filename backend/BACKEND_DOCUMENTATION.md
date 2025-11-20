# Backend Documentation

## Overview
This backend is built with FastAPI and provides AI-powered chat, file upload, vector search, and Gemini AI integration. It is structured for modularity, testability, and extensibility.

---

## Project Structure

```
backend/
├── app.py                  # Main FastAPI application
├── models/
│   └── chat_models.py      # Pydantic models for chat endpoints
├── routes/
│   └── chat_routes.py      # Chat and Gemini endpoints
├── services/
│   ├── open_ai_service.py  # OpenAI integration, vector store, file search
│   └── gemini_ai_service.py# Gemini AI integration
├── tests/                  # Unit and integration tests
│   └── test_week_*.py      # Weekly test files
├── custom_tools/           # Custom tool implementations
├── memories/               # Memory management for conversations
├── pyproject.toml          # Project dependencies and config
├── pytest.ini              # Pytest marker registration
└── ...
```

---

## Key Endpoints

### 1. `/upload` (POST)
- **Purpose:** Upload a file to be indexed in the OpenAI vector store.
- **Request:**
  - `file`: File (form-data, required)
- **Response:**
  - `filename`, `content_type`, `message`
- **Notes:**
  - The file is saved temporarily, uploaded to the vector store, then deleted.
  - Requires `python-multipart` for file parsing.

### 2. `/search_store` (POST)
- **Purpose:** Search the vector store using a user query and return an AI-generated answer.
- **Request:**
  - JSON: `{ "message": "your search query" }`
- **Response:**
  - `{ "answer": <AI answer>, "context": <retrieved context> }`
- **Notes:**
  - Uses OpenAI to search and then answer using the retrieved context.

### 3. `/chat` (POST)
- **Purpose:** General chat endpoint using OpenAI.
- **Request:**
  - JSON: `{ "message": "your message" }`
- **Response:**
  - `{ "response": <AI answer> }`

### 4. `/chat/stream` (POST)
- **Purpose:** Streamed chat responses from OpenAI.
- **Request:**
  - JSON: `{ "message": "your message" }`
- **Response:**
  - Server-Sent Events (SSE) stream

### 5. `/chat/reasoning` (POST)
- **Purpose:** Streamed reasoning and output from OpenAI.
- **Request:**
  - JSON: `{ "message": "your message" }`
- **Response:**
  - SSE stream with reasoning and output events

### 6. `/chat_with_gemini` (POST)
- **Purpose:** Chat endpoint using Gemini AI.
- **Request:**
  - JSON: `{ "message": "your message" }`
- **Response:**
  - `{ "response": <Gemini answer or error> }`
- **Notes:**
  - Handles errors and returns them in the response.

---

## Services

### `open_ai_service.py`
- Handles all OpenAI API interactions: chat, function calling, vector store, file search.
- Provides utility functions for basic chat, function calling, streaming, and vector search.

### `gemini_ai_service.py`
- Integrates with Google Gemini AI for chat.
- Exposes a function for use in the `/chat_with_gemini` endpoint.

---

## Models

### `ChatMessage`
- Pydantic model: `{ message: str }`

### `ChatResponse`
- Pydantic model: `{ response: str }`

---

## Testing
- All endpoints are covered by tests in `tests/`.
- Tests use FastAPI's `TestClient` and `pytest`.
- Markers (e.g., `@pytest.mark.integration`) are registered in `pytest.ini`.
- Mocking is used for external AI services in tests.

---

## Error Handling
- Upload and chat endpoints handle and return errors gracefully.
- If a file is missing or a service fails, a clear error message is returned.

---

## Dependencies
- FastAPI
- python-multipart (for file uploads)
- openai
- google-genai
- pytest, httpx, and other test tools

---

## Environment
- Environment variables are loaded from `.env` using `python-dotenv`.
- Sensitive keys (OpenAI, Gemini) should be set in `.env`.

---

## Extending the Backend
- Add new endpoints in `routes/` and register them in `app.py`.
- Add new services in `services/` for additional AI or utility integrations.
- Add new Pydantic models in `models/` as needed.
- Add tests in `tests/` for new features.

---

## Example Usage

**Upload a file:**
```bash
curl -F "file=@myfile.txt" http://localhost:8000/upload
```

**Search the vector store:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "search query"}' http://localhost:8000/search_store
```

**Chat with Gemini:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello Gemini!"}' http://localhost:8000/chat_with_gemini
```

---

## Contact
For questions or contributions, please contact the repository owner or open an issue on GitHub.
