from typing import Dict, List

from retrieval.bm25_retriever import BM25Retriever
from retrieval.vector_retriever import VectorRetriever


class HybridRetriever:
    def __init__(self):
        self.bm25_retriever = BM25Retriever()
        self.vector_retriever = VectorRetriever()

    def search(self, query: str, workspace_id: int, top_k: int = 5) -> List[dict]:
        bm25_results = self.bm25_retriever.search(
            query=query,
            workspace_id=workspace_id,
            top_k=top_k,
        )

        vector_results = self.vector_retriever.search(
            query=query,
            workspace_id=workspace_id,
            top_k=top_k,
        )

        fused_results = self._reciprocal_rank_fusion(
            bm25_results=bm25_results,
            vector_results=vector_results,
        )

        return fused_results[:top_k]

    def _reciprocal_rank_fusion(
        self,
        bm25_results: List[dict],
        vector_results: List[dict],
        k: int = 60,
    ) -> List[dict]:
        fused_scores: Dict[int, float] = {}
        result_map: Dict[int, dict] = {}

        self._add_results_to_fusion(
            results=bm25_results,
            fused_scores=fused_scores,
            result_map=result_map,
            source="bm25",
            k=k,
        )

        self._add_results_to_fusion(
            results=vector_results,
            fused_scores=fused_scores,
            result_map=result_map,
            source="vector",
            k=k,
        )

        ranked_chunk_ids = sorted(
            fused_scores.keys(),
            key=lambda chunk_id: fused_scores[chunk_id],
            reverse=True,
        )

        fused_results = []

        for chunk_id in ranked_chunk_ids:
            result = result_map[chunk_id]
            result["score"] = fused_scores[chunk_id]
            result["retrieval_method"] = "hybrid"
            result["retrieval_sources"] = result.get("retrieval_sources", [])

            fused_results.append(result)

        return fused_results

    def _add_results_to_fusion(
        self,
        results: List[dict],
        fused_scores: Dict[int, float],
        result_map: Dict[int, dict],
        source: str,
        k: int,
    ) -> None:
        for rank, result in enumerate(results, start=1):
            chunk_id = result["chunk_id"]

            if chunk_id not in fused_scores:
                fused_scores[chunk_id] = 0.0

            fused_scores[chunk_id] += 1 / (k + rank)

            if chunk_id not in result_map:
                result_map[chunk_id] = result.copy()
                result_map[chunk_id]["retrieval_sources"] = []

            result_map[chunk_id]["retrieval_sources"].append(source)