from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from app import app


class TestWeek01:
    
    def test_env_file_exists(self):
        # Check for .env in the project root (parent of backend)
        env_file = Path(__file__).parent.parent.parent / ".env"
        assert env_file.exists()
    
    @pytest.mark.integration # Integration tests typically cost money for external API calls
    def test_chat_endpoint_answers_questions(self):
        client = TestClient(app)
        response = client.post("/chat", json={"message": "What is the capital of Ghana?"})
        
        assert response.status_code == 200
        assert "Accra" in response.json()["response"]