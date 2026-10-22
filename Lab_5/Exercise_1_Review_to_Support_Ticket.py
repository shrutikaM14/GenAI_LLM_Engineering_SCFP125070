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

class ComplaintData(BaseModel):
    complaint: str = Field(description="The core complaint made by the customer")
    product_or_feature: str = Field(description="The product or feature mentioned by the customer")
    sentiment: str = Field(description="The customer's sentiment such as positive, negative, or mixed")


parser = PydanticOutputParser(pydantic_object=ComplaintData)


# Step 1: PromptTemplate

review_prompt = PromptTemplate.from_template(
    """
Extract the core complaint, product or feature mentioned,
and customer sentiment from the following customer review.

Customer Review:
{review_text}

{format_instructions}
"""
).partial(
    format_instructions=parser.get_format_instructions()
)


# Step 2: ChatPromptTemplate

ticket_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a support ticket writer. "
            "Create a concise internal support ticket summary "
            "using only the structured customer complaint data provided."
        ),
        (
            "user",
            """
Create a support ticket summary from this structured data:

Complaint: {complaint}
Product or Feature: {product_or_feature}
Sentiment: {sentiment}

Include:
- Complaint
- Product/Feature
- Sentiment
- Suggested support action

Do not use information that is not present in the structured data.
"""
        )
    ]
)


# Step 2: String output parser

str_parser = StrOutputParser()


# Take input from user

review_text = input("Enter customer review: ")


# Step 1 execution

step1_input = review_prompt.invoke({
    "review_text": review_text
})

step1_response = llm.invoke(step1_input)

structured_data = parser.invoke(step1_response)


# Step 2 execution

step2_input = ticket_prompt.invoke({
    "complaint": structured_data.complaint,
    "product_or_feature": structured_data.product_or_feature,
    "sentiment": structured_data.sentiment
})

step2_response = llm.invoke(step2_input)

support_ticket = str_parser.invoke(step2_response)


# Output

print("\nStep 1 - Structured Complaint Data:")
print(structured_data)

print("\nStep 2 - Support Ticket Summary:")
print(support_ticket)