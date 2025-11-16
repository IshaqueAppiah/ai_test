from openai import OpenAI

client = OpenAI()

def basic_chat_open_ai(chat:str):
    response = client.responses.create(
    model="gpt-5-nano",
    input=chat
)
    print(response)
    return response.output_text