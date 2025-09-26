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

# Track different types of content
output_text = ""
tool_calls = []
sources = []

for chunk in stream:
    # Extract output text
    if hasattr(chunk, 'delta') and chunk.delta:
        output_text += chunk.delta
        print(chunk.delta, end='', flush=True)
    elif hasattr(chunk, 'output_text') and chunk.output_text:
        output_text += chunk.output_text
        print(chunk.output_text, end='', flush=True)
    
    # Extract tool calls
    if hasattr(chunk, 'item') and hasattr(chunk.item, 'type'):
        if chunk.item.type == 'web_search_call':
            tool_calls.append({
                'type': 'web_search',
                'action': getattr(chunk.item, 'action', None),
                'status': getattr(chunk.item, 'status', None)
            })
    
    # Extract sources from annotations
    if hasattr(chunk, 'annotation') and chunk.annotation:
        if hasattr(chunk.annotation, 'type') and chunk.annotation.type == 'url_citation':
            sources.append({
                'title': getattr(chunk.annotation, 'title', ''),
                'url': getattr(chunk.annotation, 'url', '')
            })

print("\n" + "="*60)
print("EXTRACTED CONTENT:")
print("="*60)

print("\n📝 OUTPUT TEXT:")
print(output_text)

print("\n🔧 TOOL CALLS:")
for i, tool in enumerate(tool_calls, 1):
    print(f"{i}. Type: {tool['type']}")
    print(f"   Action: {tool['action']}")
    print(f"   Status: {tool['status']}")

print("\n📚 SOURCES:")
for i, source in enumerate(sources, 1):
    print(f"{i}. {source['title']}")
    print(f"   URL: {source['url']}")
