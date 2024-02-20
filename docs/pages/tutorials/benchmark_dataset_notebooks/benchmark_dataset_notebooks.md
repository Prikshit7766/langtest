---
layout: docs
header: true
seotitle: Tutorials | Benchmark Notebooks | LangTest | John Snow Labs
title: Benchmark Dataset Notebooks
key: docs-benchmark_dataset_notebook
permalink: /docs/pages/tutorials/benchmark_dataset_notebooks/
sidebar:
    nav: tutorials
aside:
    toc: true
nav_key: tutorials
show_edit_on_github: true
modify_date: "2019-05-16"
---

<div class="main-docs" markdown="1"><div class="h3-box" markdown="1">
The following table provides an overview of various Benchmark Dataset notebooks. User can select from a list of benchmark datasets provided below to test their LLMs.

</div><div class="h3-box" markdown="1">

{:.table2}
| Tutorial Description                | Hub                           | Task                              | Open In Colab                                                                                                                                                                                                                                    |
| ----------------------------------- |
| [**OpenbookQA**](/docs/pages/benchmarks/commonsense_scenario/openbookqa): Evaluate your model's ability to answer questions that require complex reasoning and inference based on general knowledge, similar to an "open-book" exam.                          | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/OpenbookQA_dataset.ipynb)                   |
| [**Quac**](/docs/pages/benchmarks/other_benchmarks/quac) : Evaluate your model's ability to answer questions given a conversational context, focusing on dialogue-based question-answering.                                | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/quac_dataset.ipynb)                         |
| [**MMLU**](/docs/pages/benchmarks/other_benchmarks/mmlu) : Evaluate language understanding models' performance in different domains. It covers 57 subjects across STEM, the humanities, the social sciences, and more.                                | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/mmlu_dataset.ipynb)                         |
| [**TruthfulQA**](/docs/pages/benchmarks/other_benchmarks/truthfulqa/): Evaluate the model's capability to answer questions accurately and truthfully based on the provided information.                          | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/TruthfulQA_dataset.ipynb)                   |
| [**NarrativeQA**](/docs/pages/benchmarks/other_benchmarks/narrativeqa): Evaluate your model's ability to comprehend and answer questions about long and complex narratives, such as stories or articles.                         | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/NarrativeQA_Question_Answering.ipynb)       |
| [**HellaSWag**](/docs/pages/benchmarks/commonsense_scenario/hellaswag): Evaluate your model's ability in completions of sentences.                           | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/HellaSwag_Question_Answering.ipynb)         |
| [**BBQ**](/docs/pages/benchmarks/other_benchmarks/bbq): Evaluate how your model responds to questions in the presence of social biases against protected classes across various social dimensions.                                 | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/BBQ_dataset.ipynb)                          |
| [**NQ open**](/docs/pages/benchmarks/other_benchmarks/nq-open): Evaluate the ability of your model to answer open-ended questions based on a given passage or context.                             | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/NQ_open_dataset.ipynb)                      |
| [**BoolQ**](/docs/pages/benchmarks/other_benchmarks/boolq): Evaluate the ability of your model to answer boolean questions (yes/no) based on a given passage or context.                               | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/BoolQ_dataset.ipynb)                        |
| [**XSum**](/docs/pages/benchmarks/other_benchmarks/xsum) : Evaluate your model's ability to generate concise and informative summaries for long articles with the XSum dataset. | OpenAI                            | Summarization                     | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/XSum_dataset.ipynb)                         |
| [**LogiQA**](/docs/pages/benchmarks/other_benchmarks/logiqa): Evaluate your model's accuracy on Machine Reading Comprehension with Logical Reasoning questions.                             | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/LogiQA_dataset.ipynb)                       |
| [**ASDiv**](/docs/pages/benchmarks/other_benchmarks/asdiv): Evaluate your model's ability answer questions based on Math Word Problems.                                | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/ASDiv_dataset.ipynb)                        |
| [**BigBench**](/docs/pages/benchmarks/other_benchmarks/bigbench): Evaluate your model's performance on BigBench datasets by Google.                            | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/Bigbench_dataset.ipynb)                     |
| [**MultiLexSum**](/docs/pages/benchmarks/legal/multilexsum): Evaluate your model's ability to generate concise and informative summaries for legal case contexts from the Multi-LexSum dataset                         | OpenAI                            | Summarization                     | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/MultiLexSum_dataset.ipynb)                  |
| [**Legal-QA**](/docs/pages/benchmarks/legal): Evaluate your model's performance on legal-qa datasets                            | OpenAI                            | Legal-Tests                       | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/LegalQA_Datasets.ipynb)                     |
| [**CommonSenseQA**](/docs/pages/benchmarks/commonsense_scenario/commonsenseqa): Evaluate your model's performance on the CommonsenseQA dataset                       | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/CommonsenseQA_dataset.ipynb)                |
| [**SIQA**](/docs/pages/benchmarks/commonsense_scenario/siqa): Evaluate your model's performance by assessing its accuracy in understanding social situations.                                | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/SIQA_dataset.ipynb)                         |
| [**PIQA**](/docs/pages/benchmarks/commonsense_scenario/piqa): Evaluate your model's performance on the PIQA dataset, which tests its ability to reason about everyday physical situations                               | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/PIQA_dataset.ipynb)                         |
| [**Fiqa**](/docs/pages/benchmarks/legal/fiqa): Evaluate your model's performance on the FiQA dataset, a comprehensive and specialized resource designed for finance-related question-answering tasks                         | OpenAI                     | Question-Answering                       | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/Fiqa_dataset.ipynb)  |
| [**LiveQA**](/docs/pages/benchmarks/medical/liveqa): Evaluate your model's performance on the Medical Question Answering Task at TREC 2017 LiveQA                                | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/Medical_Datasets.ipynb)                         |
| [**MedicationQA**](/docs/pages/benchmarks/medical/medicationqa): Evaluate your model's performance on the MedicationQA dataset, Bridging the Gap Between Consumers' Medication Questions and Trusted Answers                               | OpenAI                            | Question-Answering                | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/Medical_Datasets.ipynb)                         |
| [**HealthSearchQA**](/docs/pages/benchmarks/medical/healthsearchqa): Evaluate your model's performance on the HealthSearchQA dataset, a Large Language Models Encode Clinical Knowledge question-answering tasks                         | OpenAI                     | Question-Answering                       | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnSnowLabs/langtest/blob/main/demo/tutorials/llm_notebooks/dataset-notebooks/Medical_Datasets.ipynb)  |
