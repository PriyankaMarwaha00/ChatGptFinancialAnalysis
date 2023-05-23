import json
from sentence_transformers import SentenceTransformer, util


class SearchModel:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.fitted = False
        self.file_path = None

    def fit(self, corpus, n_neighbors=5):
        self.corpus = corpus
        embeddings = self.embedder.encode(corpus, convert_to_tensor=True)
        self.corpus_embeddings = util.normalize_embeddings(embeddings)
        self.fitted = True
        self.n_neighbors = n_neighbors

    def __call__(self, query):
        query_embeddings = self.embedder.encode([query], convert_to_tensor=True)
        query_embeddings = util.normalize_embeddings(query_embeddings)
        hits = util.semantic_search(
            query_embeddings,
            self.corpus_embeddings,
            top_k=self.n_neighbors,
            score_function=util.dot_score,
        )
        hits_ls = hits[0]
        output_ls = []
        for hit_d in hits_ls:
            output_ls.append(self.corpus[hit_d["corpus_id"]])
        return output_ls


def text_to_chunks(texts):
    word_length = 256
    text_tokens = [text.split(" ") for text in texts]
    chunks = []

    for idx, words in enumerate(text_tokens):
        i = 0
        while i < len(words):
            chunk = words[i : i + word_length]
            remaining = len(words) - (i + word_length)
            if remaining < word_length and remaining > 0 and idx + 1 < len(text_tokens):
                text_tokens[idx + 1] = chunk + text_tokens[idx + 1]
                break
            chunk_str = " ".join(chunk).strip()
            formatted_chunk = f'[{idx}] "{chunk_str}"'
            chunks.append(formatted_chunk)
            i += word_length
    return chunks


def load_searching_model(searching_model, file_path):
    print(file_path)
    print(searching_model.file_path)
    if searching_model.file_path == file_path:
        return searching_model

    with open(file_path, "r") as f:
        texts = json.load(f)
    chunks = text_to_chunks(texts)
    searching_model.fit(chunks)
    searching_model.file_path = file_path
    print("Corpus Loaded")
    return searching_model
