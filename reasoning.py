from openai import OpenAI
from decouple import config
client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

print("Streaming response with reasoning...")
print("=" * 50)

# Use responses.stream for streaming with reasoning
stream = client.responses.stream(
    model="gpt-5",
    reasoning={"effort": "medium"},
    input=[
        {
            "role": "user", 
            "content": prompt
        }
    ],
)

# Process the stream
for chunk in stream:
    if hasattr(chunk, 'output_text') and chunk.output_text:
        print(chunk.output_text, end='', flush=True)
    elif hasattr(chunk, 'status') and chunk.status == "incomplete":
        if hasattr(chunk, 'incomplete_details') and chunk.incomplete_details.reason == "max_output_tokens":
            print("\n\nRan out of tokens during streaming")
            break

print("\n" + "=" * 50)
print("Streaming complete!")