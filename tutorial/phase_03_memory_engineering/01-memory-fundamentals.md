# Chapter 01 — Memory Fundamentals

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** AI Agent-এর Memory কী, কেন দরকার, এবং Context, History ও Memory-এর পার্থক্য বোঝা।

## 1. বাস্তব গল্প

ধরো তুমি Rahim AI-কে বললে:

> আমার নাম রাহিম। আমি Python শিখছি। আমার project-এর নাম rahim_ai।

কিছুক্ষণ পর জিজ্ঞেস করলে:

> আমার project-এর নাম কী?

একই conversation-এর আগের message model-কে পাঠানো হলে সে উত্তর দিতে পারে। কিন্তু নতুন session শুরু হলে আগের message আর context-এ নাও থাকতে পারে।

এখানেই Memory দরকার।

## 2. Memory কী?

AI Agent Memory হলো এমন একটি ব্যবস্থা, যার মাধ্যমে Agent আগের interaction বা সংরক্ষিত তথ্য থেকে পরবর্তী সময়ে প্রাসঙ্গিক তথ্য ব্যবহার করতে পারে।

উদাহরণ:
- User-এর শেখার লক্ষ্য
- Project-এর নাম
- Project-এর প্রযুক্তি
- চলমান কাজের অবস্থা
- User-এর স্পষ্টভাবে জানানো দীর্ঘমেয়াদি preference

## 3. Context বনাম History বনাম Memory

| বিষয় | অর্থ | উদাহরণ |
|---|---|---|
| Context | বর্তমান model call-এ দেওয়া তথ্য | System instruction |
| Conversation history | আগের message-গুলোর ধারাবাহিকতা | আগের ১০টি message |
| Short-term memory | চলমান কাজের অস্থায়ী state | এই session-এর current task |
| Long-term memory | ভবিষ্যৎ session-এ দরকার হতে পারে এমন stored fact | Project-এর নাম |
| Knowledge base | কোনো domain-এর document বা reference | Company policy PDF |

সব history-ই memory নয়। সব memory-ও প্রতিটি prompt-এ পাঠানো উচিত নয়।

## 4. Memory কেন দরকার?

Memory ছাড়া Agent:
- নতুন session-এ আগের project context হারাতে পারে
- একই প্রশ্ন বারবার করতে পারে
- দীর্ঘ কাজের progress ধরে রাখতে পারে না
- ব্যক্তিগত workflow-এর ধারাবাহিকতা বজায় রাখতে পারে না

তবে অতিরিক্ত memory-ও সমস্যা:
- অপ্রয়োজনীয় তথ্য জমে যায়
- পুরোনো তথ্য ভুল হতে পারে
- privacy ঝুঁকি তৈরি হয়
- prompt context অযথা বড় হয়

## 5. Memory-এর সাধারণ শ্রেণি

```text
Agent Memory
├── Short-term
│   ├── Recent messages
│   └── Current task state
│
├── Long-term
│   ├── User facts
│   ├── Preferences
│   └── Project facts
│
└── Semantic / Retrieval memory
    ├── Embeddings
    ├── Vector index
    └── Retrieved passages
```

এটি একটি শেখার সুবিধার classification। বিভিন্ন framework-এ নাম বা implementation আলাদা হতে পারে।

## 6. Memory lifecycle

```text
Conversation
    |
    v
Candidate fact extraction
    |
    v
Validation and policy checks
    |
    v
Store / update / reject
    |
    v
Future user request
    |
    v
Retrieve relevant memory
    |
    v
Build model context
```

গুরুত্বপূর্ণ: LLM-কে “মনে রাখো” বললেই স্বয়ংক্রিয়ভাবে নির্ভরযোগ্য database তৈরি হয় না। Storage ও retrieval-এর দায়িত্ব application-এর।

## 7. Practical — Memory ছাড়া ও Memory-সহ

প্রথমে আগের `main.py` চালিয়ে নতুন conversation-এ একটি project detail বলো। তারপর program বন্ধ করে আবার চালিয়ে একই detail জিজ্ঞেস করো। যদি history বা persistent storage না থাকে, model-এর কাছে আগের তথ্য থাকবে না।

এই পরীক্ষায় এখনই code বদলানোর দরকার নেই। উদ্দেশ্য হলো সমস্যাটি নিজে দেখা।

## 8. Design exercise

নিচের তথ্যগুলো কোন memory category-তে যাবে?

1. চলমান conversation-এর শেষ user message
2. বর্তমান coding task-এর progress
3. User-এর project name
4. Company policy document-এর paragraph
5. User-এর একবারের random question

নিজে category নির্ধারণ করো এবং কেন তা লিখো।

## Homework

1. Memory ছাড়া chatbot-এর তিনটি সীমাবদ্ধতা লেখো।
2. Context, history ও long-term memory-এর পার্থক্য নিজের ভাষায় লেখো।
3. `rahim_ai`-এর জন্য কোন ৫ ধরনের তথ্য memory-তে রাখা যেতে পারে তার তালিকা তৈরি করো।
4. কোন ধরনের তথ্য সংরক্ষণ না করাই ভালো—৩টি উদাহরণ লেখো।

## Completion checklist

- [ ] Memory কী বুঝেছি
- [ ] Context ও history-এর পার্থক্য বুঝেছি
- [ ] Short-term ও long-term memory বুঝেছি
- [ ] Memory lifecycle বুঝেছি
