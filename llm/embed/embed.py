import mlx.core as mx
import numpy as np
from model import Bert, load_model


def embed(batch):
    model, tokenizer = load_model(
        "bert-base-uncased",
        "weights/bert-base-uncased.npz")
    tokens = tokenizer(batch, return_tensors="np", padding=True)
    tokens = {key: mx.array(v) for key, v in tokens.items()}
    _, pooled = model(**tokens)
    pooled = np.array(pooled)
    return pooled

def get_token_length(chunk):
    _, tokenizer = load_model(
        "bert-base-uncased",
        "/Users/daniel/Desktop/course_qa/llm/embed/weights/bert-base-uncased.npz")

    print('Loaded model and getting number of tokens')
    tokens = tokenizer(chunk, return_tensors="np", padding=True)
    tokens = {key: mx.array(v) for key, v in tokens.items()}
    print('Finished getting number of tokens: ', tokens['input_ids'].shape[1])
    return tokens['input_ids'].shape[1]

if __name__ == "__main__":
    batch = ["This is an example of BERT working on MLX."]
    pooled = embed(batch)
    pooled = np.array(pooled)
    print(pooled.shape)