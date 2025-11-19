import json
def get_current_weather(location:str, unit:str="fahrenheit"):
    """Get the weather in a given location"""
    weather:dict[str, str|int]={
        "location":location,
        "temperature":50,
        "unit":unit
    }
    return json.dumps(weather)


