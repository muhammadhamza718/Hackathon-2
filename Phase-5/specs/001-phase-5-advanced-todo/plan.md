# Implementation Plan: Phase-5 Advanced Todo Features

**Branch**: `001-phase-5-advanced-todo` | **Date**: 2026-01-05 | **Spec**: [specs/001-phase-5-advanced-todo/spec.md](specs/001-phase-5-advanced-todo/spec.md)
**Input**: Feature specification from `/specs/001-phase-5-advanced-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of advanced todo features including recurring tasks, due dates, reminders, and search/filter/sort capabilities using event-driven architecture with Kafka and Dapr. The system will maintain backward compatibility with existing Phase-4 functionality while introducing specialized microservices for notification, recurring tasks, and audit logging.

## Technical Context

**Language/Version**: Python 3.11, Next.js 14, TypeScript 5.0
**Primary Dependencies**: FastAPI, SQLModel, Dapr, Kafka/Redpanda, Neon PostgreSQL
**Storage**: Neon PostgreSQL with Dapr state store abstraction
**Testing**: pytest, Jest, Playwright for E2E testing
**Target Platform**: Kubernetes (Azure AKS/GKE/OKE)
**Project Type**: Web application with backend API and frontend UI
**Performance Goals**: Handle 10,000+ tasks with search returning results in under 1 second
**Constraints**: Must maintain 99.9% uptime for reminder delivery service, maintain backward compatibility with Phase-4
**Scale/Scope**: Support 1000+ concurrent users with recurring tasks and notification services

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Event-Driven Architecture: All service communication will use Kafka for asynchronous messaging
- [x] Distributed Runtime with Dapr: All services will integrate with Dapr sidecars
- [x] Cloud Native Deployment: Kubernetes deployment strategy will be implemented
- [x] CI/CD Standards: GitHub Actions workflows will be established
- [x] Tech Stack Compatibility: Maintains compatibility with Next.js, FastAPI, SQLModel/Neon DB
- [x] Spec-Driven Implementation: Following the spec from spec.md
- [x] Event-Driven Patterns: Transitioning from direct API calls to event-driven patterns
- [x] Service Communication: Using Kafka/Dapr pub/sub for background processing

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-5-advanced-todo/
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
│   ├── models/
│   │   ├── task.py              # Updated with advanced fields
│   │   └── recurring_task.py    # New recurring task model
│   ├── services/
│   │   ├── task_service.py      # Updated with advanced logic
│   │   ├── recurring_service.py # New recurring task service
│   │   ├── notification_service.py # New notification service
│   │   └── audit_service.py     # New audit service
│   ├── api/
│   │   ├── v1/
│   │   │   ├── tasks.py         # Updated endpoints
│   │   │   └── recurring.py     # New recurring endpoints
│   │   └── dapr/
│   │       └── dapr_handlers.py # Dapr integration
│   └── events/
│       ├── task_events.py       # Kafka event schemas
│       └── event_publisher.py   # Event publishing logic
├── dapr/
│   ├── components/
│   │   ├── statestore.yaml      # Dapr state store config
│   │   ├── pubsub.yaml          # Dapr pub/sub config
│   │   └── secrets.yaml         # Dapr secrets config
│   └── config.yaml              # Dapr configuration
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── TaskFormAdvanced.tsx # Advanced task form with date pickers
│   │   ├── TaskListAdvanced.tsx # Enhanced task list with search/filter/sort
│   │   └── RecurringTaskForm.tsx # Recurring task configuration
│   ├── pages/
│   │   └── dashboard/
│   │       └── index.tsx        # Updated dashboard
│   └── services/
│       └── api.ts               # Updated API service
├── package.json
└── Dockerfile

k8s/
├── base/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── dapr-components/
│   │   ├── statestore.yaml
│   │   ├── pubsub.yaml
│   │   └── secrets.yaml
│   ├── kafka/
│   │   └── redpanda.yaml
│   └── monitoring/
│       └── service-monitor.yaml
├── overlays/
│   ├── dev/
│   └── prod/
│       ├── backend-deployment.yaml
│       ├── frontend-deployment.yaml
│       └── kustomization.yaml
└── helm/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── backend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── hpa.yaml
    │   ├── frontend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── ingress.yaml
    │   ├── kafka/
    │   │   └── redpanda.yaml
    │   ├── dapr/
    │   │   └── components.yaml
    │   └── _helpers.tpl
    └── charts/

.infrastructure/
├── docker-compose.yml           # For local development with Kafka/Dapr
├── docker-compose.prod.yml      # Production-like setup
└── terraform/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf

.github/
└── workflows/
    ├── ci.yml                   # CI workflow
    ├── cd.yml                   # CD workflow
    └── security.yml             # Security scanning
```

**Structure Decision**: Multi-service architecture with backend API, frontend UI, and specialized microservices for notifications, recurring tasks, and audit logging. Dapr components for state management and pub/sub. Kubernetes manifests with Helm charts for deployment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple services | Required by spec for specialized functionality | Single service would violate event-driven architecture principle |
| Dapr integration | Required by constitution for distributed runtime | Direct access to state stores would violate constitution |
| Kafka/Redpanda | Required by constitution for event-driven architecture | Direct API calls prohibited by constitution |