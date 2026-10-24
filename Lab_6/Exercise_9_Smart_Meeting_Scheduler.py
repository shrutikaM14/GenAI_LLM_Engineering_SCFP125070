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
# Check calendar availability tool
# ---------------------------------------------------------

@tool
def check_calendar_availability(person: str, date: str) -> str:
    """Check whether a person is available on a specific date."""

    availability = {
        ("Rahul", "2026-10-28"): "Rahul is available on 2026-10-28.",
        ("Priya", "2026-10-28"): "Priya is busy on 2026-10-28.",
        ("Amit", "2026-10-29"): "Amit is available on 2026-10-29."
    }

    return availability.get(
        (person, date),
        f"No calendar information available for {person} on {date}."
    )


# ---------------------------------------------------------
# Get timezone offset tool
# ---------------------------------------------------------

@tool
def get_timezone_offset(city: str) -> str:
    """Return the timezone offset for a city."""

    timezone_offsets = {
        "Mumbai": "UTC+5:30",
        "Delhi": "UTC+5:30",
        "London": "UTC+0",
        "New York": "UTC-4",
        "Dubai": "UTC+4"
    }

    return timezone_offsets.get(
        city,
        "Timezone information not available."
    )


# ---------------------------------------------------------
# Book meeting tool
# ---------------------------------------------------------

@tool
def book_meeting(person: str, date: str, time: str) -> str:
    """Book a meeting with a person on a specific date and time."""

    return (
        f"Meeting booked with {person} on "
        f"{date} at {time}."
    )


# ---------------------------------------------------------
# Bind all three tools
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools(
    [
        check_calendar_availability,
        get_timezone_offset,
        book_meeting
    ]
)


# =========================================================
# QUERY 1 - Availability only
# =========================================================

query_1 = input(
    "\nEnter availability query "
    "(example: Is Rahul available on 2026-10-28?): "
)

response_1 = llm_with_tools.invoke(
    f"""
Call ONLY the check_calendar_availability tool.

User query:
{query_1}
"""
)

print("\nQuery 1 - Model Suggested Tool Calls:")

for tool_call in response_1.tool_calls:
    print(tool_call)


# ---------------------------------------------------------
# Execute Query 1 tool calls
# ---------------------------------------------------------

results_1 = []

for tool_call in response_1.tool_calls:

    if tool_call["name"] == "check_calendar_availability":

        result = check_calendar_availability.invoke(
            tool_call["args"]
        )

        results_1.append(result)


print("\nQuery 1 - Tool Results:")

for result in results_1:
    print(result)


# =========================================================
# QUERY 2 - Full meeting booking
# =========================================================

query_2 = input(
    "\nEnter full meeting query "
    "(example: Book a meeting with Rahul on 2026-10-28 at 3 PM in Mumbai): "
)

# ---------------------------------------------------------
# First check availability
# ---------------------------------------------------------

availability_response = llm_with_tools.invoke(
    f"""
Call ONLY the check_calendar_availability tool.

User query:
{query_2}
"""
)

print("\nQuery 2 - Availability Tool Call:")

for tool_call in availability_response.tool_calls:
    print(tool_call)


availability_results = []

for tool_call in availability_response.tool_calls:

    if tool_call["name"] == "check_calendar_availability":

        result = check_calendar_availability.invoke(
            tool_call["args"]
        )

        availability_results.append(result)


print("\nAvailability Result:")

for result in availability_results:
    print(result)


# ---------------------------------------------------------
# Ask model for timezone
# ---------------------------------------------------------

timezone_response = llm_with_tools.invoke(
    f"""
Call ONLY the get_timezone_offset tool.

User query:
{query_2}
"""
)

print("\nQuery 2 - Timezone Tool Call:")

for tool_call in timezone_response.tool_calls:
    print(tool_call)


timezone_results = []

for tool_call in timezone_response.tool_calls:

    if tool_call["name"] == "get_timezone_offset":

        result = get_timezone_offset.invoke(
            tool_call["args"]
        )

        timezone_results.append(result)


print("\nTimezone Result:")

for result in timezone_results:
    print(result)


# ---------------------------------------------------------
# Ask model for booking
# ---------------------------------------------------------

booking_response = llm_with_tools.invoke(
    f"""
Call ONLY the book_meeting tool.

User query:
{query_2}
"""
)

print("\nQuery 2 - Booking Tool Call:")

for tool_call in booking_response.tool_calls:
    print(tool_call)


booking_results = []

for tool_call in booking_response.tool_calls:

    if tool_call["name"] == "book_meeting":

        result = book_meeting.invoke(
            tool_call["args"]
        )

        booking_results.append(result)


print("\nBooking Result:")

for result in booking_results:
    print(result)


# =========================================================
# Final Answer
# =========================================================

all_results = (
    availability_results
    + timezone_results
    + booking_results
)

final_response = llm.invoke(
    f"""
You are a smart meeting scheduler.

User request:
{query_2}

Use ONLY the following tool results:

{all_results}

Give a concise final response.

Mention:
1. Availability
2. Timezone
3. Booking status

Do not invent information.
"""
)

print("\nFinal Answer:")
print(final_response.content)