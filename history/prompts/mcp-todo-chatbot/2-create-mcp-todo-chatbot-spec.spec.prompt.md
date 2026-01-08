---
id: 2
title: Create MCP Todo Chatbot Spec
stage: spec
date: 2025-12-30
surface: agent
model: qwen3-coder-plus
feature: mcp-todo-chatbot
branch: 001-mcp-todo-chatbot
user: user
command: sp.specify
labels: [specification, todo-chatbot, mcp, ai]
links:
  spec: F:/Courses/Hamza/Hackathon-2-Phase-1/specs/001-mcp-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-mcp-todo-chatbot/spec.md
 - specs/001-mcp-todo-chatbot/checklists/requirements.md
tests:
 - none
---

## Prompt

"Implement Phase 3: AI-Powered Todo Chatbot.

CRITICAL IMPLEMENTATION STRATEGY:
1. **Reference Architecture (Reuse Verified Code)**:
   - You MUST use the **exact** patterns from @[02_Backend] for the ChatKit Server and OpenAI Agents SDK setup.
   - Specifically, copy the `agent.py` (Gemini configuration) and `server.py` (ChatKit handshake) logic.
   - Reuse the `init_llm_client` and `GEMINI_MODEL` setup from @[02_Backend/agent.py] to ensure Gemini works for free.

2. **The Delta (What Changed)**:
   - In @[02_Backend], tools were local Python functions (`tools.py`).
   - In **Phase 3**, you must replace `tools.py` with an **MCP Architecture**.
   - Create an **MCP Server** using the `mcp` (Official SDK) that exposes the Todo operations (add, list, complete, delete, update).
   - The Agent in `agent.py` must connect to this MCP Server to use the tools, instead of importing them directly.

3. **Requirements**:
   - Frontend: OpenAI ChatKit (Reuse @[01_Frontend] patterns).
   - Backend: FastAPI + OpenAI Agents SDK (Reuse @[02_Backend] patterns).
   - Database: Neon Serverless PostgreSQL + SQLModel (Reuse Phase 2 DB patterns).
   - **NEW**: MCP Server for tool logic.

4. **Goal**:
   - A 'perfect' backend that uses my working Gemini setup but fulfills the Spec-Driven Development requirement for an MCP Server."

Run /sp.specify command

## Response snapshot

Created a comprehensive specification for the AI-Powered Todo Chatbot with MCP Integration. The spec includes:

- 5 user stories covering core todo functionality (add, list, complete, delete, update)
- Functional requirements (FR-001 to FR-011) including MCP integration, Gemini usage, and stateless architecture
- Key entities (Todo Item, User Session, Chat Message)
- Success criteria with measurable outcomes (SC-001 to SC-005)
- Edge cases for error handling and ambiguous requests

## Outcome

- ✅ Impact: Created complete spec at specs/001-mcp-todo-chatbot/spec.md with all required sections
- 🧪 Tests: No tests required for specification creation
- 📁 Files: Created spec.md and requirements checklist in specs/001-mcp-todo-chatbot/
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification follows SDD principles and captures all requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Begin planning phase with /sp.plan