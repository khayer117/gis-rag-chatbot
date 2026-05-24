# How It Works — Understanding Embedding Output Values

A FAQ-style guide explaining how text embeddings and vector search work in this RAG pipeline.

---

## Embeddings

### What do the floating-point values in an embedding output represent?

Those numbers are a **dense vector embedding** — a list of 384 floating-point numbers produced by the `all-MiniLM-L6-v2` model. Each index (000, 001, 002...) is a **dimension** in a high-dimensional semantic space. The model learned during training that certain directions in this space capture meaning — things like formality, topic category, or sentiment. No single dimension has a human-readable label; the meaning lives in the *combination* of all 384 values together.

---

### What do negative values in an embedding signify?

Negative values are completely normal and expected. The model uses both positive and negative directions in each dimension to encode meaning. Think of it as coordinates — a value of `-0.06` simply means "slightly negative in that dimension's direction." There is no concept of "bad" or "invalid." The values are roughly bounded between `-1.0` and `+1.0` because the final vector is L2-normalized (length = 1.0).

---

### Is an embedding similar to a hash function?

No — an embedding is the opposite of a hash in the ways that matter:

| | Hashing | Embedding |
|---|---|---|
| Similar inputs | Completely different output | Very similar output (close vectors) |
| Purpose | Uniqueness / fingerprint | Semantic similarity |
| Reversible | No | No |
| Numeric meaning | Arbitrary | Encodes semantic directions |

A hash of `"hi hello"` and `"hello hi"` would look nothing alike. Their embeddings would be nearly identical — cosine similarity close to `1.0` — because the model understands they carry the same meaning.

---

### What does "384-dimensional space" mean — is it a 384th-dimension matrix?

No, it is not a matrix. It is simply a **flat list (1D array) of 384 numbers**:

```
"hi hello"  →  [-0.064, 0.043, 0.060, 0.048, -0.056, ...]
                  dim0   dim1   dim2   dim3    dim4      dim383
```

The word *dimension* is borrowed from geometry. A 2D point needs 2 numbers `(x, y)`; a 3D point needs 3 `(x, y, z)`. A 384-dimensional point needs 384 numbers. You cannot visualize it, but the math is identical. Two embeddings that are numerically close to each other represent texts with similar meaning.

---

### Does every chunk of text — regardless of length — produce exactly 384 floats?

Yes. Every text input, whether a single word or a long paragraph, produces exactly **384 floats**. The dimension count is fixed by the model architecture. The model compresses any length of text into the same fixed-size representation through tokenization, transformer attention layers, and mean pooling.

```
"GIS stands for..."          →  [384 floats]
"Coordinate systems are..."  →  [384 floats]
"hi hello"                   →  [384 floats]
```

---

### Does ChromaDB generate the embedding floats?

No. ChromaDB only **stores and searches** embeddings — it does not generate them. The embedding model (`all-MiniLM-L6-v2`) produces the floats. ChromaDB receives them and indexes them for fast similarity search.

```
Text chunk
    │
    ▼
all-MiniLM-L6-v2  ←  generates the 384 floats
    │
    ▼
ChromaDB          ←  stores and searches those floats
```

---

### Do all embedding models produce 384 floats?

No. The number of floats (called **dimensions**) varies by model. `384` is specific to `all-MiniLM-L6-v2`.

| Model | Dimensions |
|---|---|
| `all-MiniLM-L6-v2` (this project) | 384 |
| `all-mpnet-base-v2` | 768 |
| `text-embedding-ada-002` (OpenAI) | 1536 |
| `text-embedding-3-large` (OpenAI) | 3072 |
| `nomic-embed-text` (Ollama) | 768 |

Larger dimensions generally improve accuracy but increase storage, RAM usage, and search time. The `all-MiniLM-L6-v2` choice at 384 dims is a deliberate tradeoff — fast, fully local, and sufficient for a focused GIS knowledge base.

