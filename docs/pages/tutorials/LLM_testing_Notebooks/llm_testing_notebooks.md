---
layout: docs
header: true
seotitle: Tutorials | LLM Testing | LangTest | John Snow Labs
title: LLM Testing Notebooks
key: docs-llm_testing_notebooks
permalink: /docs/pages/tutorials/llm_testing_notebooks/
sidebar:
    nav: tutorials
aside:
    toc: true
nav_key: tutorials
show_edit_on_github: true
modify_date: "2019-05-16"
---

<div class="main-docs" markdown="1"><div class="h3-box" markdown="1">
The following table gives an overview of the different tutorial notebooks to test various LLMs. We've got a bunch of tests to try out on Large Language Models, like Question-Answering, Summarization, Sycophancy, Clinical, Gender-Bias, and plenty more. Please refer the below table for more options.

</div><div class="h3-box" markdown="1">

{:.table2}
| Tutorial Description                | Hub                           | Task                              | Open In Colab                                                                                                                                                                                                                                    |
| ----------------------------------- |
| [**OpenAI QA/Summarization**](QA_Sum) :OpenAI Model Testing For Question Answering and Summarization                 | OpenAI                            | Question-Answering/Summarization  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/OpenAI_QA_Summarization_Testing_Notebook.ipynb)               |
|  [**AI21 QA/Summarization**](QA_Sum) : Ai21 Model Testing For Question Answering and Summarization                 | AI21                              | Question-Answering/Summarization  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/AI21_QA_Summarization_Testing_Notebook.ipynb)                 |
|  [**Cohere QA/Summarization**](QA_Sum)  : Cohere Model Testing For Question Answering and Summarization                 | Cohere                            | Question-Answering/Summarization  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Cohere_QA_Summarization_Testing_Notebook.ipynb)               |
|  [**Hugging Face Inference API   QA/Summarization**](QA_Sum) : Hugging Face Inference API Model Testing For Question Answering and Summarization                 | Hugging Face Inference API        | Question-Answering/Summarization  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/HuggingFaceAPI_QA_Summarization_Testing_Notebook.ipynb)       |
|  [**Hugging Face Hub   QA/Summarization**](QA_Sum)  : Hugging Face Hub Model Testing For Question Answering and Summarization                 | Hugging Face Hub                  | Question-Answering/Summarization  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/HuggingFaceHub_QA_Summarization_Testing_Notebook.ipynb)       |
|  [**Azure-OpenAI QA/Summarization**](QA_Sum) : Azure-OpenAI Model Testing For Question Answering and Summarization                 | Azure-OpenAI                      | Question-Answering/Summarization  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Azure_OpenAI_QA_Summarization_Testing_Notebook.ipynb)         |
| [**Toxicity**](toxicity) : Evaluating `gpt-3.5-turbo-instruct` model on toxicity test                       | OpenAI                            | Text-Generation                           | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Toxicity_NB.ipynb)                                            |
| [**Clinical**](clinical) : Assess any demographic bias the model might exhibit when suggesting treatment plans for two patients with identical diagnoses.             | OpenAI                            | Text-Generation                    | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Clinical_Tests.ipynb)                                         |
| [**Ideology**](ideology) : Evaluating the model in capturing nuanced political beliefs beyond the traditional left-right spectrum.                     | OpenAI                            |        Question-Answering                   | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/test-specific-notebooks/Political_Demo.ipynb)                               |
| [**Disinformation**](disinformation) :In this tutorial, we assess the model's capability to generate disinformation.                       | AI21                              | Text-Generation              | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Disinformation.ipynb)                                    |
|  [**Factuality**](factuality): In this tutorial, we assess how well LLMs can identify the factual accuracy of summary sentences. This is essential in ensuring that LLMs generate summaries that are consistent with the information presented in the source article.                    | OpenAI                            | Question-Answering                         | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Factuality.ipynb)                                        |
| [**Legal**](legal_tests): In this tutorial, we assess the model on LegalSupport dataset. Each sample consists of a text passage making a legal claim, and two case summaries.                      | OpenAI                            | Question-Answering                    | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Legal_Support.ipynb)                                          |
|  [**Security**](security): In this tutorial, we assess the prompt injection vulnerabilities in LLMs. It evaluates the model’s resilience against adversarial attacks and assess its ability to handle sensitive information appropriately.          | OpenAI                            | Text-Generation                          | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Prompt_Injections.ipynb)                                |
| [**Sensitivity**](sensitivity): In this tutorial, we assess the model sensitivity by adding negation and toxic words to see analyze the behaviour in the LLM response.                    | OpenAI                            | Question-Answering                  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Sensitivity.ipynb)                                       |
| [**Sycophancy**](sycophancy) : It is an undesirable behavior in which models tailor their responses to align with a human user's view, even when that view is not objectively correct. In this notebook, we propose a simple synthetic data intervention to reduce this behavior in language models.                      | OpenAI                            | Question-Answering                          | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Sycophancy.ipynb)                                        |
| [**Stereotype**](stereotype): In this tutorial, we assess the model on gender occupational stereotype statements.                         | OpenAI/AI21                      | Question-Answering                      | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/Wino_Bias_LLM.ipynb)                         |
| [**LM Studio**](lm_studio): Running Hugging Face quantized models through LM-Studio and testing these models for a Question Answering task.                         | LM Studio                      | Question-Answering                      | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/LM-Studio-Demo.ipynb)                         |
| [**Question Answering Benchmarking**](question_answering_benchmarking): This notebook provides a demo on benchmarking Language Models (LLMs) for Question-Answering tasks.   |  Hugging Face Inference API         | Question-Answering                          | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/benchmarks/Question-Answering.ipynb)  |