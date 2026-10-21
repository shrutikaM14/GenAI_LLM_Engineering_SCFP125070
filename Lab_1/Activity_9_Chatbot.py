import ollama

# Store the conversation history
history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]

print("Mini Chatbot")
print("Type 'exit' to stop the chatbot.\n")

while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    # Add user message to history
    history.append({
        "role": "user",
        "content": user_input
    })

    # Send the complete conversation to Ollama
    response = ollama.chat(
        model="llama3.2:3b",
        messages=history
    )

    assistant_response = response["message"]["content"]

    # Add assistant response to history
    history.append({
        "role": "assistant",
        "content": assistant_response
    })

    print("Chatbot:", assistant_response)