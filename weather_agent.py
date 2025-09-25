from openai import OpenAI
import json
import requests
import sys
from datetime import datetime
from decouple import config

# Initialize OpenAI client
client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)

# Weather API configuration
WEATHER_API_KEY = config("WEATHER_API_KEY")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """
    Get current weather information for a given city using OpenWeatherMap API.
    
    Args:
        city (str): The name of the city to get weather for
        
    Returns:
        str: Weather information or error message
    """
    try:
        # Construct the API URL
        api_url = f"{WEATHER_BASE_URL}?q={city}&units=metric&appid={WEATHER_API_KEY}"
        
        # Make the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Extract relevant weather information
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        
        weather_info = f"""Current weather in {city_name}, {country}:
🌡️ Temperature: {temperature}°C (feels like {feels_like}°C)
🌤️ Conditions: {description.title()}
💨 Wind Speed: {wind_speed} m/s
💧 Humidity: {humidity}%"""
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError as e:
        return f"Error parsing weather data: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Define tools for the AI model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather information for (e.g., 'London', 'New York', 'Tokyo')",
                    },
                },
                "required": ["city"],
            },
        },
    },
]

def stream_response(messages):
    """
    Stream the AI response to the terminal.
    
    Args:
        messages (list): List of message objects for the conversation
    """
    try:
        # Create a streaming response
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=True
        )
        
        # Process the stream
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='', flush=True)
                
    except Exception as e:
        print(f"Error during streaming: {str(e)}")

def save_conversation_to_file(messages, filename):
    """
    Save the conversation to a text file.
    
    Args:
        messages (list): List of message objects for the conversation
        filename (str): Name of the file to save to
    """
    content = f"""Weather Agent Conversation
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Model: gpt-4 with weather function calling

Conversation:
"""
    
    for message in messages:
        if message["role"] == "system":
            continue
        elif message["role"] == "user":
            content += f"\nUser: {message['content']}\n"
        elif message["role"] == "assistant":
            content += f"Weather Agent: {message['content']}\n"
        elif message["role"] == "tool":
            content += f"[Weather Data]: {message['content']}\n"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Conversation saved to: {filename}")

def main():
    """
    Main function to run the weather chatbot.
    """
    print("🌤️ Weather Agent Chatbot")
    print("Ask me about the weather in any city! Type 'quit' to exit.")
    print("Type 'save' to save the conversation to a file.\n")
    
    # Initialize conversation history
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful weather assistant. You can check the weather for any city using the get_weather function. Always provide friendly and informative responses about weather conditions."
        }
    ]
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nGoodbye! 👋")
                break
            
            # Check for save command
            if user_input.lower() == 'save':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"weather_conversation_{timestamp}.txt"
                save_conversation_to_file(messages, filename)
                continue
            
            if not user_input:
                continue
                
            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})
            
            # Get AI response with function calling
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            # Add assistant message to conversation
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            # Check if function call was made
            if assistant_message.tool_calls:
                # Execute the function call
                for tool_call in assistant_message.tool_calls:
                    if tool_call.function.name == "get_weather":
                        # Extract city from function arguments
                        args = json.loads(tool_call.function.arguments)
                        city = args.get("city", "")
                        
                        # Get weather data
                        weather_data = get_weather(city)
                        
                        # Add function result to conversation
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": weather_data
                        })
                        
                        # Get final response with weather data
                        final_response = client.chat.completions.create(
                            model="gpt-4",
                            messages=messages,
                            stream=True
                        )
                        
                        print("\nWeather Agent: ", end='', flush=True)
                        for chunk in final_response:
                            if chunk.choices[0].delta.content is not None:
                                print(chunk.choices[0].delta.content, end='', flush=True)
                        print()  # New line after response
            else:
                # No function call, just stream the response
                print("\nWeather Agent: ", end='', flush=True)
                stream_response(messages)
                print()  # New line after response
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            continue

if __name__ == "__main__":
    main()
