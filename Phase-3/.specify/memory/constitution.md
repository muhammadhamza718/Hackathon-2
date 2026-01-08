<!-- Sync Impact Report:
     Version change: N/A -> 1.0.0
     Modified principles: N/A (new constitution)
     Added sections: All sections
     Removed sections: N/A
     Templates requiring updates: N/A
     Follow-up TODOs: None
-->
# Hackathon-Todo-Phase-3 Constitution

## Core Principles

### Spec-Driven First
No code is written without a specification in `specs/`. All development work must be based on a clear specification document that outlines requirements, acceptance criteria, and implementation approach before any code is written.

### Reuse Verified Architecture
The backend MUST IMPLEMENT the architectural patterns found in @[02_Backend], specifically: Use `openai-agents` (SDK) for Agent logic. Use `chatkit-py` for the stateless server handshake. Use the **existing Gemini configuration** from `@[02_Backend/agent.py]` to maintain free API usage.

### MCP-Driven Tools
The Delta for Phase 3 is that tools (add, list, etc.) MUST be served via an **Official MCP Server**, not local functions. All tool functionality must be exposed through MCP (Model Context Protocol) servers rather than being implemented as local functions.

### Stateless Implementation
The chat server must hold no state; all conversation history persists to Neon DB. The server implementation must be stateless with all data persisted to Neon DB to ensure scalability and reliability.

### Monorepo Structure
Frontend and Backend code reside in `frontend/` and `backend/` respectively. The project follows a monorepo structure with clear separation between frontend and backend code in dedicated directories.

### Tech Stack Compliance
Use the specified technology stack: Next.js (ChatKit), FastAPI, SQLModel, Neon DB, Gemini 1.5/2.5 Flash. All implementation must adhere to the specified tech stack requirements.

## Architecture Requirements

### Backend Implementation
- Use openai-agents SDK for Agent logic implementation
- Implement chatkit-py for stateless server handshake
- Maintain existing Gemini configuration from Phase 2 backend
- Implement all tools through official MCP servers
- Ensure all conversation history persists to Neon DB
- Maintain stateless server architecture

### Frontend Implementation
- Use Next.js with ChatKit for the frontend
- Implement proper communication with backend services
- Follow modern UI/UX principles for todo management

## Development Workflow

### Specification Requirements
- All features must have a specification in the `specs/` directory before implementation
- Specifications must include acceptance criteria and test scenarios
- Changes to architecture must be documented in the specification

### Code Review Process
- All code changes must follow the specified architecture principles
- PRs must verify compliance with all constitution principles
- Architecture decisions must be documented in ADRs when significant

### Quality Gates
- All code must pass automated testing
- MCP server integration must be verified
- Database persistence must be validated
- Statelessness requirements must be confirmed

## Governance

This constitution supersedes all other development practices for the Hackathon-Todo-Phase-3 project. All amendments to this constitution require explicit documentation, team approval, and a migration plan if applicable. All pull requests and code reviews must verify compliance with these principles. Development guidance can be found in the project documentation and CLAUDE.md files.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30