from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


PROMPT = """
You are a doctor assistant.

Patient Name: {patient_name}

Patient Notes:
{patient_notes}

Generate a doctor's summary with exactly these sections:

Symptoms:
Diagnosis:
Recommendation:

Rules:
1. Use exactly these three sections.
2. Keep the same format every time.
3. Summarize only the information provided in the patient notes.
4. Do not invent any information.
5. If information is not available, write "Not provided".
6. Do not add any extra sections.
"""


patient_name = input("Enter patient name: ")
patient_notes = input("Enter patient consultation notes: ")

prompt = PROMPT.format(
    patient_name=patient_name,
    patient_notes=patient_notes
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


print("\nDoctor's Summary:\n")
print(ask_llm(prompt))