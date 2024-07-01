from sentence_transformers import util
import numpy as np
import torch
from app.base.embeddings import model


def semantic_search(query: str, corpus_embeddings: torch.Tensor, top_n: int = 10):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = np.argpartition(-cos_scores, range(top_n))[:top_n]
    return top_results, cos_scores
