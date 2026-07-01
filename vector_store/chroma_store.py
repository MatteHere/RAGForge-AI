from pathlib import Path
from typing import List

import chromadb


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "storage" / "chroma"


class ChromaStore:
    def __init__(self, collection_name: str = "ragforge_chunks"):
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict],
    ) -> None:
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        workspace_id: int | None = None,
    ) -> dict:
        where_filter = None

        if workspace_id is not None:
            where_filter = {"workspace_id": workspace_id}

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
        )

    def delete_by_document(self, document_id: int) -> None:
        self.collection.delete(
            where={"document_id": document_id}
        )