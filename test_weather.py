#!/usr/bin/env python3
"""
Simple test script to verify the weather function works correctly.
"""

from weather_agent import get_weather

def test_weather():
    """Test the weather function with a few cities."""
    test_cities = ["London", "New York", "Tokyo", "Paris"]
    
    print("Testing weather function...\n")
    
    for city in test_cities:
        print(f"Testing weather for {city}:")
        print("-" * 40)
        weather_info = get_weather(city)
        print(weather_info)
        print("\n")

if __name__ == "__main__":
    test_weather()
