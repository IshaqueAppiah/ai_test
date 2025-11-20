
from typing import List, Union, Any
from models.tools_models import ToolDict


tools: List[Union[ToolDict, dict[str, Any]]] = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "the city and state eg.  San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celcius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    },
    {"type": "web_search"},
    {"type": "code_interpreter", "container": {"type": "auto"}},
]
