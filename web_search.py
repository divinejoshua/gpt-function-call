from openai import OpenAI
from decouple import config
client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)

stream = client.responses.create(
    model="gpt-4.1",
    stream=True,
    tools=[{"type": "web_search"}],
    input="According to this website, what are the 5 ways to find business ideas? https://medium.com/@qevoltlimited/5-ways-to-find-the-right-business-idea-6581dc6d9de6"
)

for chunk in stream:
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
    elif hasattr(chunk, 'output_text') and chunk.output_text:
        print(chunk.output_text, end='', flush=True)
