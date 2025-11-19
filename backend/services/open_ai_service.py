from openai import OpenAI

client = OpenAI()
conversation = client.conversations.create()

instructions = """
You are a personal math tutor. When asked a math question, 
write and run code using the python tool to answer the question.
"""


def basic_chat_open_ai(chat: str):
    response = client.responses.create(
        model="gpt-5-nano",
        input=[{"role": "user", "content": chat}],
        tools=[
           
        ],
        conversation=conversation.id,
        instructions=instructions,
    )
    return response.output_text


def streamed_chat(chat: str):
    stream = client.responses.create(
        model="gpt-5",
        input=[{"role": "user", "content": chat}],
        reasoning={"effort": "low", "summary": "auto"},
        conversation=conversation.id,
        tools=[
            {"type": "web_search"},
            {"type": "code_interpreter", "container": {"type": "auto"}},
        ],
        stream=True,
        max_output_tokens=300,
    )
    return stream


def resonining_from_openai(chat: str):
    stream = client.responses.create(
        model="gpt-5",
        reasoning={"effort": "low", "summary": "auto"},
        input=[{"role": "user", "content": chat}],
        tools=[
            {"type": "web_search"},
            {"type": "code_interpreter", "container": {"type": "auto"}},
        ],
        conversation=conversation.id,
        stream=True,
        max_output_tokens=300,
    )
    return stream
