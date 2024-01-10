import asyncio
from typing import Any, Dict, List, Optional, Sequence
from llama_index import ServiceContext, global_service_context
from llama_index.finetuning.embeddings.common import EmbeddingQAFinetuneDataset
from llama_index.prompts.mixin import PromptDictType
from llama_index.evaluation.base import BaseEvaluator, EvaluationResult
from llama_index.evaluation import RetrieverEvaluator
from llama_index.indices.base_retriever import BaseRetriever
from llama_index.evaluation.retrieval.base import (
    RetrievalEvalMode,
    RetrievalEvalResult,
)
import pandas as pd
from collections import defaultdict
from langtest.transform import TestFactory

TESTS = TestFactory.test_scenarios().get("robustness")


class Evaluator(BaseEvaluator):
    """
    Evaluator class to evaluate language models. It uses service contexts and test configurations
    for evaluation purposes.

    Attributes:
        _service_context (ServiceContext): The service context for the language model.
        _tests_config (dict): Configuration for the tests.
    """

    def __init__(
        self,
        service_context: Optional[ServiceContext] = None,
        tests_config: Optional[dict] = None,
    ) -> None:
        self._service_context = service_context or ServiceContext.from_defaults()
        self._tests_config = tests_config or {}

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        pass

    async def aevaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[str] = None,
        reference: Optional[str] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """
        Asynchronously evaluates the performance of a language model based on a given query and other parameters.

        Parameters:
        - query (Optional[str]): The query string to be evaluated.
        - response (Optional[str]): The response generated by the language model for the query.
        - contexts (Optional[str]): Additional context information that may be relevant for the evaluation.
        - reference (Optional[str]): Reference material or answer that the response can be compared against.
        - **kwargs (Any): Additional keyword arguments that can be used for extended functionality.

        Returns:
        - EvaluationResult: An object containing various metrics representing the evaluation results.
        """
        llm = self._service_context.llm_predictor

        print("Evaluating...")
        print("Query: ", query)
        print("Response: ", llm(query))
        print("Contexts: ", contexts)
        print("Reference: ", reference)
        print("kwargs: ", kwargs)
        return EvaluationResult(0.0, 0.0, 0.0, 0.0, 0.0)


class LangtestRetrieverEvaluator(RetrieverEvaluator):

    """
    A class for evaluating the performance of a retriever model against a set of test cases and configurations.

    Attributes:
    - eval_results (defaultdict(list)): Stores the evaluation results for different test types.
    - _service_context (ServiceContext): Contextual information about the service, including the model being used.
    - config (list): Configuration settings for the evaluation, such as perturbation types.

    Methods:
    - __init__(metrics, retriever, **kwargs): Initializes the evaluator with specified metrics and retriever.
    - setPerturbations(*args): Sets the types of perturbations to be used during evaluation.
    - _aget_retrieved_ids(query, mode): Asynchronously retrieves document IDs based on the query.
    - aevaluate_dataset(dataset, workers, show_progress, **kwargs): Asynchronously evaluates a dataset.
    - eval_worker(query, expected_ids, mode, workers): Worker function for handling individual evaluation tasks.
    - display_results(): Compiles and displays the results of the evaluation in a structured format.
    """

    eval_results = defaultdict(list)
    config = ["uppercase", "lowercase", "add_typo"]

    def __init__(
        self,
        metrics: Sequence[RetrieverEvaluator],
        retriever: BaseRetriever,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(metrics=metrics, retriever=retriever, **kwargs)
        self.retriever = retriever

    def setPerturbations(self, *args):
        self.config = []
        for arg in args:
            if isinstance(arg, str) and arg in TESTS.keys():
                self.config.append(arg)
            else:
                raise ValueError("Invalid perturbation type")

    async def _aget_retrieved_ids(
        self, query: str, mode: RetrievalEvalMode = RetrievalEvalMode.TEXT
    ) -> Sequence[str]:
        """Get retrieved ids."""
        retrieved_nodes = await self.retriever.aretrieve(query)
        return [node.node.node_id for node in retrieved_nodes]

    async def aevaluate_dataset(
        self,
        dataset: EmbeddingQAFinetuneDataset,
        workers: int = 2,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> Dict[str, List[RetrievalEvalResult]]:
        """Evaluate dataset."""
        response_jobs = defaultdict(list)
        mode = RetrievalEvalMode.from_str(dataset.mode)
        for query_id, query in dataset.queries.items():
            expected_ids = dataset.relevant_docs[query_id]

            # original test case
            original_response = self.eval_worker(
                query=query, expected_ids=expected_ids, mode=mode, workers=workers
            )
            response_jobs["original_query"].append(original_response)
            for test_type in self.config:
                test_case = TESTS[test_type].transform([query])
                test_case_response = self.eval_worker(
                    query=test_case[0],
                    expected_ids=expected_ids,
                    mode=mode,
                    workers=workers,
                )
                response_jobs[test_type].append(test_case_response)

        for test_type, responses in response_jobs.items():
            responses = await asyncio.gather(*responses)
            self.eval_results[test_type] = responses

        return self.eval_results

    async def eval_worker(
        self,
        query: str,
        expected_ids: List[str],
        mode: RetrievalEvalMode,
        workers: int = 2,
    ) -> RetrievalEvalResult:
        """"""
        semaphore = asyncio.Semaphore(workers)
        async with semaphore:
            return await self.aevaluate(query, expected_ids=expected_ids, mode=mode)

    def display_results(
        self,
    ):
        metric_df = []
        for test_name, results in self.eval_results.items():
            metric_dicts = []
            for eval_result in results:
                metric_dict = eval_result.metric_vals_dict
                metric_dicts.append(metric_dict)

            full_df = pd.DataFrame(metric_dicts)

            hit_rate = full_df["hit_rate"].mean()
            mrr = full_df["mrr"].mean()

            metric_df.append(
                {
                    "Retriever Model": global_service_context.embed_model.model_name,
                    "Test Type": test_name,
                    "Hit Rate": hit_rate,
                    "MRR": mrr,
                }
            )

        final_df = pd.DataFrame(metric_df)

        return final_df
