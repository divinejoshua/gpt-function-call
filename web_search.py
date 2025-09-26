from openai import OpenAI
from decouple import config
client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)

stream = client.responses.create(
    model="gpt-4.1",
    stream=True,
    tools=[{"type": "web_search"}],
    input="Who won the 2024 presidential election in the United States?"
)

for chunk in stream:
    # Stream output text in real-time
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
    elif hasattr(chunk, 'output_text') and chunk.output_text:
        print(chunk.output_text, end='', flush=True)
    
    # Stream tool calls as they happen
    if hasattr(chunk, 'item') and hasattr(chunk.item, 'type'):
        if chunk.item.type == 'web_search_call':
            print(f"\n🔧 TOOL CALL: {chunk.item.type}")
            if hasattr(chunk.item, 'action'):
                print(f"   Action: {chunk.item.action}")
            if hasattr(chunk.item, 'status'):
                print(f"   Status: {chunk.item.status}")
    
    # Stream sources as they're discovered
    if hasattr(chunk, 'annotation') and chunk.annotation:
        if hasattr(chunk.annotation, 'type') and chunk.annotation.type == 'url_citation':
            print(f"\n📚 SOURCE: {getattr(chunk.annotation, 'title', 'Unknown')}")
            print(f"   URL: {getattr(chunk.annotation, 'url', 'Unknown')}")

print("\n" + "="*60)
print("STREAMING COMPLETE!")
