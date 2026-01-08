---
id: 1
title: Create Phase 3 Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: qwen3-coder-plus
feature: none
branch: 001-ai-todo-chatbot-mcp
user: user
command: sp.constitution
labels: [constitution, hackathon, todo-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

"Phase 3: AI-Powered Todo Chatbot.

Create a Constitution for 'Hackathon-Todo-Phase-3'.

PRINCIPLES:
1. **Spec-Driven First**: No code is written without a specification in `specs/`.
2. **Reuse Verified Architecture**: The backend MUST IMPLEMENT the architectural patterns found in @[02_Backend], specifically:
   - Use `openai-agents` (SDK) for Agent logic.
   - Use `chatkit-py` for the stateless server handshake.
   - Use the **existing Gemini configuration** from `@[02_Backend/agent.py]` to maintain free API usage.
3. **MCP-Driven Tools**: The Delta for Phase 3 is that tools (add, list, etc.) MUST be served via an **Official MCP Server**, not local functions.
4. **Stateless Implementation**: The chat server must hold no state; all conversation history persists to Neon DB.
5. **Monorepo Structure**: Frontend and Backend code reside in `frontend/` and `backend/` respectively.

Tech Stack: Next.js (ChatKit), FastAPI, SQLModel, Neon DB, Gemini 1.5/2.5 Flash."

Run /sp.constitution command right now

## Response snapshot

Created a new constitution file for Hackathon-Todo-Phase-3 with the following principles:
1. Spec-Driven First: No code is written without a specification in `specs/`
2. Reuse Verified Architecture: Using openai-agents SDK, chatkit-py, and existing Gemini configuration
3. MCP-Driven Tools: All tools must be served via Official MCP Server
4. Stateless Implementation: Server holds no state, all data persists to Neon DB
5. Monorepo Structure: Frontend in `frontend/`, Backend in `backend/`
6. Tech Stack Compliance: Using Next.js, FastAPI, SQLModel, Neon DB, and Gemini

## Outcome

- ✅ Impact: Created new constitution file at .specify/memory/constitution.md with 6 core principles
- 🧪 Tests: No tests required for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: Continue with spec, plan, or task creation based on constitution
- 🧠 Reflection: Constitution properly captures all required principles from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Begin specification creation based on constitution