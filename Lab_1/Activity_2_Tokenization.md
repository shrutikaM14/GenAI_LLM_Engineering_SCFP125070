# Lab 1 — Activity 2: Tokenization

## Objective

The objective of this activity is to understand how text is converted into tokens before being processed by a Large Language Model (LLM).

In this activity, I will examine how a sentence, individual words, and phrases are tokenized and answer the following questions:

- Is one word always equal to one token?
- Why do LLMs split text into tokens?
- How are punctuation marks handled?
- Why are token IDs used?

## 1. Tokenizing a Sentence

I used the `cl100k_base` tokenizer from the `tiktoken` library.

The sentence used was:

> Hello, how are you today?

The tokenizer produced:

```text
Token IDs: [9906, 11, 1268, 527, 499, 3432, 30]
Number of tokens: 7
Tokens: ['Hello', ',', ' how', ' are', ' you', ' today', '?']

## 3. Why Do LLMs Split Text into Tokens?

LLMs cannot directly process raw human language as text. They process numerical representations.

Tokenization converts text into smaller pieces called **tokens**. These tokens can be complete words, parts of words, punctuation marks, or spaces combined with text.

Splitting text into tokens has several advantages:

1. **Handles unknown and rare words**  
   A word that is not commonly present in the vocabulary can be divided into smaller pieces instead of being treated as completely unknown.

2. **Reduces vocabulary size**  
   The tokenizer does not need a separate token for every possible word.

3. **Handles different word forms**  
   Related words can share token pieces. For example, `tokenization` was split into `token` and `ization`.

4. **Handles punctuation and special characters**  
   Characters such as commas, periods, and question marks can also be represented as tokens.

5. **Works across different types of text**  
   The same approach can handle words, numbers, punctuation, and parts of unfamiliar words.

## 4. Why Are Token IDs Used?

After tokenization, each token is converted into a numerical **token ID**.

For example:

```text
"Hello" → 9906
","     → 11
" how"  → 1268

## 5. How Is Punctuation Handled?

Punctuation marks can be represented as separate tokens.

For example, in the sentence:

```text
Hello, how are you today?