from openai import OpenAI
from decouple import config
client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)

stream = client.responses.create(
    model="gpt-4.1",
    stream=True,
    tools=[{"type": "web_search"}],
    input="What are the 5 ways to get a business idea https://medium.com/@qevoltlimited/5-ways-to-find-the-right-business-idea-6581dc6d9de6"
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
    
    # Stream sources as they're discovered via annotation events
    if hasattr(chunk, 'type') and chunk.type == 'response.output_text.annotation.added':
        if hasattr(chunk, 'annotation') and chunk.annotation:
            if hasattr(chunk.annotation, 'type') and chunk.annotation.type == 'url_citation':
                print(f"\n📚 SOURCE: {getattr(chunk.annotation, 'title', 'Unknown')}")
                print(f"   URL: {getattr(chunk.annotation, 'url', 'Unknown')}")
    
    # Also check for tool calls in different event types
    if hasattr(chunk, 'type') and 'web_search_call' in chunk.type:
        print(f"\n🔧 TOOL CALL: {chunk.type}")
        if hasattr(chunk, 'item') and hasattr(chunk.item, 'action'):
            print(f"   Action: {chunk.item.action}")
        if hasattr(chunk, 'item') and hasattr(chunk.item, 'status'):
            print(f"   Status: {chunk.item.status}")

print("\n" + "="*60)
print("STREAMING COMPLETE!")
