from fastapi.testclient import TestClient
from app import app


class TestWeek05FunctionCalling:
    def test_function_calling_weather_tool(self):
        client = TestClient(app)
        # Simulate a user asking for the weather
        response = client.post("/chat", json={"message": "What is the weather in Accra in celsius?"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        # The response should mention Accra and celsius (case-insensitive)
        assert "accra" in data["response"].lower()
        assert "celsius" in data["response"].lower() or "celcius" in data["response"].lower()
        # Optionally, check for temperature or tool output pattern
        assert any(word in data["response"].lower() for word in ["temperature", "unit", "weather"])
