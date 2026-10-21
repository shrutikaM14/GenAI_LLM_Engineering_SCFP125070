# Lab 1 — Activity 9: Building a Mini Chatbot

## Objective

The objective of this activity is to understand how a chatbot maintains conversation history and uses previous messages to generate context-aware responses.

## 1. How Does the Chatbot Remember Previous Messages?

A chatbot can remember previous messages by storing the conversation history.

The history can contain:

- System instructions
- User messages
- Assistant responses

For example:

```text
User: My name is Rahul.
Assistant: Nice to meet you, Rahul.

User: What is my name?
Assistant: Your name is Rahul.
```

The chatbot can answer the second question because the previous conversation was included in the context.

## 2. Why Is Conversation History Important?

Conversation history provides context to the model.

Without previous messages, every user prompt may be treated as an independent request.

With conversation history, the chatbot can:

- Remember information mentioned earlier.
- Understand follow-up questions.
- Maintain the topic of the conversation.
- Provide more natural responses.

## 3. What Happens If History Is Dropped?

If the conversation history is removed, the model loses the previous context.

For example:

```text
User: My favorite programming language is Python.

User: Why do I like it?
```

If the previous message is not included, the chatbot may not know what **"it"** refers to.

Therefore, dropping history can make the chatbot behave more like a one-off question-answering system.

## 4. Chatbot vs One-Off Prompt

| Feature | One-Off Prompt | Chatbot |
|---|---|---|
| Conversation history | No | Yes |
| Context between messages | Limited | Maintained |
| Follow-up questions | Less effective | More effective |
| Personalization | Limited | Better |
| Interaction | Single request | Multiple turns |

## 5. Why Does a Chatbot Need a Loop?

A chatbot normally runs inside a loop so that it can continuously:

1. Accept a user message.
2. Add the message to conversation history.
3. Send the conversation to the model.
4. Receive the response.
5. Add the response to the history.
6. Display the response.
7. Repeat until the user exits.

A simplified flow is:

```text
Start
  ↓
Get user message
  ↓
Add message to history
  ↓
Send history to model
  ↓
Receive response
  ↓
Add response to history
  ↓
Display response
  ↓
Continue or Exit
```

## 6. Mini Chatbot Implementation

The chatbot was implemented using Python and Ollama.

The conversation history is stored in a list. Each user message and assistant response is added to this list.

```python
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
```

## 7. Actual Execution

The chatbot was executed using:

```powershell
python Lab_1\Activity_9_Chatbot.py
```

The chatbot successfully started and maintained conversation history.

### Actual Output

```text
Mini Chatbot
Type 'exit' to stop the chatbot.

You: My name is Shrutika
Chatbot: Hello Shrutika! It's nice to meet you. Is there anything I can help you with or would you like to chat for a bit?

You: What is my name?
Chatbot: Your name is Shrutika.

You: exit
Chatbot: Goodbye!
```

## 8. Observation

The chatbot correctly remembered the name **Shrutika** from the previous message.

When asked:

```text
What is my name?
```

the chatbot responded:

```text
Your name is Shrutika.
```

This demonstrates that the conversation history was successfully maintained and provided to the model during the next request.

## 9. What Happens When the User Exits?

The chatbot checks whether the user entered:

```text
exit
```

If the user enters `exit`, the loop stops and the chatbot displays:

```text
Chatbot: Goodbye!
```

## 10. Conclusion

A chatbot differs from a one-off LLM request because it maintains conversation history.

Conversation history allows the model to understand previous messages and answer follow-up questions more effectively.

In this activity, the chatbot successfully remembered the user's name across multiple messages, demonstrating the importance of maintaining conversation history.