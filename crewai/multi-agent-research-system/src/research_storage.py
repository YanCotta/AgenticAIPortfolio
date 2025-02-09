import faiss
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ResearchStorage:
    def __init__(self, dimension: int, index_path: str = "research.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = self._load_or_create_index()

    def _load_or_create_index(self):
        try:
            index = faiss.read_index(self.index_path)
            logger.info(f"Loaded existing FAISS index from {self.index_path}")
            return index
        except RuntimeError:
            logger.info("Creating a new FAISS index")
            index = faiss.IndexFlatL2(self.dimension)
            return index

    def add_data(self, data: List[Dict[str, str]]):
        vectors = [self._create_vector(item["content"]) for item in data]
        vectors = np.array(vectors).astype('float32')
        self.index.add(vectors)
        faiss.write_index(self.index, self.index_path)
        logger.info(f"Added {len(data)} items to FAISS index and saved to {self.index_path}")

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, str]]:
        query_vector = self._create_vector(query).reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        # Assuming you have a way to map indices back to original data
        # This is a placeholder, replace with your actual data retrieval logic
        for i in range(len(indices[0])):
            index = indices[0][i]
            distance = distances[0][i]
            results.append({"index": int(index), "distance": float(distance)})
        return results

    def _create_vector(self, text: str) -> np.ndarray:
        # Placeholder for embedding creation
        # Replace with actual embedding model
        return np.random.rand(self.dimension)
    
    #
