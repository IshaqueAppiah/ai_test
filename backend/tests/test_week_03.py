import pytest
from fastapi.testclient import TestClient
from app import app



class TestWeek03:
    @pytest.mark.integration
    def test_reasoning_stream(self):
        client = TestClient(app)
        response = client.post("/chat/reasoning", json={"message": "What is 2 + 2?"})
        assert response.status_code == 200
        # Parse the streamed response text
        text = response.text
        reasoning = ""
        output = ""
        event = None
        for line in text.splitlines():
            if line.startswith("event: "):
                event = line.replace("event: ", "").strip()
            elif line.startswith("data: "):
                data = line.replace("data: ", "")
                if event == "reasoning":
                    reasoning += data
                elif event == "output":
                    output += data
        assert reasoning.strip() != ""
        assert any(ans in output for ans in ["4", "four"])