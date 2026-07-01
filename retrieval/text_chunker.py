import re
from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class TextChunk:
    chunk_index: int
    chunk_text: str
    token_count: int


class TextChunker:
    def __init__(self, chunk_size: int = 900, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[TextChunk]:
        cleaned_text = self._clean_text(text)

        if not cleaned_text:
            return []

        sentences = self._split_into_sentences(cleaned_text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk.strip())
                current_chunk = self._create_overlap(current_chunk) + " " + sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return [
            TextChunk(
                chunk_index=index,
                chunk_text=chunk,
                token_count=self._estimate_token_count(chunk),
            )
            for index, chunk in enumerate(chunks)
        ]

    def _clean_text(self, text: str) -> str:
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def _create_overlap(self, text: str) -> str:
        if len(text) <= self.chunk_overlap:
            return text

        return text[-self.chunk_overlap:]

    def _estimate_token_count(self, text: str) -> int:
        return max(1, len(text.split()))