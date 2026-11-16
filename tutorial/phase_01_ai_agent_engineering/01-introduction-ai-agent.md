# Chapter 01 — Introduction to AI, LLM, Chatbot & AI Agent

**সময়:** ৪ ঘণ্টা  
**লক্ষ্য:** AI, ML, Deep Learning, LLM, Chatbot ও Agent-এর পার্থক্য বোঝা এবং ছোট rule-based agent simulation তৈরি করা।

## 1. Traditional Software কী?

সাধারণ Software-এ developer নিয়ম লিখে দেন। Input দিলে সেই নিয়ম অনুযায়ী Output আসে।

```python
def calculate_salary(basic, bonus):
    return basic + bonus

print(calculate_salary(20000, 5000))
```

Output: `25000`। এখানে AI নেই; Python function হিসাব করেছে।

## 2. AI, ML, Deep Learning ও LLM

- **AI (Artificial Intelligence):** কম্পিউটারকে ভাষা বোঝা, ছবি চেনা, পূর্বাভাস বা সিদ্ধান্তে সহায়তার মতো বুদ্ধিবৃত্তিক কাজ করানোর বিস্তৃত ক্ষেত্র।
- **ML (Machine Learning):** Data থেকে pattern শেখার পদ্ধতি।
- **Deep Learning:** বহু স্তরের neural network ব্যবহার করে pattern শেখার পদ্ধতি।
- **LLM (Large Language Model):** বড় neural network-ভিত্তিক ভাষা মডেল, যা text-এর pattern শিখে token তৈরি করতে পারে।
- **Generative AI:** নতুন text, image, audio, video বা code তৈরি করতে পারে এমন AI।

সম্পর্কটি সহজভাবে: AI-এর মধ্যে ML, ML-এর মধ্যে Deep Learning-এর মতো একটি সম্পর্ক আছে; LLM সাধারণত Deep Learning-ভিত্তিক language model।

## 3. Chatbot বনাম AI Agent

Chatbot কথোপকথন করে। Tool-enabled Agent কথোপকথনের পাশাপাশি লক্ষ্য অর্জনের জন্য পরিকল্পনা, Tool নির্বাচন, Tool execution এবং ফলাফল যাচাই করতে পারে।

উদাহরণ:
- Chatbot: “Calendar খুলে আগামীকাল ১০টায় meeting রাখো।”
- Calendar Tool-সহ Agent: free slot পরীক্ষা করে meeting create করার চেষ্টা করতে পারে।

**গুরুত্বপূর্ণ:** LLM নিজে Python function execute করে না। LLM tool call প্রস্তাব করতে পারে; Python application/runtime সেটি যাচাই করে execute করে এবং result ফেরত দেয়।

## 4. Agent-এর প্রধান Component

| Component | কাজ |
|---|---|
| LLM | ভাষা বোঝা ও সম্ভাব্য পদক্ষেপ প্রস্তাব |
| Agent Controller | কাজের flow পরিচালনা |
| Skill | নির্দিষ্ট কাজের নির্দেশনা |
| Memory | প্রয়োজনীয় তথ্য সংরক্ষণ ও retrieval |
| Tool | বাস্তব কাজ করা Python function/API |
| Runtime | Tool নিরাপদে execute করা |
| Guardrails | Permission ও validation |

সব Agent-এ একই component থাকা বাধ্যতামূলক নয়। আমরা ধাপে ধাপে তৈরি করব।

## 5. Practical — Rule-based Agent

```bash
mkdir -p ~/rahim_ai
cd ~/rahim_ai
nano main.py
```

`main.py`:

```python
def greet_user(name):
    return f"Hello {name}! Welcome to AI Agent Engineering."


def calculate_salary(basic, bonus):
    return basic + bonus


def agent(user_input):
    # এটি হাতে লেখা routing logic; এখনো LLM নয়।
    if user_input == "hello":
        return greet_user("Rahim")

    if user_input == "salary":
        total = calculate_salary(20000, 5000)
        return f"Total salary: {total}"

    return "I do not know how to handle this request yet."


def main():
    print("Rahim Agent Simulation")
    print("Commands: hello, salary, exit")

    while True:
        question = input("You: ").strip().lower()

        if question == "exit":
            print("Agent: Goodbye!")
            break

        print("Agent:", agent(question))


if __name__ == "__main__":
    main()
```

চালাও:

```bash
python main.py
```

পরীক্ষা:

```text
You: hello
Agent: Hello Rahim! Welcome to AI Agent Engineering.
You: salary
Agent: Total salary: 25000
You: what is AI
Agent: I do not know how to handle this request yet.
You: exit
Agent: Goodbye!
```

### Code walkthrough
1. `greet_user()` greeting তৈরি করে।
2. `calculate_salary()` হিসাব করে।
3. `agent()` command অনুযায়ী function বেছে নেয়।
4. `main()` input নেয় এবং loop চালায়।
5. `if __name__ == "__main__"` দিয়ে program সরাসরি চালালে `main()` শুরু হয়।

এটি Agent architecture-এর ক্ষুদ্র simulation, কিন্তু LLM নেই। তাই এটি নতুন ভাষাগত অনুরোধ বুঝতে পারে না।

## 6. Flow diagram

```text
User Input
   |
Agent Controller
   |
   +-- hello  --> greet_user()
   +-- salary --> calculate_salary()
   +-- other  --> fallback
   |
Print Result
```

## 7. Homework
1. `time` command যোগ করো, current time দেখাবে।
2. `help` command যোগ করো।
3. Salary-এর basic ও bonus user input থেকে নাও।
4. Chatbot ও Tool-enabled Agent-এর ৫টি পার্থক্য লেখো।
5. Tool এবং Skill-এর পার্থক্য নিজের ভাষায় লেখো।

## 8. Self-check
- AI ও ML কি একই?
- Deep Learning কী?
- LLM কি নিজে Python function execute করে?
- Agent Controller কেন দরকার?

## Completion checklist
- [ ] Code নিজে লিখে চালিয়েছি।
- [ ] `hello`, `salary`, `exit` কাজ করছে।
- [ ] নতুন command যোগ করেছি।
- [ ] Chatbot, LLM ও Agent-এর পার্থক্য বলতে পারি।
