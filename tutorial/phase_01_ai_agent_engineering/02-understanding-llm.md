# Chapter 02 — Understanding Large Language Models

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** Token, Tokenization, Embedding, Transformer, Attention, Context Window ও Hallucination বোঝা।

> এখানে Transformer-এর ধারণাগত ব্যাখ্যা শিখব। Scratch থেকে বড় model train করা এই Chapter-এর লক্ষ্য নয়।

## 1. LLM কীভাবে text তৈরি করে?

LLM text-কে token-এ ভাঙে। Token numerical ID-তে রূপান্তরিত হয়। Model context দেখে পরবর্তী token-এর probability অনুমান করে। একটি token তৈরি হওয়ার পর সেটি context-এ যোগ হয়, তারপর পরবর্তী token তৈরি হয়। এভাবে response গঠিত হয়।

```text
Input text
   |
Tokenizer
   |
Token IDs
   |
Model layers
   |
Next-token probabilities
   |
Selected token
   |
Repeat until response ends
```

## 2. Token কী?

Token হতে পারে সম্পূর্ণ শব্দ, শব্দের অংশ, punctuation বা text-এর অন্য unit। একটি শব্দ সবসময় একটি token নয়। বাংলা ও ইংরেজি text-এর token count আলাদা হতে পারে। Tokenization model-specific।

## 3. Practical — Tokenization

```bash
cd ~/rahim_ai
source .venv/bin/activate
python -m pip install tiktoken
```

`token_demo.py`:

```python
import tiktoken

samples = [
    "Hello, how are you?",
    "Artificial Intelligence is changing software.",
    "আমি AI Agent তৈরি করতে শিখছি।",
]

# cl100k_base একটি পরিচিত encoding; সব model-এর tokenizer এক নয়।
encoding = tiktoken.get_encoding("cl100k_base")

for text in samples:
    token_ids = encoding.encode(text)

    print("=" * 50)
    print("Text:", text)
    print("Token IDs:", token_ids)
    print("Token count:", len(token_ids))
    print("Decoded:", encoding.decode(token_ids))
```

চালাও:

```bash
python token_demo.py
```

দেখবে text token ID-তে রূপান্তরিত হয়েছে এবং decode করলে আবার text পাওয়া যায়। এই encoding সব model-এর exact tokenizer নয়; এটি ধারণা বোঝানোর Practical।

## 4. Embedding কী?

Embedding হলো token বা text-এর numerical vector representation। Model numerical representation ব্যবহার করে semantic pattern শিখতে পারে।

```text
"king"  -> [0.12, -0.45, 0.88, ...]
"queen" -> [0.10, -0.39, 0.82, ...]
```

উপরের সংখ্যা illustrative, বাস্তব embedding নয়। Embedding semantic search, similarity, recommendation এবং RAG-এ ব্যবহৃত হয়।

## 5. Transformer ও Attention

Transformer আধুনিক অনেক LLM-এর ভিত্তি architecture। Attention একটি token process করার সময় অন্য token-গুলোর সঙ্গে তার সম্পর্ক বিবেচনা করতে সাহায্য করে।

উদাহরণ:

```text
The employee submitted the report because she finished it.
```

“she” কাকে বোঝাচ্ছে, তা বুঝতে sentence-এর অন্য শব্দের context গুরুত্বপূর্ণ। Attention এই ধরনের সম্পর্কের গুরুত্ব গণনায় সাহায্য করে।

High-level architecture:

```text
Text -> Tokenizer -> Token IDs -> Embeddings
     -> Transformer layers (Attention + Feed-forward)
     -> Output probabilities -> Next token
```

## 6. Context Window

Context window হলো model একবারে যে পরিমাণ token process করতে পারে তার সীমা। এতে instructions, user messages, assistant messages, tool results এবং generated output থাকতে পারে। Limit model অনুযায়ী বদলায়।

বড় context window মানেই model সবকিছু নিখুঁতভাবে মনে রাখবে—এমন নয়।

## 7. Temperature

Temperature sampling-এর randomness নিয়ন্ত্রণে সাহায্য করে। কম temperature সাধারণত বেশি predictable output দেয়; বেশি temperature output-এ variation বাড়াতে পারে। সব model/API-তে একই parameter support নাও থাকতে পারে।

## 8. Hallucination

Hallucination হলো আত্মবিশ্বাসী শোনালেও ভুল বা ভিত্তিহীন উত্তর। কারণ হতে পারে অসম্পূর্ণ training data, অস্পষ্ট prompt, অনুপস্থিত context বা external source না থাকা।

প্রতিরোধে সাহায্য করে:
- trusted source থেকে তথ্য আনা
- output validation
- প্রয়োজন হলে tool/search ব্যবহার
- অনিশ্চয়তা জানানো
- গুরুত্বপূর্ণ ফলাফল human review-এ রাখা

## 9. Practical exercise

`token_demo.py`-তে ১০টি বাংলা ও ইংরেজি বাক্য পরীক্ষা করো। Token count লিখে রাখো।

## 10. Homework
1. Token, word ও character-এর পার্থক্য লেখো।
2. Embedding কী, নিজের ভাষায় বোঝাও।
3. Attention-এর একটি বাস্তব উদাহরণ লেখো।
4. Context window ও hallucination ব্যাখ্যা করো।
5. Tokenization Practical চালিয়ে ফলাফল সংরক্ষণ করো।

## Completion checklist
- [ ] Tokenization code চালিয়েছি।
- [ ] Token ID ও count বুঝেছি।
- [ ] Embedding-এর ধারণা বুঝেছি।
- [ ] Transformer flow আঁকতে পারি।
- [ ] Context window ও hallucination ব্যাখ্যা করতে পারি।
