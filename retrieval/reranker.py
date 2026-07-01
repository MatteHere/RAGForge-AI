from functools import lru_cache
from typing import List

from sentence_transformers import CrossEncoder


@lru_cache(maxsize=1)
def load_reranker_model(model_name: str):
    return CrossEncoder(model_name)


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.model = load_reranker_model(model_name)

    def rerank(
        self,
        query: str,
        results: List[dict],
        top_k: int = 5,
    ) -> List[dict]:
        if not query.strip() or not results:
            return []

        pairs = [[query, result["chunk_text"]] for result in results]
        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(results, scores):
            updated_result = result.copy()
            updated_result["reranker_score"] = float(score)
            updated_result["retrieval_method"] = f'{result["retrieval_method"]}+rerank'
            reranked_results.append(updated_result)

        reranked_results.sort(
            key=lambda item: item["reranker_score"],
            reverse=True,
        )

        return reranked_results[:top_k]