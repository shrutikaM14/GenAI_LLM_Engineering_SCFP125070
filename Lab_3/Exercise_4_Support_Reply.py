from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


PROMPT = """
You are a professional customer support assistant.

Company Name: {company_name}

Customer Message:
{customer_message}

Maximum Words: {max_words}

Write a helpful and professional customer support reply.

Rules:
1. The reply must not exceed the specified maximum number of words.
2. Maintain a polite, professional, and helpful tone.
3. Directly address the customer's issue.
4. Do not invent information that is not provided.
5. Do not include a subject line.
6. Return only the customer support reply.
7. Keep the tone consistent for every response.
"""


customer_message = input("Enter customer message: ")
company_name = input("Enter company name: ")
max_words = input("Enter maximum number of words: ")

prompt = PROMPT.format(
    customer_message=customer_message,
    company_name=company_name,
    max_words=max_words
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


print("\nCustomer Support Reply:\n")
print(ask_llm(prompt))