import os
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models.chat_models import ChatMessage
from dotenv import load_dotenv

load_dotenv()
from services.open_ai_service import  basic_chat_open_ai_file_search, search_vector_store, upload_file_to_vector_store
from routes.batch_routes import router as batch_router
from evaluations.run_openai_eval import retrieve_result, run_evaluation
from routes.chat_routes import router as chat_router
import json


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

# GET endpoint to run the eval
@app.get("/run-eval")
async def run_eval():
    run = run_evaluation()
    if isinstance(run, dict) and "error" in run:
        return {"error": run["error"]}
    if hasattr(run, "model_dump_json"):
        return json.loads(run.model_dump_json()) # type: ignore
    return run

@app.get("/get_eval_results")
async def get_results(eval_id: str, run_id: str):
    try:
        result = retrieve_result(eval_id, run_id)
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")




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


app.include_router(batch_router)


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