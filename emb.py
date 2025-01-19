from sentence_transformers import SentenceTransformer
import torch

class EmbeddingFunction:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:

        embeddings = self.model.encode(
            texts, convert_to_tensor=False, device=self.device
        )
        return embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings

    def embed_query(self, text: str) -> list[float]:

        embedding = self.model.encode(
            text, convert_to_tensor=False, device=self.device
        )
        return embedding.tolist() if hasattr(embedding, "tolist") else embedding
