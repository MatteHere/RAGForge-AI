from database.chunk_repository import ChunkRepository
from database.document_repository import DocumentRepository
from retrieval.text_chunker import TextChunker


class ChunkService:
    def __init__(self):
        self.chunk_repository = ChunkRepository()
        self.document_repository = DocumentRepository()
        self.text_chunker = TextChunker()

    def chunk_document(self, document_id: int) -> int:
        document = self.document_repository.get_document_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if document.status != "parsed":
            raise ValueError("Document must be parsed before chunking.")

        if not hasattr(document, "extracted_text") or not document.extracted_text:
            raise ValueError("Document has no extracted text.")

        self.chunk_repository.delete_chunks_by_document(document_id)

        chunks = self.text_chunker.chunk_text(document.extracted_text)

        for chunk in chunks:
            self.chunk_repository.create_chunk(
                document_id=document.id,
                workspace_id=document.workspace_id,
                chunk_index=chunk.chunk_index,
                chunk_text=chunk.chunk_text,
                token_count=chunk.token_count,
            )

        self.document_repository.update_document_status(
            document_id=document_id,
            status="chunked",
        )

        return len(chunks)

    def count_chunks(self) -> int:
        return self.chunk_repository.count_chunks()