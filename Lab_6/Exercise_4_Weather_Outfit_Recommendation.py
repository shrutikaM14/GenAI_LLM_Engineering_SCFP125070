from langchain_groq import ChatGroq
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

# Create the LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# Weather tool
@tool
def get_weather(city: str) -> str:
    """Return the current temperature and weather conditions for a city."""

    weather_data = {
        "Mumbai": {
            "temperature": 31,
            "conditions": "humid and partly cloudy"
        },
        "Delhi": {
            "temperature": 24,
            "conditions": "clear"
        },
        "Pune": {
            "temperature": 26,
            "conditions": "partly cloudy"
        },
        "Bangalore": {
            "temperature": 22,
            "conditions": "cloudy"
        }
    }

    data = weather_data.get(city)

    if data is None:
        return f"Weather data not available for {city}."

    return (
        f"City: {city}, "
        f"Temperature: {data['temperature']}°C, "
        f"Conditions: {data['conditions']}"
    )


# Outfit recommendation tool
@tool
def recommend_outfit(temperature: float, conditions: str) -> str:
    """Recommend an outfit based on temperature and weather conditions."""

    conditions_lower = conditions.lower()

    if temperature >= 30:
        outfit = "Light cotton clothes, comfortable trousers or shorts, and breathable footwear."

    elif temperature >= 20:
        outfit = "A light shirt or T-shirt with comfortable trousers and casual footwear."

    else:
        outfit = "Warm clothes such as a sweater or light jacket with long trousers."

    if "rain" in conditions_lower or "storm" in conditions_lower:
        outfit += " Carry an umbrella or rain jacket."

    elif "humid" in conditions_lower:
        outfit += " Choose breathable fabric and carry water."

    elif "sunny" in conditions_lower or "clear" in conditions_lower:
        outfit += " Sunglasses and sunscreen may be useful."

    return outfit


# Bind both tools to the model
llm_with_tools = llm.bind_tools(
    [
        get_weather,
        recommend_outfit
    ]
)


# Take user input
user_query = input("Enter your weather/outfit query: ")


# ---------------------------------------------------------
# ROUND 1: Ask the model which tool it needs first
# ---------------------------------------------------------

response_1 = llm_with_tools.invoke(user_query)

print("\nFirst Model Tool Calls:")
print(response_1.tool_calls)


# Manually execute get_weather
weather_result = None
weather_tool_call = None

for tool_call in response_1.tool_calls:

    if tool_call["name"] == "get_weather":

        weather_tool_call = tool_call

        weather_result = get_weather.invoke(
            tool_call["args"]
        )


print("\nFetched Weather Data:")
print(weather_result)


# ---------------------------------------------------------
# ROUND 2: Send weather result back to the model
# ---------------------------------------------------------

messages = [
    {
        "role": "user",
        "content": user_query
    },
    response_1,
    {
        "role": "tool",
        "tool_call_id": weather_tool_call["id"],
        "content": weather_result
    }
]


response_2 = llm_with_tools.invoke(messages)

print("\nSecond Model Tool Calls:")
print(response_2.tool_calls)


# Manually execute recommend_outfit
outfit_result = None
outfit_tool_call = None

for tool_call in response_2.tool_calls:

    if tool_call["name"] == "recommend_outfit":

        outfit_tool_call = tool_call

        outfit_result = recommend_outfit.invoke(
            tool_call["args"]
        )


print("\nOutfit Tool Result:")
print(outfit_result)


# ---------------------------------------------------------
# ROUND 3: Send outfit result back for final answer
# ---------------------------------------------------------

messages.append(response_2)

messages.append(
    {
        "role": "tool",
        "tool_call_id": outfit_tool_call["id"],
        "content": outfit_result
    }
)


final_response = llm_with_tools.invoke(messages)

print("\nFinal Recommendation:")
print(final_response.content)