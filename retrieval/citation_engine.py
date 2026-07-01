from typing import List


class CitationEngine:
    def build_citations(self, sources: List[dict]) -> List[dict]:
        citations = []

        for index, source in enumerate(sources, start=1):
            citations.append(
                {
                    "citation_id": index,
                    "document_id": source.get("document_id"),
                    "file_name": source.get("file_name", "Unknown Document"),
                    "file_type": source.get("file_type", ""),
                    "chunk_index": source.get("chunk_index"),
                    "chunk_text": source.get("chunk_text", ""),
                    "retrieval_method": source.get("retrieval_method", ""),
                }
            )

        return citations

    def format_citation_label(self, citation: dict) -> str:
        return f"[Source {citation['citation_id']}: {citation['file_name']} • Chunk {citation['chunk_index']}]"

    def enforce_citations(self, answer: str, citations: List[dict]) -> str:
        if not citations:
            return answer

        citation_labels = [
            self.format_citation_label(citation)
            for citation in citations
        ]

        citation_block = "\n\nSources:\n" + "\n".join(citation_labels)

        return answer.strip() + citation_block