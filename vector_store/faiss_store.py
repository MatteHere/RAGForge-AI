from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
FAISS_DIR = BASE_DIR / "storage" / "faiss"
FAISS_INDEX_PATH = FAISS_DIR / "ragforge.index"


class FAISSStore:
    def __init__(self, dimension: int = 384):
        FAISS_DIR.mkdir(parents=True, exist_ok=True)

        self.dimension = dimension

        if FAISS_INDEX_PATH.exists():
            self.index = faiss.read_index(str(FAISS_INDEX_PATH))
        else:
            self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings: List[List[float]]) -> None:
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.save()

    def search(self, query_embedding: List[float], top_k: int = 5) -> Tuple[List[float], List[int]]:
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        return distances[0].tolist(), indices[0].tolist()

    def save(self) -> None:
        faiss.write_index(self.index, str(FAISS_INDEX_PATH))