**Important:** you must use the same embedding model for both ingestion and querying. Vectors from different models cannot be compared — they are different shapes entirely.

---

### Is ChromaDB compatible with any embedding model regardless of dimension size?

Yes. ChromaDB is **dimension-agnostic** — it works with any embedding model at any dimension size. When the first chunk is added to a collection, ChromaDB auto-detects and locks the dimension for that collection. Subsequent inserts must match that dimension, but separate collections can use different dimensions in the same ChromaDB instance.

```
collection "gis_knowledge"  →  384 dims  (all-MiniLM-L6-v2)
collection "legal_docs"     →  1536 dims (text-embedding-ada-002)
```

Other vector databases (Pinecone, Weaviate, pgvector, FAISS) work the same way — they are all just smart float-array storage and search engines.

---

### How does the embedding model assign float values to a given input? What is the algorithm?

The values come from a multi-step process — not from a hand-written formula, but from weights learned during training on millions of sentence pairs.

**Step 1 — Tokenization**
Text is split into subword tokens from a fixed vocabulary and mapped to integer IDs. Special tokens are added:
```
"hi hello"  →  [CLS, hi, hello, SEP]  →  [101, 2182, 7592, 102]
```

**Step 2 — Token Lookup**
Each token ID maps to a pre-trained vector row in a large weight matrix (768 floats per token for this model).

**Step 3 — Transformer Attention Layers**
Tokens "attend" to each other across 6 layers. Each token's vector is updated based on surrounding context:
```
"hi" sees "hello"  →  updates its vector
"hello" sees "hi"  →  updates its vector
```

**Step 4 — Mean Pooling**
All token vectors are averaged into one single vector of 768 floats.

**Step 5 — Linear Projection**
A trained weight matrix compresses 768 → 384 floats.

**Step 6 — L2 Normalization**
The vector is scaled so its length equals 1.0, which makes cosine similarity computationally efficient.

The model was trained so that semantically similar sentences produce close vectors, and unrelated sentences produce distant vectors. The float values are the learned outcome of that training — not computed by a deterministic rule.

---

## Vector Search

### How does ChromaDB perform a similarity search when a query is submitted?

**Step 1 — Encode the query**
The same embedding model encodes the user's query into 384 floats.

**Step 2 — Cosine similarity against all stored vectors**
For every stored chunk, ChromaDB computes the cosine similarity between the query vector and the chunk vector:

```
cosine_similarity = (A · B) / (|A| × |B|)
```

Where `A · B` is the dot product (multiply each pair of floats and sum), and `|A|` is the vector length. The result ranges from `-1.0` (opposite meaning) to `1.0` (identical meaning).

**Step 3 — Rank and filter**
Results are sorted by score, highest first. Chunks below `SIMILARITY_THRESHOLD = 0.3` are discarded. The top `TOP_K = 5` chunks are returned.

**Step 4 — Return original text**
ChromaDB returns the original text of the top chunks, not the vectors. These are injected into the LLM prompt as context.

---

### Why is cosine similarity used instead of Euclidean distance?

For text meaning, **direction matters more than magnitude**:

```
"GIS"  vs  "GIS GIS GIS GIS"
```

Both carry the same meaning, but repeating words produces a longer vector. Cosine similarity measures the *angle* between vectors and ignores their length, so both examples would score as nearly identical. Euclidean distance would incorrectly treat them as far apart.

---

### Does ChromaDB compare the query against every stored vector?

For small collections, yes — it uses **brute-force comparison** (exact search). For millions of vectors, ChromaDB switches to an approximate algorithm called **HNSW** (Hierarchical Navigable Small World graphs), which finds near-neighbors without checking every vector, trading a small accuracy loss for a large speed gain.

---

*This document is based on an exploratory session covering the internals of the `all-MiniLM-L6-v2` embedding model and ChromaDB vector search as used in this project.*
