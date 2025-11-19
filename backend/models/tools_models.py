from typing import TypedDict, List, Dict, Union

class ToolParameters(TypedDict, total=False):
    type: str
    properties: Dict[str, Dict[str, Union[str, List[str]]]]
    required: List[str]

class ToolFunction(TypedDict):
    name: str
    description: str
    parameters: ToolParameters

class ToolDict(TypedDict):
    type: str
    function: ToolFunction