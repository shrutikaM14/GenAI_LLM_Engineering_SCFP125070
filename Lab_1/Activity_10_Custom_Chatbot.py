import ollama

# Conversation history with a custom AI/ML tutor role
history = [
    {
        "role": "system",
        "content": (
            "You are an AI and Machine Learning tutor. "
            "Explain concepts in simple language with examples. "
            "Help students understand concepts rather than just giving answers."
        )
    }
]

print("AI/ML Tutor Chatbot")
print("Type 'exit' to stop the chatbot.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Tutor: Goodbye! Keep learning!")
        break

    history.append({
        "role": "user",
        "content": user_input
    })

    response = ollama.chat(
        model="llama3.2:3b",
        messages=history
    )

    assistant_response = response["message"]["content"]

    history.append({
        "role": "assistant",
        "content": assistant_response
    })

    print("Tutor:", assistant_response)