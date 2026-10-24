from langchain_groq import ChatGroq
from langchain_core.tools import BaseTool
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

# Create the LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# Custom BaseTool subclass
class ProductStockChecker(BaseTool):

    name: str = "check_product_stock"

    description: str = (
        "Check whether a product is in stock using its product ID."
    )

    def _run(self, product_id: str) -> str:
        """Synchronous product stock check."""

        stock_data = {
            "P1023": "Product P1023 is in stock.",
            "P2045": "Product P2045 is out of stock.",
            "P3056": "Product P3056 is in stock.",
            "P4089": "Product P4089 is out of stock."
        }

        return stock_data.get(
            product_id,
            f"Product {product_id} was not found."
        )

    async def _arun(self, product_id: str) -> str:
        """Asynchronous product stock check."""

        stock_data = {
            "P1023": "Product P1023 is in stock.",
            "P2045": "Product P2045 is out of stock.",
            "P3056": "Product P3056 is in stock.",
            "P4089": "Product P4089 is out of stock."
        }

        return stock_data.get(
            product_id,
            f"Product {product_id} was not found."
        )


# Create the tool
stock_tool = ProductStockChecker()


# ---------------------------------------------------------
# Manual synchronous call
# ---------------------------------------------------------

product_id = input("Enter product ID for manual check: ")

sync_result = stock_tool.invoke({
    "product_id": product_id
})

print("\nManual Sync Call Result:")
print(sync_result)


# ---------------------------------------------------------
# Manual asynchronous call
# ---------------------------------------------------------

async def run_async_check():

    async_result = await stock_tool.ainvoke({
        "product_id": product_id
    })

    print("\nManual Async Call Result:")
    print(async_result)


asyncio.run(run_async_check())


# ---------------------------------------------------------
# Bind the tool to the model
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools([stock_tool])


# Take natural-language query
user_query = input("\nEnter your product stock query: ")


# First model call
response = llm_with_tools.invoke(user_query)

print("\nModel Suggested Tool Calls:")
print(response.tool_calls)


# Manually execute suggested tool call
tool_results = []

for tool_call in response.tool_calls:

    if tool_call["name"] == "check_product_stock":

        result = stock_tool.invoke(
            tool_call["args"]
        )

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": "check_product_stock",
            "result": result
        })


print("\nBound Flow Tool Result:")
for result in tool_results:
    print(result["result"])


# Send tool result back to the model
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