from typing import List

from vector_store.chroma_store import ChromaStore
from vector_store.embedding_service import EmbeddingService


class VectorRetriever:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chroma_store = ChromaStore()

    def search(self, query: str, workspace_id: int, top_k: int = 5) -> List[dict]:
        if not query.strip():
            return []

        query_embedding = self.embedding_service.embed_text(query)

        raw_results = self.chroma_store.query(
            query_embedding=query_embedding,
            top_k=top_k,
            workspace_id=workspace_id,
        )

        results = []

        ids = raw_results.get("ids", [[]])[0]
        documents = raw_results.get("documents", [[]])[0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        distances = raw_results.get("distances", [[]])[0]

        for index, chunk_id in enumerate(ids):
            distance = distances[index] if index < len(distances) else 0.0
            similarity_score = 1 / (1 + distance)

            metadata = metadatas[index]
            chunk_text = documents[index]

            results.append(
                {
                    "chunk_id": metadata["chunk_id"],
                    "document_id": metadata["document_id"],
                    "workspace_id": metadata["workspace_id"],
                    "chunk_index": metadata["chunk_index"],
                    "chunk_text": chunk_text,
                    "score": float(similarity_score),
                    "retrieval_method": "vector",
                    "vector_id": chunk_id,
                }
            )

        return results