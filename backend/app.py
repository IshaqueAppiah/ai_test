
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models.chat_models import ChatMessage
from dotenv import load_dotenv

load_dotenv()
from services.open_ai_service import  basic_chat_open_ai_file_search, search_vector_store, upload_file_to_vector_store
from routes.chat_routes import router as chat_router



app = FastAPI(title="AI Application Developer Labs", version="1.0.0")
vector_store_id = None
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "AI Application Developer Labs Backend"}

@app.get("/health")
async def health():
    return {"status": "healthy"}





@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str | None]:
    global vector_store_id
    temp_path = f"uploaded_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    # Call the OpenAI vector store upload function
    try:
        vector_store_id = upload_file_to_vector_store(temp_path)
        message = f"File uploaded and added to vector store (ID: {vector_store_id})!"
    except Exception as exc:
        message = f"Error uploading file to vector store: {str(exc)}"
        vector_store_id = None
    os.remove(temp_path)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": message
    }


@app.post("/search_store")


@app.post("/search_store")
def search_store(chat_message: ChatMessage) :
    global vector_store_id
    user_input = chat_message.message
    if not vector_store_id:
        return {"error": "No vector store available. Please upload a file first."}
    

    search_results = search_vector_store(user_input, vector_store_id)
    # Use attribute access for context extraction
    try:
        context = "\n".join([
            item.content[0].text for item in getattr(search_results, 'data', []) if getattr(item, 'content', None)
        ])
    except Exception:
        context = None
    response = basic_chat_open_ai_file_search(user_input, context)
    return response



if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)