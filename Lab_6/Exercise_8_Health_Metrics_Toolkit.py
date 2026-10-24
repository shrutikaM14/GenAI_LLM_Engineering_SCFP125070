from langchain_groq import ChatGroq
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------------------------------------------------
# Create the LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# ---------------------------------------------------------
# BMI input schema
# ---------------------------------------------------------

class BMIInput(BaseModel):
    weight_kg: float = Field(gt=0)
    height_m: float = Field(gt=0)


# ---------------------------------------------------------
# BMI calculation
# ---------------------------------------------------------

def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """Calculate BMI using weight in kilograms and height in meters."""

    bmi = weight_kg / (height_m ** 2)

    return f"BMI: {bmi:.2f}"


bmi_tool = StructuredTool.from_function(
    func=calculate_bmi,
    name="calculate_bmi",
    description="Calculate BMI using weight in kilograms and height in meters.",
    args_schema=BMIInput
)


# ---------------------------------------------------------
# Daily calorie input schema
# ---------------------------------------------------------

class CalorieInput(BaseModel):
    weight_kg: float = Field(gt=0)
    age: int = Field(gt=0)
    activity_level: str


# ---------------------------------------------------------
# Daily calorie calculation
# ---------------------------------------------------------

def calculate_daily_calories(
    weight_kg: float,
    age: int,
    activity_level: str
) -> str:
    """Estimate daily calorie needs using weight, age, and activity level."""

    activity_multipliers = {
        "sedentary": 25,
        "light": 30,
        "moderate": 35,
        "active": 40
    }

    multiplier = activity_multipliers.get(
        activity_level.lower(),
        30
    )

    calories = weight_kg * multiplier

    return f"Estimated daily calories: {calories:.0f} kcal"


calorie_tool = StructuredTool.from_function(
    func=calculate_daily_calories,
    name="calculate_daily_calories",
    description=(
        "Estimate daily calorie needs using weight in kilograms, "
        "age, and activity level."
    ),
    args_schema=CalorieInput
)


# ---------------------------------------------------------
# HealthToolkit class
# ---------------------------------------------------------

class HealthToolkit:

    def get_tools(self):
        return [
            bmi_tool,
            calorie_tool
        ]


# ---------------------------------------------------------
# Create toolkit
# ---------------------------------------------------------

health_toolkit = HealthToolkit()

health_tools = health_toolkit.get_tools()


# ---------------------------------------------------------
# Bind toolkit tools to the LLM
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools(health_tools)


# ---------------------------------------------------------
# Take user input
# ---------------------------------------------------------

user_query = input("Enter your health metrics query: ")


# ---------------------------------------------------------
# Ask model for BMI tool call
# ---------------------------------------------------------

bmi_response = llm_with_tools.invoke(
    f"""
From the following user request, call ONLY the calculate_bmi tool.

User request:
{user_query}
"""
)


# ---------------------------------------------------------
# Ask model for calorie tool call
# ---------------------------------------------------------

calorie_response = llm_with_tools.invoke(
    f"""
From the following user request, call ONLY the calculate_daily_calories tool.

User request:
{user_query}
"""
)


# ---------------------------------------------------------
# Display model suggested tool calls
# ---------------------------------------------------------

print("\nModel Suggested Tool Calls:")

print(bmi_response.tool_calls)
print(calorie_response.tool_calls)


# ---------------------------------------------------------
# Manually execute BMI tool
# ---------------------------------------------------------

tool_results = []

for tool_call in bmi_response.tool_calls:

    if tool_call["name"] == "calculate_bmi":

        result = bmi_tool.invoke(
            tool_call["args"]
        )

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": tool_call["name"],
            "result": result
        })


# ---------------------------------------------------------
# Manually execute calorie tool
# ---------------------------------------------------------

for tool_call in calorie_response.tool_calls:

    if tool_call["name"] == "calculate_daily_calories":

        result = calorie_tool.invoke(
            tool_call["args"]
        )

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": tool_call["name"],
            "result": result
        })


# ---------------------------------------------------------
# Print manually executed tool results
# ---------------------------------------------------------

print("\nManually Executed Tool Results:")

for result in tool_results:

    print(
        f"{result['name']}: {result['result']}"
    )


# ---------------------------------------------------------
# Prepare results
# ---------------------------------------------------------

tool_result_text = "\n".join(
    [
        f"{result['name']}: {result['result']}"
        for result in tool_results
    ]
)


# ---------------------------------------------------------
# Final answer
# ---------------------------------------------------------

final_response = llm.invoke(
    f"""
You are a health metrics assistant.

User request:
{user_query}

Use ONLY these tool results:

{tool_result_text}

Give the final answer containing:

1. BMI
2. Estimated daily calorie requirement

Do not invent or change any values.
"""
)


print("\nFinal Answer:")
print(final_response.content)