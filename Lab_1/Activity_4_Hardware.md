# Lab 1 — Activity 4: Computer Hardware and Memory Estimation

## Objective

The objective of this activity is to understand how computer hardware affects the ability to run Large Language Models (LLMs) locally.

In this activity, I will:

- Check the available RAM and GPU hardware.
- Estimate the memory required for model weights at different precisions.
- Compare a 4B model in FP16 and INT4.
- Compare a 4B INT4 model with a 7B INT4 model.
- Understand why additional memory is required beyond model weights.
- Examine whether quantization is always the safest choice.

## 1. My Computer Hardware

I checked the hardware available on my laptop using PowerShell.

The results were:

| Hardware | Result |
|---|---|
| System RAM | 7.73 GB |
| GPU | Intel(R) UHD Graphics |
| Reported GPU memory | 0.12 GB |

The laptop has approximately **8 GB of system RAM** and uses integrated Intel UHD Graphics rather than a dedicated high-memory GPU.

This means that the system has limited resources for running large LLMs locally.

## 2. Memory Required for Model Weights

The approximate memory required for model weights can be estimated using:

```text
Memory = Number of Parameters × Bytes per Parameter
```

For FP16, each parameter requires approximately 2 bytes.

For INT4, each parameter requires approximately 0.5 bytes.

| Model | FP16 Weight Memory | INT4 Weight Memory |
|---|---:|---:|
| 4B | ~8 GB | ~2 GB |
| 7B | ~14 GB | ~3.5 GB |

These values are approximate because real model files also contain metadata and other components.

## 3. 4B FP16 vs 4B INT4 on an 8 GB Laptop

A 4B model in FP16 would require approximately **8 GB just for its weights**.

Since my laptop has only **7.73 GB of system RAM**, an 8 GB FP16 model would leave essentially no memory for the operating system, model runtime, and other applications.

A 4B model in INT4 requires approximately **2 GB for its weights**, making it much more practical on an 8 GB system.

However, the actual memory required during inference will be higher than the weight-only estimate.

## 4. 4B INT4 vs 7B INT4

A 4B INT4 model requires approximately **2 GB** for its weights, while a 7B INT4 model requires approximately **3.5 GB**.

Therefore, the 4B INT4 model is more suitable for an 8 GB laptop because it leaves more memory available for the operating system and inference overhead.

The 7B INT4 model may still be possible on some 8 GB systems, but it leaves significantly less available memory and may result in slow or unstable inference.

## 5. Why Is More Memory Needed Besides Model Weights?

Model weights are not the only memory requirement during inference.

Additional memory may be required for:

- **KV cache** — stores information from previous tokens during generation.
- **Activations** — intermediate values produced while the model processes input.
- **Temporary tensors and buffers** — used during calculations.
- **Runtime overhead** — memory required by the inference software.
- **Operating system and other applications** — also consume system RAM.

Therefore, a model that theoretically fits into available memory based only on its weight size may still require more memory to run comfortably.

## 6. Is Quantization Always Safer?

No. Quantization is useful for reducing memory usage, but it is not always the best choice.

Quantization converts model weights from higher-precision formats into lower-precision formats. For example, FP16 weights can be converted to INT4 weights.

### Advantages of Quantization

- Reduces model memory requirements.
- Makes larger models more practical on limited hardware.
- Can reduce memory bandwidth requirements.
- Makes local inference possible on some consumer computers.

### Disadvantages of Quantization

- Some information can be lost when reducing numerical precision.
- Model accuracy or response quality can decrease, depending on the model and quantization method.
- Very aggressive quantization may produce noticeable quality degradation.
- Some hardware or software setups may not support every quantization format efficiently.

Therefore, quantization involves a **trade-off between memory usage, speed, and model quality**.

## 7. Conclusion

My laptop has approximately 8 GB of RAM and integrated Intel UHD Graphics, so running large models in high precision is not practical.

A 4B model in FP16 would require approximately 8 GB just for its weights, while a 4B INT4 model would require approximately 2 GB for its weights.

A 7B INT4 model would require approximately 3.5 GB for its weights, but additional memory would still be needed during inference.

Therefore, for an 8 GB laptop, a smaller quantized model is generally more practical than a larger high-precision model.

Quantization is useful because it reduces memory requirements, but it should be chosen carefully because reducing precision can involve a trade-off with model quality.