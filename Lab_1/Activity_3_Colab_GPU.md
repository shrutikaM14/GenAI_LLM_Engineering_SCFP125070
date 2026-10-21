# Lab 1 — Activity 3: Colab GPU

## Objective

The objective of this activity is to understand how a GPU can be used to run an LLM or other machine learning model in Google Colab.

In this activity, I will examine:

- Whether the Colab GPU is actually being used.
- How much GPU memory is available.
- What happens when the output length is increased.
- Whether a laptop without a dedicated GPU can run the same model locally.

## 1. Checking the Colab GPU

I enabled a GPU runtime in Google Colab and used PyTorch to check whether CUDA was available.

The results were:

```text
PyTorch version: 2.11.0+cu130
CUDA available: True
GPU: Tesla T4
GPU memory: 14.56 GB