from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def load_embedding_model(model_name: str):
    return SentenceTransformer(model_name)


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = load_embedding_model(model_name)

    def embed_text(self, text: str) -> List[float]:
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()