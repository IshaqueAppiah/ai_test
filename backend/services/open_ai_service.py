from openai import OpenAI

client = OpenAI()
conversation = client.conversations.create()


def basic_chat_open_ai(chat:str):
    response = client.responses.create( 
    model="gpt-5-nano",
    input=[{"role": "user", "content": chat}],
    conversation=conversation.id
)
    return response.output_text