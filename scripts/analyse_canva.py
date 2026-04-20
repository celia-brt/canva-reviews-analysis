import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

# 1. Load data
df = pd.read_csv("/Users/celiabreteau/Downloads/verbatims.csv")
texts = df["Text"].astype(str).tolist()

# 2. Embeddings model (fast + multilingual)
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

# 3. Reduce dimension
reducer = umap.UMAP(n_neighbors=15, n_components=5, metric="cosine")
reduced = reducer.fit_transform(embeddings)

# 4. Clustering
clusterer = hdbscan.HDBSCAN(min_cluster_size=50)
labels = clusterer.fit_predict(reduced)

df["cluster"] = labels

# 5. Save result
df.to_csv("verbatims_clustered.csv", index=False)

print("DONE - file saved: verbatims_clustered.csv")
