# Lab 1 — Activity 7: Local vs Cloud LLM Inference

## Objective

The objective of this activity is to compare running an LLM locally with using a cloud-based inference service.

## 1. If I Have an 8 GB Laptop with No Dedicated GPU

For an 8 GB laptop without a dedicated GPU, I would prefer using a **cloud-based API** for larger LLMs.

Large models require significant memory and computational resources. Running them locally on a computer with limited RAM and no dedicated GPU can be slow or may not be possible.

A small quantized model can still be considered for local inference, but a cloud API is more practical when using larger models.

## 2. Which Option Is More Private?

**Local inference is generally more private** because the model runs on my own computer and prompts do not need to be sent to an external inference provider.

However, privacy also depends on how the local system and application are configured.

With a cloud API, prompts are sent to the provider's servers, so the provider's data handling and privacy policies become important.

## 3. Which Option Is More Scalable?

**Cloud inference is generally more scalable.**

Cloud providers can use powerful GPUs and multiple servers to handle more requests and larger models.

Local inference is limited by the hardware available on my computer.

## 4. Local vs Cloud Comparison

| Feature | Local Inference | Cloud Inference |
|---|---|---|
| Model location | My computer | Provider's servers |
| Internet | Usually not required after download | Required |
| Privacy | Generally higher control | Depends on provider |
| Hardware | Must provide suitable hardware | Provider provides hardware |
| Large models | Difficult on limited hardware | Easier to access |
| Scalability | Limited | High |
| Cost | Hardware and electricity | Usually usage-based |
| Setup | More technical | Usually easier |

## 5. Advantages of Local Inference

- Better control over data.
- Can work offline after the model is downloaded.
- No API request charges.
- Full control over the model and inference environment.

## 6. Advantages of Cloud Inference

- Access to powerful hardware.
- Easier to run large models.
- Better scalability.
- No need to purchase a powerful GPU.
- Easier to integrate into applications.

## 7. Final Decision

For my **8 GB laptop without a dedicated GPU**, I would choose a **cloud-based inference service for larger LLMs** because the required computing resources are provided by the cloud.

For privacy-sensitive workloads or small models that can run efficiently on my computer, **local inference** can be a better choice.

Overall, the choice depends on the available hardware, privacy requirements, cost, model size, and scalability requirements.