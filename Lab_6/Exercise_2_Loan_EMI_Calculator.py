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


# Pydantic schema for EMI calculator
class LoanEMIInput(BaseModel):
    principal: float = Field(
        gt=0,
        description="Loan principal amount. Must be greater than 0."
    )
    annual_rate: float = Field(
        ge=0,
        le=30,
        description="Annual interest rate in percentage. Must be between 0 and 30."
    )
    tenure_months: int = Field(
        gt=0,
        description="Loan tenure in months. Must be greater than 0."
    )


# EMI calculation function
def calculate_emi(
    principal: float,
    annual_rate: float,
    tenure_months: int
) -> str:

    monthly_rate = annual_rate / (12 * 100)

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** tenure_months
            / ((1 + monthly_rate) ** tenure_months - 1)
        )

    return f"Monthly EMI: ₹{emi:.2f}"


# Create StructuredTool
emi_tool = StructuredTool.from_function(
    func=calculate_emi,
    name="calculate_loan_emi",
    description=(
        "Calculate the monthly EMI for a loan using "
        "principal, annual interest rate, and tenure in months."
    ),
    args_schema=LoanEMIInput
)


# Bind the tool to the model
llm_with_tools = llm.bind_tools([emi_tool])


# Take user input
user_query = input("Enter your loan query: ")


# First model call
response = llm_with_tools.invoke(user_query)

print("\nModel Suggested Tool Calls:")
print(response.tool_calls)


# Manually execute the suggested tool call
tool_results = []

for tool_call in response.tool_calls:

    if tool_call["name"] == "calculate_loan_emi":

        result = emi_tool.invoke(tool_call["args"])

        tool_results.append({
            "tool_call_id": tool_call["id"],
            "name": "calculate_loan_emi",
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