from langchain_groq import ChatGroq
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

# Create the LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# Pydantic schema for expense splitter
class ExpenseSplitInput(BaseModel):
    total_amount: float = Field(
        gt=0,
        description="Total bill amount. Must be greater than 0."
    )
    num_people: int = Field(
        gt=0,
        description="Number of people sharing the bill. Must be greater than 0."
    )


# Expense splitting function
def split_expense(
    total_amount: float,
    num_people: int
) -> str:

    amount_per_person = total_amount / num_people

    return f"Each person owes: ₹{amount_per_person:.2f}"


# Create StructuredTool
expense_tool = StructuredTool.from_function(
    func=split_expense,
    name="split_expense",
    description=(
        "Split a total bill equally among a given number of people "
        "and calculate how much each person owes."
    ),
    args_schema=ExpenseSplitInput
)


# ---------------------------------------------------------
# Manual tool call
# ---------------------------------------------------------

total_amount = float(
    input("Enter total bill amount: ")
)

num_people = int(
    input("Enter number of people: ")
)

manual_result = expense_tool.invoke({
    "total_amount": total_amount,
    "num_people": num_people
})

print("\nManual Call Result:")
print(manual_result)


# ---------------------------------------------------------
# Bind the tool to the model
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools([expense_tool])


# Take natural-language query
user_query = input("\nEnter your expense splitting query: ")


# First model call
response = llm_with_tools.invoke(user_query)

print("\nModel Suggested Tool Calls:")
print(response.tool_calls)


# ---------------------------------------------------------
# Manually execute the model's suggested tool call
# ---------------------------------------------------------

tool_results = []

for tool_call in response.tool_calls:

    if tool_call["name"] == "split_expense":

        result = expense_tool.invoke(
            tool_call["args"]
        )

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": "split_expense",
            "result": result
        })


print("\nBound-Flow Tool Result:")
for result in tool_results:
    print(result["result"])


# ---------------------------------------------------------
# Compare manual result with bound-flow result
# ---------------------------------------------------------

bound_result = tool_results[0]["result"]

print("\nComparison:")
print("Manual Result:     ", manual_result)
print("Bound-Flow Result: ", bound_result)

if manual_result == bound_result:
    print("Match: YES - Both results are identical.")
else:
    print("Match: NO - Results are different.")


# ---------------------------------------------------------
# Send the tool result back to the model
# ---------------------------------------------------------

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