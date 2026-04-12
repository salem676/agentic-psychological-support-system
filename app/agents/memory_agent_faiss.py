from typing import List
import numpy as np
import faiss
import json
import os


class FAISSMemoryAgent:
    """Simple semantic memory using FAISS.

    MVP note:
    - uses deterministic toy embeddings based on hashed tokens
    - can later be replaced with OpenAI/Hugging Face embeddings
    """

    def __init__(self, dimension: int = 128, index_path: str = "faiss.index", store_path: str = "memories.json"):
        self.dimension = dimension
        self.index_path = index_path
        self.store_path = store_path
        self.memories: List[str] = []

        # we load FAISS index if it exists already
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(dimension)

        #load memory tests if they exist
        if os.path.exists(store_path):
            with open(store_path, "r", encoding = "utf-8") as f:
                self.memories = json.load(f)

    def _embed(self, text: str) -> np.ndarray:
        """Lightweight deterministic embedding for MVP development."""
        vec = np.zeros(self.dimension, dtype="float32")
        for token in text.lower().split():
            slot = hash(token) % self.dimension
            vec[slot] += 1.0

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def _persist(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.store_path, "w", encoding = "utf-8") as f:
            json.dump(self.memories, f, ensure_ascii = False, indent = 2)

    def add_memory(self, text: str):
        vector = self._embed(text).reshape(1, -1)
        self.index.add(vector)
        self.memories.append(text)
        self._persist()

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if len(self.memories) == 0:
            return []

        query_vector = self._embed(query).reshape(1, -1)
        k = min(top_k, len(self.memories))
        distances, indices = self.index.search(query_vector, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.memories):
                results.append(self.memories[idx])
        return results


# singleton instance for MVP
memory_agent = FAISSMemoryAgent()
