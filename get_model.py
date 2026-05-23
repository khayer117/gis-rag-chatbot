from sentence_transformers import SentenceTransformer

# Small but effective model (~90MB), runs on CPU
model = SentenceTransformer("all-MiniLM-L6-v2")
model.save("./models/all-MiniLM-L6-v2")
print("Embedding model downloaded and saved locally.")
