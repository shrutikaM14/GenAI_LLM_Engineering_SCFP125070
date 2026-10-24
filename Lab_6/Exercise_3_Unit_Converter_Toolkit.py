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


# Temperature conversion tool
@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius and Fahrenheit."""

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = (value * 9 / 5) + 32

    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (value - 32) * 5 / 9

    elif from_unit == to_unit:
        result = value

    else:
        return "Unsupported temperature conversion."

    return f"{value}° {from_unit} = {result:.2f}° {to_unit}"


# Distance conversion tool
@tool
def convert_distance(value: float, from_unit: str, to_unit: str) -> str:
    """Convert distance between kilometers and miles."""

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit in ["km", "kilometers", "kilometres"] and \
       to_unit in ["miles", "mile"]:

        result = value * 0.621371

    elif from_unit in ["miles", "mile"] and \
         to_unit in ["km", "kilometers", "kilometres"]:

        result = value / 0.621371

    elif from_unit == to_unit:
        result = value

    else:
        return "Unsupported distance conversion."

    return f"{value} {from_unit} = {result:.2f} {to_unit}"


# Bind both tools to the model
llm_with_tools = llm.bind_tools(
    [
        convert_temperature,
        convert_distance
    ]
)


# Take user input
user_query = input("Enter your conversion query: ")


# First model call
response = llm_with_tools.invoke(user_query)

print("\nModel Suggested Tool Calls:")
print(response.tool_calls)


# Manually execute the suggested tool call
tool_results = []

for tool_call in response.tool_calls:

    if tool_call["name"] == "convert_temperature":

        result = convert_temperature.invoke(
            tool_call["args"]
        )

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": "convert_temperature",
            "result": result
        })

    elif tool_call["name"] == "convert_distance":

        result = convert_distance.invoke(
            tool_call["args"]
        )

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": "convert_distance",
            "result": result
        })


print("\nManually Executed Tool Result:")
for result in tool_results:
    print(result["result"])


# Send the tool result back to the model
messages = [
    {
        "role": "user",
        "content": user_query
    },
    response,
]

for result in tool_results:

    messages.append(
        {
            "role": "tool",
            "tool_call_id": result["tool_call_id"],
            "content": result["result"]
        }
    )


# Final model response
final_response = llm_with_tools.invoke(messages)

print("\nFinal Natural-Language Answer:")
print(final_response.content)