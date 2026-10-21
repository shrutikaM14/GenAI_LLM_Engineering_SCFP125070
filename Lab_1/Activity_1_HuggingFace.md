# Lab 1 — Activity 1: Explore LLM Models on Hugging Face

## Objective

The objective of this activity is to explore three different Large Language Models (LLMs) available on Hugging Face.

One small, one medium, and one large model will be compared based on:

- Model creator
- Number of parameters
- Whether it is a generative model
- Context length
- Suitability for local execution
- Recommended hardware

## 1. Selected Models

For this activity, I selected three generative language models of different sizes:

| Category | Model | Creator | Parameters | Context Length |
|---|---|---|---:|---:|
| Small | SmolLM2-135M | Hugging Face | 135M | 8,192 tokens |
| Medium | Mistral-7B-Instruct-v0.3 | Mistral AI | 7B | 32,768 tokens |
| Large | Llama 3.1-70B-Instruct | Meta | 70B | 128,000 tokens |

All three are **generative language models** because they are designed to generate text from an input prompt.

### 1.1 SmolLM2-135M — Small Model

**Creator:** Hugging Face  
**Parameters:** 135 million  
**Type:** Generative, decoder-only Transformer  
**Context length:** 8,192 tokens  
**Local execution:** Yes. This model is small enough to run locally on a normal computer, especially using a suitable quantized version.  
**Hardware:** It has relatively low inference requirements compared with the other two models. The Hugging Face model card reports training on H100 GPUs, but that refers to training the model, not the hardware required by a user for inference.

SmolLM2 is suitable for learning, experimentation, and lightweight local applications.

### 1.2 Mistral-7B-Instruct-v0.3 — Medium Model

**Creator:** Mistral AI  
**Parameters:** 7 billion  
**Type:** Generative, instruction-tuned language model  
**Context length:** 32,768 tokens  
**Local execution:** Possible, but it requires substantially more memory than SmolLM2. Quantized versions make local execution much more practical.  
**Hardware:** A GPU with sufficient VRAM is recommended for faster inference. For example, a 7B model in full precision requires considerably more memory than a 135M model.

The model configuration specifies a maximum position length of 32,768 tokens.

### 1.3 Llama 3.1-70B-Instruct — Large Model

**Creator:** Meta  
**Parameters:** 70 billion  
**Type:** Generative, instruction-tuned language model  
**Context length:** 128,000 tokens  
**Local execution:** Not practical on a typical laptop. It requires substantial memory and powerful hardware, although quantized versions can reduce the memory requirement.  
**Hardware:** High-end multi-GPU or large-memory systems are appropriate. Meta's training used H100 80GB GPUs, illustrating the scale of hardware involved with this model family.

The Llama 3.1 model card specifies a 128K context length for the 70B model.

---

## 2. Comparison of Local Suitability

| Model | Local Execution | Suitable for a Typical Laptop? | Relative Hardware Requirement |
|---|---|---|---|
| SmolLM2-135M | Yes | Yes | Low |
| Mistral-7B-Instruct-v0.3 | Yes, preferably quantized | Depends on RAM/GPU | Medium to High |
| Llama 3.1-70B-Instruct | Possible with specialized hardware/quantization | No | Very High |

### Observation

As the number of parameters increases, the memory and computing requirements also increase. SmolLM2-135M is the easiest of the three to run locally. Mistral-7B can be run locally with appropriate hardware and quantization. Llama 3.1-70B requires much more powerful hardware and is generally better suited to high-end systems or cloud/inference services.

## 3. Conclusion

The comparison shows that LLM size has a major effect on the hardware required for local execution.

The **SmolLM2-135M** model is the easiest to run locally because it has only 135 million parameters and requires relatively little memory.

The **Mistral-7B-Instruct-v0.3** model is considerably larger and requires more system memory or GPU VRAM. Quantization can make local execution more practical.

The **Llama 3.1-70B-Instruct** model is much larger and generally requires high-end hardware or cloud-based inference for practical use.

Therefore, when selecting an LLM for local use, both the model's capabilities and the available hardware must be considered. A smaller model may be more practical on a laptop, while larger models may provide greater capabilities but require significantly more computing resources.