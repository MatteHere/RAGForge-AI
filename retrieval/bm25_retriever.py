import re
from typing import List

from rank_bm25 import BM25Okapi

from database.chunk_repository import ChunkRepository


class BM25Retriever:
    def __init__(self):
        self.chunk_repository = ChunkRepository()

    def search(self, query: str, workspace_id: int, top_k: int = 5) -> List[dict]:
        chunks = self.chunk_repository.get_chunks_by_workspace(workspace_id)

        if not chunks:
            return []

        tokenized_query = self._tokenize(query)

        if not tokenized_query:
            return []

        tokenized_corpus = [
            self._tokenize(chunk["chunk_text"])
            for chunk in chunks
        ]

        bm25 = BM25Okapi(tokenized_corpus)
        raw_scores = bm25.get_scores(tokenized_query)

        keyword_matches = [
            self._count_keyword_matches(chunk["chunk_text"], tokenized_query)
            for chunk in chunks
        ]

        ranked_results = sorted(
            zip(chunks, raw_scores, keyword_matches),
            key=lambda item: (
                item[2],
                item[1],
            ),
            reverse=True,
        )

        relevant_results = [
            (chunk, raw_score, match_count)
            for chunk, raw_score, match_count in ranked_results
            if match_count > 0
        ]

        results = []

        for chunk, raw_score, match_count in relevant_results[:top_k]:
            safe_score = self._calculate_safe_score(
                raw_score=float(raw_score),
                match_count=match_count,
            )

            results.append(
                {
                    "chunk_id": chunk["id"],
                    "document_id": chunk["document_id"],
                    "workspace_id": chunk["workspace_id"],
                    "chunk_index": chunk["chunk_index"],
                    "chunk_text": chunk["chunk_text"],
                    "token_count": chunk["token_count"],
                    "file_name": chunk["file_name"],
                    "file_type": chunk["file_type"],
                    "document_status": chunk["document_status"],
                    "score": safe_score,
                    "raw_bm25_score": float(raw_score),
                    "keyword_matches": match_count,
                    "retrieval_method": "bm25",
                }
            )

        return results

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = text.replace("-", " ")
        text = text.replace("_", " ")
        tokens = re.findall(r"[a-zA-Z0-9]+", text)
        return tokens

    def _count_keyword_matches(self, text: str, query_tokens: List[str]) -> int:
        document_tokens = set(self._tokenize(text))

        return sum(
            1
            for token in query_tokens
            if token in document_tokens
        )

    def _calculate_safe_score(self, raw_score: float, match_count: int) -> float:
        if raw_score > 0:
            return raw_score + match_count

        return float(match_count)