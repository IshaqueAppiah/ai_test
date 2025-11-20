import os
import tempfile
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from app import app

def test_upload_and_search():
    client = TestClient(app)
    # Create a temp file to upload
    with tempfile.NamedTemporaryFile(delete=False, mode="w+t") as tmp:
        tmp.write("This is a test file for week 6 file search implementation.")
        tmp.seek(0)
        tmp_name = tmp.name
    # Upload the file using the endpoint (simulate UploadFile)
    with open(tmp_name, "rb") as f:
        response = client.post("/upload", files={"file": (os.path.basename(tmp_name), f, "text/plain")})
    os.unlink(tmp_name)
    assert response.status_code == 200
    data = response.json()
    assert "File uploaded and added to vector store" in data["message"]
    # Now search for a term in the uploaded file
    search_payload = {"message": "week 6 file search implementation"}
    search_response = client.post("/search_store", json=search_payload)
    assert search_response.status_code == 200
    # The response should be a string answer (from the LLM) or a dict
    assert isinstance(search_response.json(), str) or isinstance(search_response.json(), dict)
