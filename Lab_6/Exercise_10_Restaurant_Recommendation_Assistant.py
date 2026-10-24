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
# Find restaurants tool
# ---------------------------------------------------------

@tool
def find_restaurants(cuisine: str, city: str) -> str:
    """Find restaurants of a given cuisine in a city."""

    restaurants = {
        ("italian", "mumbai"): "Trattoria Milano, Pasta House",
        ("indian", "mumbai"): "Spice Garden, Masala Junction",
        ("chinese", "mumbai"): "Dragon Bowl, Golden Wok",
        ("italian", "delhi"): "Bella Italia, Roma Kitchen",
        ("indian", "delhi"): "Delhi Spice, Curry House"
    }

    result = restaurants.get(
        (cuisine.lower(), city.lower()),
        "No matching restaurants found."
    )

    return f"Restaurants: {result}"


# ---------------------------------------------------------
# Restaurant rating tool
# ---------------------------------------------------------

@tool
def get_restaurant_rating(restaurant_name: str) -> str:
    """Return the rating of a restaurant."""

    ratings = {
        "Trattoria Milano": "4.5/5",
        "Pasta House": "4.2/5",
        "Spice Garden": "4.4/5",
        "Masala Junction": "4.1/5",
        "Dragon Bowl": "4.3/5",
        "Golden Wok": "4.0/5",
        "Bella Italia": "4.6/5",
        "Roma Kitchen": "4.2/5",
        "Delhi Spice": "4.5/5",
        "Curry House": "4.1/5"
    }

    return ratings.get(
        restaurant_name,
        "Rating not available."
    )


# ---------------------------------------------------------
# Restaurant opening status tool
# ---------------------------------------------------------

@tool
def check_restaurant_open(
    restaurant_name: str,
    day: str
) -> str:
    """Check whether a restaurant is open on a specific day."""

    closed_days = {
        "Pasta House": "Monday",
        "Golden Wok": "Tuesday"
    }

    if (
        restaurant_name in closed_days
        and closed_days[restaurant_name].lower() == day.lower()
    ):
        return f"{restaurant_name} is closed on {day}."

    return f"{restaurant_name} is open on {day}."


# ---------------------------------------------------------
# Estimated cost tool
# ---------------------------------------------------------

@tool
def estimate_cost_for_two(restaurant_name: str) -> str:
    """Estimate the cost for two people at a restaurant."""

    costs = {
        "Trattoria Milano": 1800,
        "Pasta House": 1500,
        "Spice Garden": 1200,
        "Masala Junction": 1100,
        "Dragon Bowl": 1400,
        "Golden Wok": 1300,
        "Bella Italia": 2000,
        "Roma Kitchen": 1700,
        "Delhi Spice": 1300,
        "Curry House": 1100
    }

    cost = costs.get(
        restaurant_name,
        1500
    )

    return f"Estimated cost for two: ₹{cost}"


# ---------------------------------------------------------
# Bind all four tools
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools(
    [
        find_restaurants,
        get_restaurant_rating,
        check_restaurant_open,
        estimate_cost_for_two
    ]
)


# ---------------------------------------------------------
# Take user input
# ---------------------------------------------------------

user_query = input(
    "Enter your restaurant recommendation query: "
)


# ---------------------------------------------------------
# Ask model to find restaurants
# ---------------------------------------------------------

restaurant_response = llm_with_tools.invoke(
    f"""
Call ONLY the find_restaurants tool.

User query:
{user_query}
"""
)

print("\nRestaurant Search Tool Call:")

for tool_call in restaurant_response.tool_calls:
    print(tool_call)


restaurant_results = []

for tool_call in restaurant_response.tool_calls:

    if tool_call["name"] == "find_restaurants":

        result = find_restaurants.invoke(
            tool_call["args"]
        )

        restaurant_results.append(result)


print("\nRestaurant Search Result:")

for result in restaurant_results:
    print(result)


# ---------------------------------------------------------
# Ask model for restaurant rating
# ---------------------------------------------------------

rating_response = llm_with_tools.invoke(
    f"""
Call ONLY the get_restaurant_rating tool.

User query:
{user_query}

Use the restaurant name suggested by the restaurant
search result:

{restaurant_results}
"""
)

print("\nRating Tool Call:")

for tool_call in rating_response.tool_calls:
    print(tool_call)


rating_results = []

for tool_call in rating_response.tool_calls:

    if tool_call["name"] == "get_restaurant_rating":

        result = get_restaurant_rating.invoke(
            tool_call["args"]
        )

        rating_results.append(result)


print("\nRating Result:")

for result in rating_results:
    print(result)


# ---------------------------------------------------------
# Ask model to check restaurant opening status
# ---------------------------------------------------------

open_response = llm_with_tools.invoke(
    f"""
Call ONLY the check_restaurant_open tool.

User query:
{user_query}

Restaurant search result:
{restaurant_results}

Choose an appropriate restaurant and use the
day mentioned in the user request.
"""
)

print("\nOpening Status Tool Call:")

for tool_call in open_response.tool_calls:
    print(tool_call)


open_results = []

for tool_call in open_response.tool_calls:

    if tool_call["name"] == "check_restaurant_open":

        result = check_restaurant_open.invoke(
            tool_call["args"]
        )

        open_results.append(result)


print("\nOpening Status Result:")

for result in open_results:
    print(result)


# ---------------------------------------------------------
# Ask model for estimated cost
# ---------------------------------------------------------

cost_response = llm_with_tools.invoke(
    f"""
Call ONLY the estimate_cost_for_two tool.

User query:
{user_query}

Restaurant search result:
{restaurant_results}
"""
)

print("\nCost Tool Call:")

for tool_call in cost_response.tool_calls:
    print(tool_call)


cost_results = []

for tool_call in cost_response.tool_calls:

    if tool_call["name"] == "estimate_cost_for_two":

        result = estimate_cost_for_two.invoke(
            tool_call["args"]
        )

        cost_results.append(result)


print("\nCost Result:")

for result in cost_results:
    print(result)


# ---------------------------------------------------------
# Prepare all tool results
# ---------------------------------------------------------

all_results = (
    restaurant_results
    + rating_results
    + open_results
    + cost_results
)


# ---------------------------------------------------------
# Final recommendation
# ---------------------------------------------------------

final_response = llm.invoke(
    f"""
You are a restaurant recommendation assistant.

User request:
{user_query}

Use ONLY the following tool results:

{all_results}

Give a concise restaurant recommendation.

Mention:
1. Restaurant name
2. Cuisine/city
3. Rating
4. Opening status
5. Estimated cost for two

Do not invent information.
Do not change any values returned by the tools.
"""
)

print("\nFinal Recommendation:")
print(final_response.content)