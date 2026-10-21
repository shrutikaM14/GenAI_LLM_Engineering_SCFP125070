from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


PROMPT = """
You are a resume information extractor.

Extract only the fields requested by the user from the resume.

Resume:
{resume_text}

Fields to extract:
{fields_to_extract}

Rules:
1. Return the result as valid JSON only.
2. Include only the requested fields.
3. Do not include any extra fields.
4. Do not add explanations or comments.
5. If a requested field is not found in the resume, use null as its value.
6. Use the field names exactly as provided by the user.
7. The output must contain nothing except the JSON object.

Example format:
{{
    "name": "Rahul",
    "email": "rahul@example.com"
}}
"""


resume_text = input("Enter resume text: ")
fields_to_extract = input("Enter fields to extract (comma separated): ")

prompt = PROMPT.format(
    resume_text=resume_text,
    fields_to_extract=fields_to_extract
)


def ask_llm(user_query):
    message = [
        {
            "role": "user",
            "content": user_query
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=message,
        model="openai/gpt-oss-20b"
    )

    response = chat_completion.choices[0].message.content
    return response


print(ask_llm(prompt))