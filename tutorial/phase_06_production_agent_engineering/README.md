# Phase 06 — Production Agent Engineering

এই Phase-এ prototype agent-কে production-minded system বানানোর engineering শিখবেন: reliability, security, retry/timeout, async, observability, testing এবং MCP।

## Chapter list
1. Production Agent Architecture & Reliability
2. Security, Permissions, Prompt Injection & Guardrails
3. Error Handling, Retry, Timeout & Rate Limits
4. Async Python & Concurrent Tool Execution
5. Logging, Observability, Evaluation & Testing
6. MCP + Production Agent Capstone

## Ubuntu setup
```bash
mkdir phase06_agent && cd phase06_agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install openai python-dotenv pydantic tenacity pytest
```
`.env`-এ `OPENAI_API_KEY=...` রাখুন। `.env` কখনো GitHub-এ commit করবেন না। MCP chapter-এ MCP SDK আলাদাভাবে install করবেন। SDK/API version বদলাতে পারে, তাই official MCP Python SDK documentation দেখে tested version pin করবেন।

এই Phase-এর code শিক্ষামূলক reference implementation; production deployment-এর আগে authentication, authorization, durable storage, secrets management, monitoring এবং security/load testing যোগ করতে হবে।
