from database.chunk_repository import ChunkRepository
from vector_store.chroma_store import ChromaStore
from vector_store.embedding_service import EmbeddingService
from vector_store.faiss_store import FAISSStore


class IndexingService:
    def __init__(self):
        self.chunk_repository = ChunkRepository()
        self.embedding_service = EmbeddingService()
        self.chroma_store = ChromaStore()
        self.faiss_store = FAISSStore()

    def index_workspace(self, workspace_id: int) -> int:
        chunks = self.chunk_repository.get_chunks_by_workspace(workspace_id)

        if not chunks:
            raise ValueError("No chunks found for this workspace.")

        chunk_texts = [chunk["chunk_text"] for chunk in chunks]

        embeddings = self.embedding_service.embed_texts(chunk_texts)

        ids = [f"chunk_{chunk['id']}" for chunk in chunks]

        metadatas = [
            {
                "chunk_id": chunk["id"],
                "document_id": chunk["document_id"],
                "workspace_id": chunk["workspace_id"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        self.chroma_store.add_chunks(
            ids=ids,
            texts=chunk_texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        self.faiss_store.add_embeddings(embeddings)

        return len(chunks)