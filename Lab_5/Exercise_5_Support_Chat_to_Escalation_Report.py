from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# Step 1: Structured output schema
class SupportData(BaseModel):
    issue: str = Field(
        description="The main issue or problem reported by the customer"
    )
    customer_tone: str = Field(
        description="The customer's tone such as frustrated, angry, neutral, or satisfied"
    )
    resolution_attempted: str = Field(
        description="The resolution or troubleshooting attempt already made"
    )


parser_step1 = PydanticOutputParser(
    pydantic_object=SupportData
)


# Step 1: PromptTemplate
chat_prompt = PromptTemplate.from_template(
    """
Extract the issue, customer tone, and resolution attempted
from the following customer support chat log.

Chat Log:
{chat_log_text}

{format_instructions}
"""
).partial(
    format_instructions=parser_step1.get_format_instructions()
)


# Step 2: Structured output schema
class EscalationCheck(BaseModel):
    missing_fields: list[str] = Field(
        description="Information that is missing before the issue can be escalated"
    )
    is_ready_to_escalate: bool = Field(
        description="Whether the support case is ready to be escalated"
    )


parser_step2 = PydanticOutputParser(
    pydantic_object=EscalationCheck
)


# Step 2: ChatPromptTemplate
escalation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an escalation-readiness reviewer."
        ),
        (
            "user",
            """
Review the structured support case data below.

Issue: {issue}
Customer Tone: {customer_tone}
Resolution Attempted: {resolution_attempted}

Determine:
- What important information is missing before escalation
- Whether the case is ready to be escalated

Base your evaluation only on the structured support case data.

{format_instructions}
"""
        )
    ]
).partial(
    format_instructions=parser_step2.get_format_instructions()
)


# Step 3: ChatPromptTemplate
report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a support operations lead."
        ),
        (
            "user",
            """
Create a concise escalation report using the structured data below.

Issue: {issue}
Customer Tone: {customer_tone}
Resolution Attempted: {resolution_attempted}

Missing Fields:
{missing_fields}

Ready to Escalate:
{is_ready_to_escalate}

Include:
- Issue
- Customer tone
- Resolution attempted
- Missing information
- Escalation readiness
- Recommended next action

Use only the information provided in the structured data.
"""
        )
    ]
)

str_parser = StrOutputParser()


# Take input from user
print("Enter customer support chat log.")
print("Type END on a new line when finished:")

chat_lines = []

while True:
    line = input()

    if line == "END":
        break

    chat_lines.append(line)

chat_log_text = "\n".join(chat_lines)


# Step 1
step1_input = chat_prompt.invoke({
    "chat_log_text": chat_log_text
})

step1_response = llm.invoke(step1_input)

support_data = parser_step1.invoke(step1_response)


# Step 2
step2_input = escalation_prompt.invoke({
    "issue": support_data.issue,
    "customer_tone": support_data.customer_tone,
    "resolution_attempted": support_data.resolution_attempted
})

step2_response = llm.invoke(step2_input)

escalation_check = parser_step2.invoke(step2_response)


# Convert missing fields to text
missing_fields_text = ", ".join(
    escalation_check.missing_fields
) if escalation_check.missing_fields else "None"


# Step 3
step3_input = report_prompt.invoke({
    "issue": support_data.issue,
    "customer_tone": support_data.customer_tone,
    "resolution_attempted": support_data.resolution_attempted,
    "missing_fields": missing_fields_text,
    "is_ready_to_escalate": escalation_check.is_ready_to_escalate
})

step3_response = llm.invoke(step3_input)

escalation_report = str_parser.invoke(step3_response)


# Display results
print("\nStep 1 - Structured Support Data:")
print(support_data)

print("\nStep 2 - Escalation Readiness:")
print(escalation_check)

print("\nStep 3 - Escalation Report:")
print(escalation_report)