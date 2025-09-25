from openai import OpenAI
from decouple import config
client = OpenAI(api_key=config("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
        ],
    }],
)

for chunk in stream:
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
    elif hasattr(chunk, 'output_text') and chunk.output_text:
        print(chunk.output_text, end='', flush=True)