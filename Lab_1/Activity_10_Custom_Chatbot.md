# Lab 1 — Activity 10: Customize the Chatbot

## Objective

The objective of this activity is to customize the chatbot by giving it a specific role through a system instruction.

In this activity, the chatbot is configured as an **AI and Machine Learning tutor**.

The tutor should:

- Explain AI/ML concepts in simple language.
- Provide examples.
- Help students understand concepts instead of only giving direct answers.
- Maintain conversation history.

---

## 1. Custom Role

The chatbot was given the following system instruction:

> You are an AI and Machine Learning tutor. Explain concepts in simple language with examples. Help students understand concepts rather than just giving answers.

This changes the behavior of the chatbot from a general-purpose assistant into a specialized AI/ML tutor.

---

## 2. Python Implementation

The chatbot was implemented using Ollama and the `llama3.2:3b` model.

```python
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

    ```

---

## 3. Execution

The program was executed using:

```powershell
python Lab_1\Activity_10_Custom_Chatbot.py
```

The chatbot was tested with:

```text
What is self-attention in Transformers?
```

The chatbot provided a detailed explanation of self-attention, including:

- What self-attention means.
- Why self-attention is useful.
- How attention weights are calculated.
- The roles of Query (Q) and Key (K).
- An example of self-attention.
- Advantages of self-attention.

The chatbot was then stopped using:

```text
exit
```

The program displayed:

```text
Tutor: Goodbye! Keep learning!
```

---

## 4. Does the Response Change?

Yes.

The response changes because the system instruction tells the model to behave as an AI/ML tutor.

Instead of behaving only as a general-purpose assistant, it is instructed to:

- Focus on Artificial Intelligence and Machine Learning topics.
- Explain concepts in simple language.
- Provide examples.
- Help students understand concepts.

The underlying model remains the same, but its behavior and response style are influenced by the system instruction.

---

## 5. Can the Same Model Become Different Assistants?

Yes.

The same `llama3.2:3b` model can be customized into different assistants by changing the system instruction.

For example:

```text
You are a Python programming tutor.
```

can make it behave like a Python tutor.

Similarly:

```text
You are a Data Science mentor.
```

can make it behave like a Data Science mentor.

Therefore, the same model can be used for different purposes without changing the underlying model.

---

## 6. Another Role I Would Try

Another role I would try is:

**Data Science Mentor**

The system instruction could be:

```text
You are a Data Science mentor. Explain data science concepts in simple language, provide practical examples, and guide students through problem-solving step by step.
```

This role would be useful for learning:

- Python
- Pandas
- Data visualization
- Statistics
- Machine Learning
- Data preprocessing

---

## 7. Why Role-Based Instructions Are Useful

Role-based instructions allow one general-purpose LLM to be adapted for different tasks.

| System Role | Purpose |
|---|---|
| AI/ML Tutor | Teach AI and ML concepts |
| Python Tutor | Help learn Python |
| Data Science Mentor | Guide data science learning |
| Coding Assistant | Help with programming |
| Study Planner | Create study plans |
| Interview Coach | Practice technical interviews |

---

## 8. Conclusion

This activity demonstrated how a system instruction can customize the behavior of an LLM.

The `llama3.2:3b` model was configured as an **AI/ML tutor** and successfully provided a teaching-oriented explanation of self-attention.

This shows that the same underlying LLM can act as different assistants depending on the instructions provided to it.