# Lab 1 — Activity 6: API and Inference Providers

## Objective

The objective of this activity is to understand how an application communicates with an LLM through an API or inference provider.

## 1. What Happens Between My Program and the Model?

When a program uses an LLM through an API, the program sends a request to a remote server.

The general process is:

```text
My Python Program
       ↓
     API Request
       ↓
Inference Provider
       ↓
    LLM Model
       ↓
Generated Response
       ↓
     API Response
       ↓
My Python Program

The request usually contains information such as the model name, user prompt, and other parameters.

The inference provider processes the request using its servers and sends the generated response back to the application.

## 2. Who Pays for the Compute?

When using a cloud-based inference API, the inference provider is responsible for providing the computing hardware.

The provider has to pay for resources such as:

- GPUs or other accelerators
- Servers
- Electricity
- Storage
- Networking
- Infrastructure and maintenance

Depending on the service, the user may be charged based on the number of tokens, requests, or amount of compute used.

Some providers also offer free usage within certain limits.

## 3. Local Inference vs Cloud API

| Feature | Local Inference | Cloud API |
|---|---|---|
| Where model runs | My computer | Provider's servers |
| Internet required | Usually not after model download | Yes |
| Hardware requirement | Depends on model size | Mostly handled by provider |
| Privacy | More control over data | Data is sent to provider |
| Scalability | Limited by local hardware | Easier to scale |
| Cost | Hardware/electricity cost | Usually usage-based |
| Setup | Requires model and software setup | Usually easier to start |

## 4. Advantages of Local Inference

Local inference can provide:

- Better control over data.
- Ability to work without an internet connection after the model is downloaded.
- No per-request API charges.
- Greater control over the model and inference environment.

However, local inference requires suitable hardware and can be slow for large models.

## 5. Advantages of Cloud APIs

Cloud APIs provide:

- Access to powerful computing hardware.
- Easier access to large models.
- Better scalability.
- No need to maintain a powerful local GPU.
- Easier integration into applications.

The main disadvantages are dependence on internet connectivity, possible usage costs, and sending prompts to an external service.

## 6. Conclusion

An API provides a communication layer between an application and an inference provider.

With local inference, the model runs on my own computer, giving me greater control over data but requiring suitable hardware.

With a cloud API, the model runs on the provider's servers. This makes powerful models easier to access and scale, but it introduces internet dependency, possible costs, and privacy considerations.

For a computer with limited hardware, a cloud API can be more practical for running larger models.