import os
import json
import math
import random
from datetime import datetime, timedelta
from typing import Optional
from fastmcp import FastMCP
from pydantic import Field

# Get port from environment variable or use default
port = int(os.environ.get("PORT", 8080))

mcp = FastMCP(
    name="Personal Assistant MCP Server",
    stateless_http=True,
    debug=False,
)

@mcp.tool(
    title="Welcome a user",
    description="Return a friendly welcome message for the user.",
)
def welcome(
    name: str = Field(description="Name of the user")
) -> str:
    return f"Welcome {name}! I'm your personal assistant with tools for weather, calculations, and more!"

@mcp.tool(
    title="Get weather forecast",
    description="Get a simulated weather forecast for a given city. Note: This is a demo tool with mock data.",
)
def get_weather(
    city: str = Field(description="City name to get weather for"),
    days: int = Field(default=3, description="Number of days to forecast (1-7)")
) -> str:
    # Mock weather data for demo purposes
    weather_conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Snow", "Thunderstorms"]
    
    forecast = f"Weather forecast for {city}:\n\n"
    
    for i in range(min(days, 7)):
        date = datetime.now() + timedelta(days=i)
        condition = random.choice(weather_conditions)
        temp_high = random.randint(15, 35)
        temp_low = temp_high - random.randint(5, 15)
        humidity = random.randint(30, 90)
        
        day_label = "Today" if i == 0 else "Tomorrow" if i == 1 else date.strftime("%A")
        
        forecast += f"{day_label} ({date.strftime('%Y-%m-%d')}):\n"
        forecast += f"  Condition: {condition}\n"
        forecast += f"  High: {temp_high}°C, Low: {temp_low}°C\n"
        forecast += f"  Humidity: {humidity}%\n\n"
    
    forecast += "Note: This is simulated weather data for demonstration purposes."
    return forecast

@mcp.tool(
    title="Calculate mathematical expressions",
    description="Perform mathematical calculations including basic arithmetic, trigonometry, and more.",
)
def calculate(
    expression: str = Field(description="Mathematical expression to calculate (e.g., '2 + 3 * 4', 'sin(45)', 'sqrt(16)')")
) -> str:
    try:
        # Safe evaluation of mathematical expressions
        # Replace common math functions
        safe_expression = expression.replace('^', '**')
        
        # Define safe functions
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
        }
        
        result = eval(safe_expression, safe_dict)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

@mcp.tool(
    title="Generate random password",
    description="Generate a secure random password with customizable length and character sets.",
)
def generate_password(
    length: int = Field(default=12, description="Password length (8-50 characters)"),
    include_symbols: bool = Field(default=True, description="Include special symbols"),
    include_numbers: bool = Field(default=True, description="Include numbers")
) -> str:
    import string
    
    if length < 8 or length > 50:
        return "Error: Password length must be between 8 and 50 characters"
    
    chars = string.ascii_letters  # Always include letters
    
    if include_numbers:
        chars += string.digits
    
    if include_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    password = ''.join(random.choice(chars) for _ in range(length))
    
    return f"Generated password: {password}\n\nPassword strength: {length} characters with {'letters' + (', numbers' if include_numbers else '') + (', symbols' if include_symbols else '')}"

@mcp.tool(
    title="Text analysis",
    description="Analyze text for word count, character count, and other statistics.",
)
def analyze_text(
    text: str = Field(description="Text to analyze")
) -> str:
    if not text.strip():
        return "Error: Please provide text to analyze"
    
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    analysis = f"Text Analysis Results:\n\n"
    analysis += f"Characters (with spaces): {len(text)}\n"
    analysis += f"Characters (without spaces): {len(text.replace(' ', ''))}\n"
    analysis += f"Words: {len(words)}\n"
    analysis += f"Sentences: {sentences}\n"
    analysis += f"Paragraphs: {paragraphs}\n"
    analysis += f"Average words per sentence: {len(words) / max(sentences, 1):.1f}\n"
    
    if words:
        avg_word_length = sum(len(word.strip('.,!?;:')) for word in words) / len(words)
        analysis += f"Average word length: {avg_word_length:.1f} characters\n"
    
    return analysis

@mcp.tool(
    title="Convert units",
    description="Convert between different units of measurement.",
)
def convert_units(
    value: float = Field(description="Value to convert"),
    from_unit: str = Field(description="Source unit (e.g., 'celsius', 'fahrenheit', 'meters', 'feet', 'kg', 'pounds')"),
    to_unit: str = Field(description="Target unit")
) -> str:
    conversions = {
        # Temperature
        ('celsius', 'fahrenheit'): lambda x: x * 9/5 + 32,
        ('fahrenheit', 'celsius'): lambda x: (x - 32) * 5/9,
        ('celsius', 'kelvin'): lambda x: x + 273.15,
        ('kelvin', 'celsius'): lambda x: x - 273.15,
        
        # Length
        ('meters', 'feet'): lambda x: x * 3.28084,
        ('feet', 'meters'): lambda x: x / 3.28084,
        ('meters', 'inches'): lambda x: x * 39.3701,
        ('inches', 'meters'): lambda x: x / 39.3701,
        ('kilometers', 'miles'): lambda x: x * 0.621371,
        ('miles', 'kilometers'): lambda x: x / 0.621371,
        
        # Weight
        ('kg', 'pounds'): lambda x: x * 2.20462,
        ('pounds', 'kg'): lambda x: x / 2.20462,
        ('grams', 'ounces'): lambda x: x * 0.035274,
        ('ounces', 'grams'): lambda x: x / 0.035274,
    }
    
    key = (from_unit.lower(), to_unit.lower())
    
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result:.4f} {to_unit}"
    else:
        available = list(set([unit for pair in conversions.keys() for unit in pair]))
        return f"Conversion not supported. Available units: {', '.join(sorted(available))}"

@mcp.tool(
    title="Get server info",
    description="Get information about the MCP server and available tools.",
)
def server_info() -> str:
    tools = [
        "welcome - Greet users",
        "get_weather - Weather forecasts (demo data)",
        "calculate - Mathematical calculations",
        "generate_password - Secure password generation",
        "analyze_text - Text analysis and statistics",
        "convert_units - Unit conversions",
        "server_info - This tool"
    ]
    
    info = f"Personal Assistant MCP Server\n\n"
    info += f"Transport: streamable-http\n"
    info += f"Available Tools ({len(tools)}):\n\n"
    
    for tool in tools:
        info += f"• {tool}\n"
    
    info += f"\nServer Status: Running and ready to assist!"
    return info

# IMPORTANT: no __main__ guard for deployment; start on import so Lambda boots the server automatically
mcp.run(transport="streamable-http")
