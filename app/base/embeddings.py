from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def get_corpus_embeddings(corpus: list):
    return model.encode(corpus, convert_to_tensor=True)


def get_embeddings(text: str):
    return model.encode(text).tolist()
