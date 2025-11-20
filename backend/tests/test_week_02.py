import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from app import app


class TestWeek02:
    
    @pytest.mark.integration
    def test_conversation_memory(self):
        client = TestClient(app)
        
        # First message: provide information
        response1 = client.post("/chat", json={"message": "My name is Alice"})
        assert response1.status_code == 200
        
        # Second message: test memory of previous exchange
        response2 = client.post("/chat", json={"message": "What is my name?"})
        assert response2.status_code == 200
        assert "Alice" in response2.json()["response"]