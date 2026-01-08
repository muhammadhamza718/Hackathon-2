<!-- Sync Impact Report:
Version change: N/A → 1.0.0
Added sections: Event-Driven Architecture, Distributed Runtime, Cloud Native Deployment, CI/CD Standards, Tech Stack Compatibility, Spec-Driven Rules
Templates requiring updates: ✅ Updated
Follow-up TODOs: None
-->
# Evolution of Todo Project Constitution - Phase 5

## Core Principles

### Event-Driven Architecture (NON-NEGOTIABLE)
All service communication must utilize Kafka (Redpanda/Confluent) for asynchronous messaging. Direct API calls between services are prohibited except for synchronous user-facing operations. This includes implementing event-driven patterns for reminders, recurring tasks, and audit logs to ensure loose coupling and improved scalability.

### Distributed Runtime with Dapr (NON-NEGOTIABLE)
All services must integrate with Dapr sidecars for state management, pub/sub abstraction, and secret management. Direct access to state stores, message queues, or secrets must be abstracted through Dapr components to ensure platform portability and consistent distributed system capabilities.

### Cloud Native Deployment (NON-NEGOTIABLE)
All deployments must target production Kubernetes environments (Azure AKS/GKE/OKE) instead of local Minikube. Services must be designed as cloud-native workloads with proper resource requests/limits, health checks, and readiness probes. Container images must be optimized for production deployment.

### CI/CD Standards (NON-NEGOTIABLE)
All deployments must be automated through GitHub Actions workflows. Manual deployments are prohibited except for emergency recovery. All code changes must pass through automated testing, security scanning, and deployment pipelines before reaching production environments.

### Tech Stack Compatibility (NON-NEGOTIABLE)
All new features must maintain compatibility with the existing Next.js frontend, FastAPI backend, and SQLModel/Neon DB setup from Phase-4. New dependencies must not introduce conflicts or break existing functionality. Backward compatibility must be maintained for existing APIs and data schemas.

### Spec-Driven Implementation (NON-NEGOTIABLE)
No implementation work may begin without verified tasks and updated specifications. All features must follow the spec-driven development process with clear acceptance criteria. Implementation without proper spec alignment is prohibited and will be rejected during code review.

## Architecture Standards

### Event-Driven Patterns
Services must transition from direct API calls to event-driven patterns where applicable. Event sourcing and CQRS patterns should be implemented for complex business operations. All events must follow a consistent schema and be versioned appropriately.

### Service Communication
Synchronous communication is limited to user-facing operations that require immediate response. All background processing, notifications, and cross-service data synchronization must use asynchronous event-driven patterns via Kafka/Dapr pub/sub.

## Development Workflow

### Specification Requirements
All work must begin with updated specifications in the specs/ directory. Tasks must be generated from verified specifications before implementation begins. Any deviation from the spec must result in spec updates before implementation continues.

### Testing Standards
Unit tests must cover 80%+ of new code. Integration tests must validate event-driven workflows and Dapr component interactions. End-to-end tests must verify complete user journeys across services.

### Code Review Process
All pull requests must demonstrate compliance with the constitution principles. Reviewers must verify event-driven architecture compliance, Dapr integration, and spec-driven development adherence before approval.

## Governance

This constitution supersedes all other development practices for Phase 5. All team members must acknowledge and comply with these principles. Amendments require documented justification, team approval, and migration plan for existing code. All pull requests must verify compliance with these principles; non-compliant code will be rejected.

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05