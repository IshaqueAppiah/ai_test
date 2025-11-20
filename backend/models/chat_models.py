from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    
class EvalRunRequest(BaseModel):
    eval_id: str
    run_id: str