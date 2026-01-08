---
id: 0003
title: "Fix Database Connection and Agent Language"
stage: "red"
date_iso: "2026-01-01"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-mcp-todo-chatbot"
user: "unknown"
command: "/sp.fix_code"
labels: ["database", "dotenv", "environment-variables", "language", "agent"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/db/session.py"
  - "backend/src/models/database.py"
  - "backend/main.py"
  - "backend/agent.py"
tests_yaml:
  - "none"
---

# Fix Database Connection and Agent Language

## Prompt Text

Fix the database connection in the backend. load_dotenv() is called too late, causing the engine to use fallback credentials. Move it to the top of main.py and agent.py. Also, the agent is speaking German; update its instructions to strictly use English.

## Response Text

Successfully fixed the database connection issue by ensuring load_dotenv() is called before database engines are created in db/session.py and src/models/database.py, and reordering imports in main.py. Also enhanced agent.py instructions to explicitly require English and prohibit German phrases.

## Outcome Impact

Fixed database connection issue where engines were created with fallback credentials instead of environment variables, and ensured the agent responds exclusively in English as requested.

## Tests Summary

Verified database modules load actual environment variables instead of fallback credentials, confirmed modules import successfully, and validated agent instructions contain English requirement.

## Files Summary

- backend/db/session.py: Moved load_dotenv() to top
- backend/src/models/database.py: Added load_dotenv() before engine creation
- backend/main.py: Reordered imports to call load_dotenv() early
- backend/agent.py: Enhanced English language instructions

## Next Prompts

None

## Reflection Note

The issue was more complex than initially apparent, requiring fixes in multiple files beyond just main.py and agent.py, including the database modules where engines were created at import time before environment variables were loaded.

## Failure Modes Observed

None

## Next Experiment to Improve Prompt Quality

N/A
