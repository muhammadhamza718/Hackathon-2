# Implementation Plan: AI-Powered Todo Chatbot with MCP Integration

**Branch**: `001-mcp-todo-chatbot` | **Date**: 2025-12-30 | **Spec**: [F:/Courses/Hamza/Hackathon-2-Phase-1/specs/001-mcp-todo-chatbot/spec.md](file:///F:/Courses/Hamza/Hackathon-2-Phase-1/specs/001-mcp-todo-chatbot/spec.md)
**Input**: Feature specification from `/specs/001-mcp-todo-chatbot/spec.md`

## Summary

Implement an AI-powered todo chatbot that integrates MCP (Model Context Protocol) servers for todo operations (add, list, complete, delete, update). The solution will reuse existing architecture patterns from Phase 2 backend, including the OpenAI Agents SDK, ChatKit server handshake, and Gemini configuration, while replacing local tool functions with MCP-based tooling.

## Technical Context

**Language/Version**: Python 3.11, Node.js 18+
**Primary Dependencies**: openai-agents SDK, chatkit-py, mcp (Model Context Protocol SDK), FastAPI, SQLModel, Next.js, Neon DB
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Linux/Windows server for backend, Web browser for frontend
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <3 second response time for 90% of interactions, 95% accuracy for natural language processing
**Constraints**: Stateless backend architecture, MCP server integration, Gemini API usage limits
**Scale/Scope**: Single user focused initially, designed for extensibility to multiple users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven First**: ✅ - Feature specification exists at spec.md with detailed requirements
2. **Reuse Verified Architecture**: ✅ - Will reuse patterns from @[02_Backend] including agent.py, server.py, and Gemini configuration
3. **MCP-Driven Tools**: ✅ - Implementation will use MCP Server instead of local functions for todo operations
4. **Stateless Implementation**: ✅ - Backend will be stateless with all conversation history in Neon DB
5. **Monorepo Structure**: ✅ - Will follow structure with frontend/ and backend/ directories
6. **Tech Stack Compliance**: ✅ - Will use Next.js, FastAPI, SQLModel, Neon DB, and Gemini 1.5/2.5 Flash

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-todo-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agents/
│   │   ├── agent.py           # OpenAI Agent with MCP integration
│   │   └── mcp_server.py      # MCP server for todo operations
│   ├── api/
│   │   └── server.py          # ChatKit handshake server
│   ├── models/
│   │   ├── todo.py            # Todo data model using SQLModel
│   │   └── database.py        # Database connection and session management
│   └── services/
│       └── todo_service.py    # Business logic for todo operations
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── TodoChat.js        # Chat interface component
│   │   └── TodoList.js        # Todo list display component
│   ├── pages/
│   │   └── index.js           # Main page
│   └── services/
│       └── chatService.js     # Service for chat communication
└── tests/
    ├── unit/
    └── e2e/

mcp-server/
├── src/
│   ├── todo_operations.py     # MCP server implementation for todo operations
│   └── config.py              # Configuration for MCP server
└── tests/
    └── unit/
```

**Structure Decision**: Web application with separate backend and frontend directories following monorepo structure. Backend uses FastAPI with SQLModel for database access, frontend uses Next.js with ChatKit integration. MCP server is implemented as a separate service that exposes todo operations via Model Context Protocol.

## Phase 0: Research & Architecture

### Research Tasks
- Investigate MCP (Model Context Protocol) Python SDK implementation patterns
- Review existing agent.py from @[02_Backend] for Gemini integration
- Research ChatKit handshake implementation from @[02_Backend]/server.py
- Analyze SQLModel patterns for Neon DB integration
- Determine how to connect OpenAI Agent to MCP Server for tool operations

### Key Decisions
- MCP Server will implement todo operations (add, list, complete, delete, update) as MCP tools
- Agent will connect to MCP server to access these tools instead of using local functions
- Database models will use SQLModel with Neon DB for persistence
- ChatKit will handle the frontend communication with the backend

## Phase 1: Design & Architecture

### Data Model Design
- Todo model with fields: id, content, completed status, created timestamp, optional due date
- User session model for tracking conversation state
- Database relationships and validation rules

### API Contracts
- RESTful endpoints for todo operations
- ChatKit integration endpoints
- MCP server protocol definitions

### MCP Server Design
- Todo operations as MCP tools
- Connection protocol between agent and MCP server
- Error handling and validation

## Phase 2: Implementation Plan
- MCP Server implementation for todo operations
- Backend integration with MCP server and database
- Frontend implementation with ChatKit
- Testing and validation of the complete system

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations found] | [All constitution requirements met] |
