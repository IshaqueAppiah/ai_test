from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Any
import json

from services.open_ai_service import (
    create_batch_from_upload,
    check_batch_status,
    retrieving_batch_results,
    cancel_batch,
    get_all_batches,
)

router = APIRouter(prefix="/batch", tags=["batch"])


@router.post("/upload")
async def upload_batch(file: UploadFile = File(...)) -> dict[str, Any]:
    filename = file.filename or "uploaded_batch.jsonl"
    if not (filename.endswith('.jsonl') or file.content_type in ('application/json', 'application/x-ndjson')):
        raise HTTPException(status_code=400, detail="File must be a .jsonl (JSON Lines) file")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Validate JSONL
    try:
        text = contents.decode('utf-8') if isinstance(contents, (bytes, bytearray)) else str(contents)
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file must be UTF-8 encoded")

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Uploaded file contains no JSON lines")

    for idx, ln in enumerate(lines, start=1):
        try:
            json.loads(ln)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid JSON on line {idx}: {str(exc)}")

    try:
        result = create_batch_from_upload(text, filename=filename)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Batch creation failed: {str(exc)}")

    return {"filename": filename, "result": result}


@router.get("/status/{batch_id}")
def batch_status(batch_id: str):
    try:
        batch = check_batch_status(batch_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"batch": batch}


@router.get("/results/{file_id}")
def batch_results(file_id: str):
    try:
        data = retrieving_batch_results(file_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"file_id": file_id, "content": data}


@router.post("/cancel/{batch_id}")
def cancel(batch_id: str):
    try:
        cancel_batch(batch_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"status": "cancellation_requested", "batch_id": batch_id}


@router.get("/list")
def list_batches():
    try:
        batches = get_all_batches()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"batches": batches}
