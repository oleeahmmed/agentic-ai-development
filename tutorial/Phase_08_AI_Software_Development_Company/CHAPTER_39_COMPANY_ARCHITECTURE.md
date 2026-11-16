# Chapter 39 — AI Software Development Company: Product Scope & Architecture

## 1. আমরা কী তৈরি করছি?

একজন client বলল: “আমার inventory management web application দরকার। Product, stock-in, stock-out, supplier, login এবং reports থাকবে।”

একটি software company-তে Business Analyst requirements বোঝে, Architect design করে, Developer code লেখে, QA test করে, Security Engineer ঝুঁকি দেখে, DevOps deployment প্রস্তুত করে এবং Project Manager কাজ পরিচালনা করে।

আমাদের AI company-তে এই দায়িত্বগুলো আলাদা specialist agent পালন করবে। Supervisor Agent workflow পরিচালনা করবে। গুরুত্বপূর্ণ সিদ্ধান্তে human approval লাগবে।

**মূল ধারণা:** অনেক agent মানেই অনেক স্বাধীন AI নয়। এগুলো নির্দিষ্ট দায়িত্ব, সীমাবদ্ধতা, skills, tools এবং shared project state-সহ orchestrated workers।

## 2. Product scope

প্রথম সংস্করণ:
1. Client request গ্রহণ।
2. Structured requirements তৈরি।
3. Architecture proposal তৈরি।
4. Development tasks তৈরি।
5. সীমিত workspace-এ code draft/patch তৈরি।
6. Automated tests চালানো।
7. Security review।
8. Human review-এর জন্য report।

প্রথম সংস্করণে থাকবে না:
- Human approval ছাড়া production deployment
- Arbitrary shell execution
- Unlimited internet access
- Production database-এ সরাসরি পরিবর্তন
- Agent-কে নিজের permission নিজে বাড়াতে দেওয়া

## 3. High-level architecture

```text
CLIENT / HUMAN
      |
      v
API / DASHBOARD
      |
      v
SUPERVISOR AGENT
      |
      +---- ANALYST
      +---- ARCHITECT
      +---- PROJECT MANAGER / TASK BOARD
      +---- DEVELOPER ----> ISOLATED WORKSPACE
      +---- TESTER
      +---- SECURITY REVIEWER
      +---- DEVOPS
                 |
                 v
          HUMAN APPROVAL
                 |
                 v
          STAGING / RELEASE
```

## 4. Agent responsibilities

### Supervisor
- Request গ্রহণ, workflow নির্বাচন, specialist assign
- Shared state update ও run status track
- Failure-এ retry বা human escalation
- Final report তৈরি

Supervisor arbitrary code execute করবে না এবং policy override করতে পারবে না।

### Analyst
Output:
- Problem statement
- Functional requirements
- Non-functional requirements
- Acceptance criteria
- Open questions

### Architect
Output:
- Component architecture
- Database entities ও relations
- API design
- Security controls
- Risks ও trade-offs

### Developer
- Approved task অনুযায়ী code draft
- Authorized workspace-এর file read
- Patch propose
- Implementation summary

Developer-এর tool access allowlist-based হবে। Project root-এর বাইরে write নিষিদ্ধ।

### Tester
- Acceptance criteria থেকে test cases
- Restricted runner-এ tests
- Failure reproduction steps

### Security Reviewer
- Authentication ও authorization
- Input validation
- Secret leakage
- Injection risks
- Dependency/configuration review

Security reviewer-এর “pass” শতভাগ নিরাপত্তার প্রমাণ নয়।

### DevOps
- Docker/deployment config draft
- Environment checklist
- Health check ও rollback plan
- Staging deployment proposal

Production deployment-এর জন্য আলাদা human approval থাকবে।

## 5. Skills vs Tools vs Agents

| ধারণা | কাজ | উদাহরণ |
|---|---|---|
| Skill | কাজ করার নির্দেশনা/workflow | `django_api_development` |
| Tool | বাস্তব কাজ করা function/API | `read_file`, `run_tests` |
| Agent | Model + instructions + state + tools | Developer Agent |

Skill নিজে code execute করে না। Tool execute করে; application permission যাচাই করে তারপর।

## 6. Skills library

```text
skills/
├── business_analysis/SKILL.md
├── system_architecture/SKILL.md
├── django_backend/SKILL.md
├── react_frontend/SKILL.md
├── database_design/SKILL.md
├── testing/SKILL.md
├── security_review/SKILL.md
└── devops/SKILL.md
```

