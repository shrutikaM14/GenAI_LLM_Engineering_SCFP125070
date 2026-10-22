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
class ResearchData(BaseModel):
    research_question: str = Field(
        description="The main research question being investigated"
    )
    method: str = Field(
        description="The method or study design used by the researchers"
    )
    key_finding: str = Field(
        description="The main finding or result of the research"
    )


parser = PydanticOutputParser(pydantic_object=ResearchData)

# Step 1: PromptTemplate
abstract_prompt = PromptTemplate.from_template(
    """
Extract the research question, method, and key finding
from the following research paper abstract.

Research Paper Abstract:
{abstract_text}

{format_instructions}
"""
).partial(
    format_instructions=parser.get_format_instructions()
)

# Step 2: ChatPromptTemplate
summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a science communicator explaining to a general audience."
        ),
        (
            "user",
            """
Create a simple layperson-friendly summary from this structured research data:

Research Question: {research_question}
Method: {method}
Key Finding: {key_finding}

Explain:
- What the researchers wanted to find out
- How they studied it
- What they found

Use simple language that a general audience can understand.

Do not use information that is not present in the structured data.
"""
        )
    ]
)

str_parser = StrOutputParser()

# Take input from user
abstract_text = input("Enter research paper abstract: ")

# Step 1
step1_input = abstract_prompt.invoke({
    "abstract_text": abstract_text
})

step1_response = llm.invoke(step1_input)

structured_data = parser.invoke(step1_response)

# Step 2
step2_input = summary_prompt.invoke({
    "research_question": structured_data.research_question,
    "method": structured_data.method,
    "key_finding": structured_data.key_finding
})

step2_response = llm.invoke(step2_input)

layperson_summary = str_parser.invoke(step2_response)

# Display results
print("\nStep 1 - Structured Research Data:")
print(structured_data)

print("\nStep 2 - Layperson Summary:")
print(layperson_summary)
