<!-- Sync Impact Report:
     Version change: N/A -> 1.0.0
     Modified principles: N/A (Initial Phase 4 Constitution)
     Added sections: Core Principles, Architecture Requirements, Development Workflow
     Removed sections: N/A
     Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md
     Follow-up TODOs: TODO(RATIFICATION_DATE): Confirm final adoption date.
-->

# Hackathon-Todo-Phase-4 Constitution

## Core Principles

### I. Spec-Driven Infrastructure

No infrastructure changes (Dockerfiles, Helm Charts, K8s Manifests) are implemented without a validated specification in the `specs/` directory. All DevOps tasks must map to a specific task ID.

### II. Multi-Stage Containerization

Every service (Frontend, FastAPI Backend, and MCP Server) must be containerized using multi-stage, production-grade Dockerfiles to ensure minimal image size and maximum security.

### III. Internal Service Discovery

Services MUST communicate using Kubernetes internal DNS (e.g., `http://backend-service:8000`) instead of `localhost`. This ensures resilience and proper routing within the clustered environment.

### IV. K8s-Native Secret Management

Sensitive data (Better Auth secrets, Database URLs, API keys) must be managed via Kubernetes Secrets. Hardcoding credentials in environment variables or configuration files is strictly prohibited.

### V. Stateless Scalability

The backend must remain strictly stateless, relying on external services (Neon DB) for persistence. This allows any pod to handle any request, facilitating horizontal pod autoscaling.

### VI. Tenant Isolation & Auth Proxy

Maintain strict multi-user isolation. The Better Auth JWT verification must be enforced at the backend gateway level, ensuring that every request is tied to a verified `user_id`.

## Infrastructure Requirements

### Containerization

- Use `python:3.11-slim` or similar for backend to minimize footprint.
- Use `node:18-alpine` for frontend builds.
- Implement `.dockerignore` to exclude development artifacts.

### Orchestration (Local K8s)

- Use Helm Charts for all deployments.
- Deploy targeting Minikube using local image loading (`minikube image load`).
- Define clear Resource Limits/Requests for all Pods.

## Development Workflow

### Quality Gates

- All Dockerfiles must pass security linting.
- All Helm Charts must be validated via `helm lint` before deployment.
- Inter-service connectivity must be verified via health checks in the cluster.

## Governance

This constitution supersedes all previous phase rules. Amendments require a semantic version bump and a Sync Impact Report.

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02

<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