প্রতিটি skill-এ রাখবে: purpose, when-to-use, workflow, coding conventions, output format, validation checklist, forbidden actions এবং escalation rules।

## 7. Shared project state

```python
project_state = {
    "project_id": "PRJ-001",
    "client_request": "Build an inventory management system",
    "requirements": [],
    "architecture": {},
    "tasks": [],
    "code_changes": [],
    "test_results": [],
    "security_findings": [],
    "approvals": [],
    "status": "requirements_pending",
}
```

Rules:
1. State schema versioned হবে।
2. Agent শুধু নিজের অনুমোদিত fields update করবে।
3. State changes audit log-এ লিখবে।
4. LLM-generated data validate করবে।
5. Secrets state বা prompt-এ রাখবে না।

## 8. Relational data model

### `users`
`id`, `email`, `password_hash` বা external identity reference, `role`, `is_active`, `created_at`

### `clients`
`id`, `name`, `contact_email`, `created_at`

### `projects`
`id`, `client_id`, `name`, `description`, `status`, `created_at`, `updated_at`

### `tasks`
`id`, `project_id`, `title`, `description`, `assigned_agent`, `status`, `priority`, timestamps

### `artifacts`
`id`, `project_id`, `task_id`, `artifact_type`, `storage_key`, `version`, `created_at`

### `agent_runs`
`id`, `project_id`, `agent_name`, `status`, `input_summary`, `output_summary`, `started_at`, `finished_at`

### `approvals`
`id`, `project_id`, `action_type`, `action_payload_hash`, `requested_by`, `approved_by`, `status`, timestamps

### `audit_events`
`id`, `actor_type`, `actor_id`, `action`, `resource_type`, `resource_id`, `metadata_json`, `created_at`

Production design-এ foreign keys, indexes, tenant scoping, retention, encryption ও migrations লাগবে।

## 9. Workflow state machine

```text
REQUEST_RECEIVED
 -> REQUIREMENTS_DRAFT
 -> REQUIREMENTS_REVIEW
 -> ARCHITECTURE_DRAFT
 -> ARCHITECTURE_APPROVAL
 -> TASKS_READY
 -> DEVELOPMENT
 -> TESTING
 -> SECURITY_REVIEW
 -> HUMAN_FINAL_REVIEW
 -> STAGING_APPROVAL
 -> STAGING_DEPLOYMENT
 -> DONE
```

প্রতিটি transition application code যাচাই করবে। LLM-কে যেকোনো database status ইচ্ছামতো পরিবর্তন করতে দেবে না।

## 10. Approval policy

| Action | Default policy |
|---|---|
| Requirements/architecture draft | Agent করতে পারবে |
| Task create | Policy অনুযায়ী |
| Read project files | Workspace permission |
| Write files | Isolated workspace + allowlist |
| Run tests | Restricted runner |
| Install dependency | Vetted allowlist / approval |
| Delete files | Explicit approval |
| Production secrets access | Agent-এর জন্য নিষিদ্ধ |
| Production deploy | Human approval বাধ্যতামূলক |

Approval record-এ actor identity, exact action, payload hash, timestamp, expiry ও audit trail থাকবে। Payload বদলালে পুরনো approval invalid।

## 11. Reliability

- Tool timeout ও output-size limit
- Transient error-এ exponential backoff + jitter
- Non-idempotent action-এ idempotency key
- Agent loop-এ max steps
- Token/cost budget
- Structured output validation
- Partial result persistence
- Human escalation path

## 12. Observability

Track: `trace_id`, `project_id`, `agent_name`, `model`, `prompt_version`, `skill_version`, `tool_name`, `duration_ms`, `token_usage`, `estimated_cost`, `status`, `error_type`।

API key, password, private key বা access token log করবে না।

## 13. Practical assignment

“Clinic Appointment Management System” বেছে নাও। তৈরি করো:
1. ১০ functional requirements
2. ৫ non-functional requirements
3. ৮ acceptance criteria
4. Architecture proposal
5. Database entity list
6. ১০ development tasks
7. Approval matrix
8. Threat/risk list

## 14. Checkpoint

পরের chapter-এ যাওয়ার আগে ব্যাখ্যা করতে পারবে:
- Supervisor ও specialist-এর পার্থক্য
- Skill, Tool ও Agent-এর পার্থক্য
- Shared state কেন দরকার
- LLM output কেন untrusted
- Human approval কোথায় বাধ্যতামূলক
