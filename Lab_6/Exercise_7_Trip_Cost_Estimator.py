from langchain_groq import ChatGroq
from langchain_core.tools import tool
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
# Flight cost tool
# ---------------------------------------------------------

@tool
def get_flight_cost(origin: str, destination: str) -> str:
    """Return the approximate flight cost from origin to destination."""

    flight_costs = {
        ("Delhi", "Goa"): 7500,
        ("Mumbai", "Goa"): 4500,
        ("Bangalore", "Goa"): 5000,
        ("Delhi", "Mumbai"): 6000
    }

    cost = flight_costs.get(
        (origin, destination),
        7000
    )

    return (
        f"Approximate flight cost from "
        f"{origin} to {destination}: ₹{cost}"
    )


# ---------------------------------------------------------
# Hotel cost tool
# ---------------------------------------------------------

@tool
def get_hotel_cost(city: str, nights: int) -> str:
    """Return the approximate total hotel cost for a city and number of nights."""

    nightly_rates = {
        "Goa": 3000,
        "Mumbai": 3500,
        "Delhi": 2800,
        "Bangalore": 2500
    }

    nightly_rate = nightly_rates.get(
        city,
        3000
    )

    total_cost = nightly_rate * nights

    return (
        f"Approximate hotel cost in {city} for "
        f"{nights} nights: ₹{total_cost}"
    )


# ---------------------------------------------------------
# Food budget tool
# ---------------------------------------------------------

@tool
def get_food_budget(city: str, days: int) -> str:
    """Return the approximate food budget for a city and number of days."""

    daily_budgets = {
        "Goa": 1200,
        "Mumbai": 1000,
        "Delhi": 900,
        "Bangalore": 900
    }

    daily_budget = daily_budgets.get(
        city,
        1000
    )

    total_budget = daily_budget * days

    return (
        f"Approximate food budget in {city} for "
        f"{days} days: ₹{total_budget}"
    )


# ---------------------------------------------------------
# Bind all three tools
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools(
    [
        get_flight_cost,
        get_hotel_cost,
        get_food_budget
    ]
)


# ---------------------------------------------------------
# Take user input
# ---------------------------------------------------------

user_query = input("Enter your trip cost query: ")


# ---------------------------------------------------------
# Model suggests the flight tool
# ---------------------------------------------------------

response_flight = llm_with_tools.invoke(
    "Call the get_flight_cost tool for a trip from Delhi to Goa."
)


# ---------------------------------------------------------
# Model suggests the hotel tool
# ---------------------------------------------------------

response_hotel = llm_with_tools.invoke(
    "Call the get_hotel_cost tool for Goa for 3 nights."
)


# ---------------------------------------------------------
# Model suggests the food tool
# ---------------------------------------------------------

response_food = llm_with_tools.invoke(
    "Call the get_food_budget tool for Goa for 3 days."
)


# ---------------------------------------------------------
# Store all model responses
# ---------------------------------------------------------

responses = [
    response_flight,
    response_hotel,
    response_food
]


# ---------------------------------------------------------
# Display model suggested tool calls
# ---------------------------------------------------------

print("\nModel Suggested Tool Calls:")

for response in responses:
    print(response.tool_calls)


# ---------------------------------------------------------
# Manually execute all suggested tool calls
# ---------------------------------------------------------

tool_results = []

for response in responses:

    for tool_call in response.tool_calls:

        if tool_call["name"] == "get_flight_cost":

            result = get_flight_cost.invoke(
                tool_call["args"]
            )

        elif tool_call["name"] == "get_hotel_cost":

            result = get_hotel_cost.invoke(
                tool_call["args"]
            )

        elif tool_call["name"] == "get_food_budget":

            result = get_food_budget.invoke(
                tool_call["args"]
            )

        else:
            continue

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
# Prepare tool results for final answer
# ---------------------------------------------------------

tool_result_text = "\n".join(
    [
        f"{result['name']}: {result['result']}"
        for result in tool_results
    ]
)


# ---------------------------------------------------------
# Final combined answer
# ---------------------------------------------------------

final_response = llm.invoke(
    f"""
You are a trip cost estimation assistant.

Answer the user's request using ONLY the tool results provided below.

User request:
{user_query}

Tool results:
{tool_result_text}

Give a concise combined trip cost estimate.

Mention:
1. Flight cost
2. Hotel cost
3. Food budget
4. Approximate total cost

Do not invent different values.
Use exactly the values returned by the tools.
"""
)


print("\nFinal Combined Answer:")
print(final_response.content)