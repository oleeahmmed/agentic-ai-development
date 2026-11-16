# Chapter 03 — ReAct Pattern: Reasoning and Acting

ReAct হলো এমন একটি pattern যেখানে model পর্যায়ক্রমে পরবর্তী action নির্ধারণ করে, tool ব্যবহার করে এবং পাওয়া observation-এর ভিত্তিতে পরবর্তী পদক্ষেপ নেয়।

## 1. ReAct-এর ধারণা

```text
User goal
   |
   v
Decide next action
   |
   v
Action (tool call)
   |
   v
Observation (tool result)
   |
   v
Decide again
   |
   +----> another action
   |
   v
Final answer
```

এখানে model-এর private chain-of-thought সংগ্রহ বা প্রকাশ করার প্রয়োজন নেই। Application-এর জন্য structured action, tool arguments এবং observation-ই যথেষ্ট।

## 2. Practical example

User:
“২৫০ টাকার তিনটি item-এর মোট দাম বের করো, তারপর note-এ রাখো।”

সম্ভাব্য action sequence:
1. `multiply_numbers(250, 3)`
2. Result `750` পাওয়া
3. `save_note("৩টি item-এর মোট দাম ৭৫০ টাকা")`
4. Save confirmation পাওয়া
5. User-কে summary দেওয়া

## 3. Structured decision format

Model-কে free-form text দিয়ে controller চালাতে না দিয়ে নির্দিষ্ট schema ব্যবহার করো।

```python
decision = {
    "type": "tool_call",
    "tool_name": "multiply_numbers",
    "arguments": {"a": 250, "b": 3},
}
```

অথবা:

```python
decision = {
    "type": "final",
    "message": "মোট দাম ৭৫০ টাকা।",
}
```

অথবা:

```python
decision = {
    "type": "need_user_input",
    "question": "প্রতি item-এর দাম কি ২৫০ টাকা?",
}
```

## 4. Action policy

Controller-এর কাজ:
1. Decision-এর type validate করা।
2. Tool name allowlist-এ আছে কি না দেখা।
3. Arguments schema validate করা।
4. Permission check করা।
5. প্রয়োজন হলে confirmation নেওয়া।
6. Tool execute করা।
7. Result observation হিসেবে model-কে দেওয়া।

Model-এর output কখনোই trusted command নয়।

## 5. Observation ভালোভাবে গঠন করা

খারাপ:
```text
Done
```

ভালো:
```json
{
  "success": true,
  "tool": "multiply_numbers",
  "result": 750,
  "unit": "BDT"
}
```

Error observation:
```json
{
  "success": false,
  "tool": "divide_numbers",
  "error_code": "DIVISION_BY_ZERO",
  "message": "শূন্য দিয়ে ভাগ করা যায় না।"
}
```

Structured result model-কে পরবর্তী সিদ্ধান্ত নিতে সাহায্য করে।

## 6. Tool call আর reasoning আলাদা রাখো

- Model: “পরবর্তী কোন action দরকার?” নির্ধারণ করে।
- Controller: policy প্রয়োগ করে।
- Tool: নির্দিষ্ট কাজ করে।
- Observation: tool-এর ফলাফল।
- Model: observation দেখে পরবর্তী action বা final response বেছে নেয়।

## 7. ReAct-এর ঝুঁকি

- একই tool বারবার call
- ভুল arguments
- অপ্রয়োজনীয় tool use
- hallucinated success
- prompt injection থেকে ভুল action
- অতিরিক্ত tool execution cost

প্রতিরোধ:
- Max rounds
- Duplicate-action detection
- Idempotency key
- Tool permission
- Confirmation
- Result verification
- Structured logs

## 8. Exercise

1. Calculator ও note tool দিয়ে উপরের example-এর sequence কাগজে আঁকো।
2. `decision` dictionary-এর তিনটি type validate করার function লেখো।
3. Unknown tool name reject করো।
4. একই `save_note` action duplicate হলে কীভাবে ঠেকাবে, design করো।

**Chapter outcome:** ReAct-style action/observation workflow বুঝতে পারবে এবং model output-কে নিরাপদভাবে controller-এ ব্যবহার করতে পারবে।
