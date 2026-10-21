from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


PROMPT = """
You are a content refinement assistant.

Draft Text:
{draft_text}

Issue to Fix:
{issue_to_fix}

Improve the draft by resolving the specified issue.

Rules:
1. Fix only the specified issue.
2. Preserve the original meaning.
3. Make the revised text clear and natural.
4. Do not add unnecessary information.
5. Return only the revised text.
"""


draft_text = input("Enter draft text: ")
issue_to_fix = input("Enter issue to fix: ")


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


current_text = draft_text

for round_number in range(1, 4):

    prompt = PROMPT.format(
        draft_text=current_text,
        issue_to_fix=issue_to_fix
    )

    current_text = ask_llm(prompt)

    print("\nRound", round_number, ":")
    print(current_text)


print("\nFinal Revised Text:")
print(current_text)