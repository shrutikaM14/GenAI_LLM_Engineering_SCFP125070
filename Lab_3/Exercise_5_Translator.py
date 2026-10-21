from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


PROMPT = """
You are a professional translator.

Sentence:
{sentence}

Target Language:
{target_language}

Formality:
{formality}

Translate the sentence into the requested target language.

Rules:
1. Return only the translated sentence.
2. Do not provide explanations.
3. Do not include the original sentence.
4. Match the requested formality exactly.
5. Preserve the original meaning.
6. Do not add or remove important information.
"""


sentence = input("Enter sentence: ")
target_language = input("Enter target language: ")
formality = input("Enter formality (formal/informal): ")

prompt = PROMPT.format(
    sentence=sentence,
    target_language=target_language,
    formality=formality
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


print("\nTranslation:\n")
print(ask_llm(prompt))