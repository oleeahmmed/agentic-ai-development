# Chapter 05 — Tool Loop, Results & Error Handling

Model-এর tool request execute করলেই cycle শেষ হয় না। Python-কে tool result আবার model-কে পাঠাতে হয়।

## 1. Complete cycle

```text
User message
    |
Responses API + tool definitions
    |
Model returns function_call
    |
Python validates & executes tool
    |
Python creates function_call_output
    |
Responses API continuation
    |
Model produces final answer
```

## 2. Complete single-round example

`main.py`:

```python
import json
from config import client
from tools.registry import execute_tool

tools = [
    {
        "type": "function",
        "name": "add_numbers",
        "description": "দুটি সংখ্যা যোগ করে।",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

def ask_agent(user_message: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_message,
        tools=tools,
    )

    tool_outputs = []

    for item in response.output:
        if item.type != "function_call":
            continue

        try:
            arguments = json.loads(item.arguments)
            result = execute_tool(item.name, arguments)
            payload = {"success": True, "result": result}
        except Exception as error:
            # Production-এ internal detail log করবে; secret expose করবে না।
            payload = {"success": False, "error": str(error)}

        tool_outputs.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(payload, ensure_ascii=False),
        })

    if not tool_outputs:
        return response.output_text

    final_response = client.responses.create(
        model="gpt-4.1-mini",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools,
    )
    return final_response.output_text


if __name__ == "__main__":
    print(ask_agent("৪৫ এবং ৫৫ যোগ করে ফলাফল বুঝিয়ে বলো।"))
```

## 3. `call_id` কেন জরুরি?

Model-এর function call-এর সঙ্গে `call_id` থাকে। Tool result-এ একই `call_id` দিতে হয়, যাতে API সঠিক call-এর result চিনতে পারে।

## 4. একাধিক tool call

একটি response-এ একাধিক function call থাকতে পারে। তাই সবগুলো iterate করতে হবে এবং সব output continuation request-এ পাঠাতে হবে।

## 5. Bounded tool loop

Production agent-এ model আবার tool call চাইতে পারে। তাই loop-এর সীমা রাখবে:
- সর্বোচ্চ tool rounds
- সর্বোচ্চ tool calls
- Timeout
- Allowed tool names
- Per-call validation

অসীম loop চলতে দেবে না।

## 6. Failure types
- Invalid JSON arguments
- Unknown tool
- Missing argument
- Validation failure
- Database/API unavailable
- Permission denied
- Timeout

ব্যবহারকারীকে সংক্ষিপ্ত নিরাপদ error দাও। Debug details developer log-এ রাখবে; API key, password বা sensitive content log করবে না।

## 7. Exercise
1. `divide_numbers` tool definition যোগ করো।
2. `10 / 0` দিয়ে error path পরীক্ষা করো।
3. `MAX_TOOL_ROUNDS = 5` দিয়ে bounded loop design করো।
4. Tool call ও output-এর `call_id` মিলিয়ে দেখো।

**Outcome:** Request → execution → result → final answer cycle implement করতে পারবে।
