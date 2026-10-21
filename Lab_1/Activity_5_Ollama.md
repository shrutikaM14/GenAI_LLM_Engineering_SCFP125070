# Lab 1 — Activity 5: Running an LLM with Ollama

## Objective

The objective of this activity is to understand how Ollama can be used to run a Large Language Model locally.

In this activity, I examined:

- How to install and run a model using Ollama.
- Whether an internet connection is required after the model is downloaded.
- Where the inference computation takes place.
- Whether data needs to leave the local computer.
- What happens when a model is too large for the available hardware.

## 1. Installing Ollama

Ollama was installed on my Windows laptop.

I verified the installation using:

```powershell
ollama --version
```

Output:

```text
ollama version is 0.40.7
```

This confirmed that Ollama was installed successfully.

## 2. Downloading a Model

I downloaded the `llama3.2:3b` model using:

```powershell
ollama pull llama3.2:3b
```

The model download completed successfully.

The model size downloaded was approximately **2.0 GB**.

Output included:

```text
verifying sha256 digest
writing manifest
success
```

## 3. Running the Model

I started the model using:

```powershell
ollama run llama3.2:3b
```

I tested the model with the prompt:

```text
Hello, introduce yourself in one sentence.
```

The model generated:

```text
I'm an artificial intelligence designed to provide information and assist with tasks to
the best of my abilities, and I don't have a personal identity but can help answer your
questions and provide assistance on a wide range of topics.
```

This confirmed that the model was running successfully on my local computer.

## 4. Is Internet Required After Downloading the Model?

The internet is required to **download the model initially**.

After the model has been downloaded, Ollama can run the model locally without continuously sending prompts to a cloud inference provider.

Therefore, an internet connection is generally not required for normal local inference after the model is already available on the computer.

## 5. Where Does the Inference Take Place?

The inference takes place **locally on my computer**.

Ollama runs the downloaded model using the available hardware resources of the computer.

Unlike a cloud API, the prompt does not need to be sent to a remote LLM server for the model to generate a response.

## 6. Does the Data Leave the Computer?

For normal local inference, the prompts are processed by the locally running model.

Therefore, the conversation does not need to be sent to an external cloud inference provider.

This provides greater control over sensitive information compared with sending prompts to a cloud API.

However, other network activity such as downloading models or software updates can still require an internet connection.

## 7. What Happens If the Model Is Too Large?

If a model is too large for the available hardware, several problems can occur.

For example:

- The model may fail to load.
- The system may run out of RAM.
- Inference may become very slow.
- The operating system may start using virtual memory.
- The computer may become less responsive.

Therefore, the model size should be selected according to the available hardware.

For my laptop with approximately 8 GB of RAM, a smaller model such as `llama3.2:3b` is more practical than a much larger model.

## 8. Local Inference Summary

| Question | Observation |
|---|---|
| Ollama installed? | Yes |
| Ollama version | 0.40.7 |
| Model used | llama3.2:3b |
| Model downloaded successfully? | Yes |
| Approximate download size | 2.0 GB |
| Model runs locally? | Yes |
| Internet required after download? | Generally no |
| Inference location | Local computer |
| Data needs to be sent to a cloud LLM? | No for normal local inference |

## Conclusion

Ollama provides a convenient way to run LLMs locally.

In this activity, I successfully installed Ollama, downloaded the `llama3.2:3b` model, and generated a response locally.

Local inference can provide better control over data and can work without continuous internet access after the model has been downloaded.

However, the available hardware limits which models can be run efficiently. Smaller or quantized models are more suitable for computers with limited RAM and GPU resources.