from openai import OpenAI
from decouple import config

client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)

print("Streaming analysis of Berkshire Hathaway 2024 letter...")
print("=" * 60)

# Use responses.stream for streaming
stream = client.responses.create(
    model="gpt-4.1",
    stream=True,
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "tell me somethings aout mexico",
                },
                {
                    "type": "input_file",
                    "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                },
                {
                    "type": "input_file",
                    "file_url": "https://didiai-test.s3.us-east-2.amazonaws.com/mexico.pdf",
                },
            ],
        },
    ]
)

for chunk in stream:
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
    elif hasattr(chunk, 'output_text') and chunk.output_text:
        print(chunk.output_text, end='', flush=True)

print("Analysis complete!")