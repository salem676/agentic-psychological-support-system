from typing import List
import numpy as np
import faiss
import json
import os


class MultiUserFAISSMemoryAgent:
    """Persistent FAISS memory with one isolated store per user.

    Each user gets:
    - <user_id>.index  (vector store)
    - <user_id>.json   (raw memory text)
    """

    def __init__(self, dimension: int = 128, base_path: str = "memory_store"):
        self.dimension = dimension
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def _paths(self, user_id: str):
        safe_user = str(user_id).replace("/", "_").replace("\\", "_")
        index_path = os.path.join(self.base_path, f"{safe_user}.index")
        store_path = os.path.join(self.base_path, f"{safe_user}.json")
        return index_path, store_path

    def _load_user_store(self, user_id: str):
        index_path, store_path = self._paths(user_id)

        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
        else:
            index = faiss.IndexFlatL2(self.dimension)

        if os.path.exists(store_path):
            with open(store_path, "r", encoding="utf-8") as f:
                memories = json.load(f)
        else:
            memories = []

        return index, memories, index_path, store_path

    def _embed(self, text: str) -> np.ndarray:
        vec = np.zeros(self.dimension, dtype="float32")

        for token in text.lower().split():
            slot = hash(token) % self.dimension
            vec[slot] += 1.0

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        return vec

    def _persist(self, index, memories, index_path: str, store_path: str):
        faiss.write_index(index, index_path)
        with open(store_path, "w", encoding="utf-8") as f:
            json.dump(memories, f, ensure_ascii=False, indent=2)

    def add_memory(self, user_id: str, text: str):
        index, memories, index_path, store_path = self._load_user_store(user_id)

        vector = self._embed(text).reshape(1, -1)
        index.add(vector)
        memories.append(text)

        self._persist(index, memories, index_path, store_path)

    def search(self, user_id: str, query: str, top_k: int = 3) -> List[str]:
        index, memories, _, _ = self._load_user_store(user_id)

        if len(memories) == 0:
            return []

        query_vector = self._embed(query).reshape(1, -1)
        k = min(top_k, len(memories))

        distances, indices = index.search(query_vector, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(memories):
                results.append(memories[idx])

        return results


memory_agent = MultiUserFAISSMemoryAgent()
