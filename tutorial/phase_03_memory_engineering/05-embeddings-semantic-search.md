# Chapter 05 — Embeddings & Semantic Search

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Text embedding কী, কেন ব্যবহার হয় এবং semantic similarity দিয়ে relevant memory খুঁজে বের করা।

## 1. Keyword search-এর সমস্যা

ধরো memory-তে আছে:

> User is learning Python programming.

User প্রশ্ন করল:

> আমি কোন coding language শিখছি?

Keyword search-এ exact word না মিললেও অর্থ কাছাকাছি। Semantic search অর্থের মিল ধরার চেষ্টা করে।

## 2. Embedding কী?

Embedding হলো text-কে একটি numerical vector-এ রূপান্তর করা। একই অর্থ বা কাছাকাছি অর্থের text-এর vector সাধারণত embedding space-এ কাছাকাছি থাকতে পারে।

ধারণাগত উদাহরণ:

```text
"I am learning Python"
          |
          v
Embedding model
          |
          v
[0.12, -0.08, 0.31, ...]
```

এই সংখ্যা শুধু illustrative; বাস্তব vector-এর dimension ও value model অনুযায়ী আলাদা হয়।

## 3. Embedding model বনাম Chat model

- Chat model: text বুঝে উত্তর তৈরি করে।
- Embedding model: text-কে vector-এ রূপান্তর করে।

একটি embedding নিজে উত্তর তৈরি করে না।

## 4. Practical — embedding তৈরি

```bash
cd ~/rahim_ai
nano embeddings_demo.py
```

Code:

```python
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)


def create_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


if __name__ == "__main__":
    sentence = input("Text: ")
    vector = create_embedding(sentence)

    print("Vector dimensions:", len(vector))
    print("First 10 values:", vector[:10])
```

চালাও:

```bash
python3 embeddings_demo.py
```

প্রথমবার API request হবে, তাই internet ও valid API key লাগবে।

## 5. Cosine similarity

দুটি vector-এর দিক কতটা কাছাকাছি তা cosine similarity দিয়ে মাপা যায়।

\[
\operatorname{cosine}(A,B)=
\frac{A\cdot B}{\|A\|\|B\|}
\]

সহজভাবে:
- 1-এর কাছাকাছি: একই দিকে
- 0-এর কাছাকাছি: প্রায় orthogonal
- -1-এর কাছাকাছি: বিপরীত দিকে

বাস্তব semantic similarity score model ও data অনুযায়ী ব্যাখ্যা করতে হয়; নির্দিষ্ট threshold সব dataset-এর জন্য এক নয়।

## 6. Practical — Python-এ cosine similarity

```bash
nano similarity.py
```

```python
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimensions")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Zero vector has no cosine direction")

    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    vector_a = [1.0, 0.0, 1.0]
    vector_b = [0.9, 0.1, 0.8]
    vector_c = [0.0, 1.0, 0.0]

    print("A vs B:", cosine_similarity(vector_a, vector_b))
    print("A vs C:", cosine_similarity(vector_a, vector_c))
```

Run:

```bash
python3 similarity.py
```

এখানে ছোট illustrative vector দিয়ে formula পরীক্ষা করছ। এটি production embedding search নয়।

## 7. Semantic retrieval-এর ধারণা

```text
Stored memories/documents
       |
       v
Embedding model
       |
       v
Vectors stored in an index

User query
       |
       v
Query embedding
       |
       v
Similarity search
       |
       v
Top relevant memories
```

## 8. গুরুত্বপূর্ণ বিষয়

- Query ও document একই compatible embedding model দিয়ে encode করতে হবে।
- Model বদলালে পুরোনো vectors re-embed করতে হতে পারে।
- Text chunking retrieval quality-তে প্রভাব ফেলে।
- Similarity মানেই factual correctness নয়।
- Retrieved content-এর source ও permission বজায় রাখতে হবে।

## Homework

1. তিনটি related ও তিনটি unrelated sentence বেছে embedding তৈরি করো।
2. Vector dimension print করো।
3. Cosine similarity formula নিজে ব্যাখ্যা করো।
4. Semantic search কেন exact keyword search থেকে আলাদা তা লেখো।

## Completion checklist

- [ ] Embedding কী বুঝেছি
- [ ] Embedding API call করেছি
- [ ] Vector dimension দেখেছি
- [ ] Cosine similarity implement করেছি
- [ ] Semantic retrieval flow বুঝেছি
