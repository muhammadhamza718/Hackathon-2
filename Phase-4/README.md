# Todo Application - Kubernetes Deployment

This repository contains the Todo application with Kubernetes deployment capabilities using Helm charts.

## Overview

The Todo application consists of:
- **Backend**: FastAPI application written in Python
- **Frontend**: Next.js application
- **Deployment**: Kubernetes manifests and Helm charts for easy deployment

## Features

- Containerized with optimized multi-stage Dockerfiles
- Kubernetes-ready with proper health checks and resource configuration
- Helm chart for easy deployment and management
- Secure by default with non-root users and secrets management
- Local development with Minikube support

## Prerequisites

- Docker
- Kubernetes cluster (Minikube for local development)
- Helm 3.x
- kubectl

## Quick Start with Minikube

### 1. Start Minikube

```bash
minikube start
eval $(minikube docker-env)
```

### 2. Build Docker Images

```bash
# Build backend
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend
cd frontend
docker build -t todo-frontend:latest .
cd ..
```

### 3. Deploy with Helm

```bash
cd helm/todo-app
helm install todo-app .
```

### 4. Access the Application

```bash
minikube service todo-frontend-service --url
```

## Architecture

### Docker Images

- **Backend**: Multi-stage build with Python 3.11-slim, non-root user, health checks
- **Frontend**: Multi-stage build with Node.js 18-alpine, non-root user, health checks

### Kubernetes Resources

- Deployments for both frontend and backend with proper resource limits
- Services for internal and external communication
- Network policies for secure communication
- ConfigMaps and Secrets for configuration management

### Helm Chart

- Parameterized values for easy customization
- Templates for all Kubernetes resources
- Proper labeling and selectors
- Health checks and readiness probes

## Configuration

The Helm chart can be customized using values in `values.yaml`:

```yaml
backend:
  image:
    repository: todo-backend
    tag: latest
  replicaCount: 1

frontend:
  image:
    repository: todo-frontend
    tag: latest
  replicaCount: 1
```

## Security

- Docker images run as non-root users
- Secrets are managed through Kubernetes Secrets
- Network policies restrict unnecessary communication
- Resource limits prevent resource exhaustion

## Local Development

For local development, see [docs/local-development-workflow.md](docs/local-development-workflow.md)

## Troubleshooting

For common issues and solutions, see [docs/troubleshooting.md](docs/troubleshooting.md)

## Deployment Guide

For detailed deployment instructions, see [docs/deployment-guide.md](docs/deployment-guide.md)

## Quality Gates

- Dockerfiles follow multi-stage build patterns
- Security best practices implemented (non-root users, minimal base images)
- Health checks and readiness probes configured
- Resource limits and requests configured
- Helm chart validated with `helm lint`

## Project Structure

```
├── backend/                 # Python FastAPI backend
│   ├── Dockerfile         # Multi-stage Dockerfile
│   └── ...
├── frontend/              # Next.js frontend
│   ├── Dockerfile         # Multi-stage Dockerfile
│   └── ...
├── helm/                  # Helm charts
│   └── todo-app/          # Todo application Helm chart
├── k8s/                   # Kubernetes manifests
│   └── base/              # Base Kubernetes resources
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update Docker images if needed
5. Test with Kubernetes
6. Submit a pull request

## License

See the LICENSE file for licensing information.