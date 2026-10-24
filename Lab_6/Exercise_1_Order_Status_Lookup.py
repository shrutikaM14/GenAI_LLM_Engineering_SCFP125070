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


# Order status lookup tool
@tool
def lookup_order_status(order_id: str) -> str:
    """Look up the shipping status of an order using its order ID."""

    order_status = {
        "ORD-4521": "Your order has been shipped and is currently in transit.",
        "ORD-1001": "Your order has been delivered.",
        "ORD-2002": "Your order is being processed.",
        "ORD-3003": "Your order is out for delivery."
    }

    return order_status.get(
        order_id,
        "Order ID not found. Please check the order ID."
    )


# Bind the tool to the model
llm_with_tools = llm.bind_tools([lookup_order_status])


# Take user input
user_query = input("Enter your order query: ")


# First model call
response = llm_with_tools.invoke(user_query)

print("\nModel Suggested Tool Calls:")
print(response.tool_calls)


# Manually execute the suggested tool call
tool_results = []

for tool_call in response.tool_calls:

    if tool_call["name"] == "lookup_order_status":

        order_id = tool_call["args"]["order_id"]

        result = lookup_order_status.invoke({
            "order_id": order_id
        })

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": "lookup_order_status",
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