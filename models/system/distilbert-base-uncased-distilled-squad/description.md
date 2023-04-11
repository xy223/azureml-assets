The DistilBERT model is a distilled version of the BERT language model with 40% fewer parameters, 60% faster run time, but with 95% of BERT's performance. It is trained for question answering and has a F1 score of 87.1 on SQuAD V1.1. The model is licensed under the Apache 2.0 license and is developed by Hugging Face. The model is based on the Transformer architecture and trained in English. However, it's output should not be used to create hostile or alienating environments or produce false/biased content. Training the model requires 8 16GB V100 GPUs and 90 hours. The model card authors are from the Hugging Face team.

> The above summary was generated using ChatGPT. Review the [original model card](https://huggingface.co/distilbert-base-uncased-distilled-squad) to understand the data used to train the model, evaluation metrics, license, intended uses, limitations and bias before using the model.

### Inference samples

Inference type|Python sample (Notebook)|CLI with YAML
|--|--|--|
Real time|[question-answering-online-endpoint.ipynb](https://aka.ms/azureml-infer-online-sdk-question-answering)|[question-answering-online-endpoint.sh](https://aka.ms/azureml-infer-online-cli-question-answering)
Batch | coming soon


### Finetuning samples

Task|Use case|Dataset|Python sample (Notebook)|CLI with YAML
|---|--|--|--|--|
Text Classification|Emotion Detection|[Emotion](https://huggingface.co/datasets/dair-ai/emotion)|[emotion-detection.ipynb](https://aka.ms/azureml-ft-sdk-emotion-detection)|[emotion-detection.sh](https://aka.ms/azureml-ft-cli-emotion-detection)
Token Classification|Token Classification|[Conll2003](https://huggingface.co/datasets/conll2003)|[token-classification.ipynb](https://aka.ms/azureml-ft-sdk-token-classification)|[token-classification.sh](https://aka.ms/azureml-ft-cli-token-classification)
Question Answering|Extractive Q&A|[SQUAD (Wikipedia)](https://huggingface.co/datasets/squad)|[extractive-qa.ipynb](https://aka.ms/azureml-ft-sdk-extractive-qa)|[extractive-qa.sh](https://aka.ms/azureml-ft-cli-extractive-qa)


### Model Evaluation

|Task|Use case|Dataset|Python sample (Notebook)|
|---|--|--|--|
|Question Answering|Extractive Q&A|[Squad v2](https://huggingface.co/datasets/squad_v2)|[evaluate-model-question-answering.ipynb](https://aka.ms/azureml-eval-sdk-question-answering)|**


#### Sample input
```json
{
    "inputs": {
        "question": ["What is my name?", "Where do I live?"],
        "context": ["My name is John and I live in Seattle.", "My name is Ravi and I live in Hyderabad."]
    }
}
```

#### Sample output
```json
[
    {
        "score": 0.9875025749206543,
        "start": 11,
        "end": 15,
        "answer": "John"
    },
    {
        "score": 0.9459660053253174,
        "start": 30,
        "end": 39,
        "answer": "Hyderabad"
    }
]
```