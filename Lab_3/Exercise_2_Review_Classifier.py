from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


PROMPT = """
You are a customer review classifier.

Classify the customer review into exactly ONE of these categories:

POSITIVE:
The customer is satisfied, happy, or gives praise.

NEGATIVE:
The customer is dissatisfied, unhappy, or gives criticism.

MIXED:
The review contains both positive and negative opinions.

NEUTRAL:
The review is mainly factual and does not clearly express a positive
or negative opinion.

Customer Review:
{review_text}

Rules:
1. Return only ONE category label.
2. The output must be exactly one of:
   POSITIVE
   NEGATIVE
   MIXED
   NEUTRAL
3. Do not provide an explanation.
4. Do not add punctuation or extra text.
"""


review_text = input("Enter customer review: ")

prompt = PROMPT.format(review_text=review_text)


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