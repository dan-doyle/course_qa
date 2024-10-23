import numpy as np

def embed_dataframe(dataframe, embed, batch_size=4):
    all_embeddings = []

    for i in range(0, len(dataframe), batch_size):
        batch_content = dataframe['content'].iloc[i:i + batch_size].tolist()
        batch_embeddings = embed(batch_content)
        if not isinstance(batch_embeddings, np.ndarray):
            raise ValueError("The embed function must return a numpy array.")
        
        all_embeddings.append(batch_embeddings)

    all_embeddings = np.vstack(all_embeddings)
    dataframe['embedding'] = list(all_embeddings)
    
    return dataframe
