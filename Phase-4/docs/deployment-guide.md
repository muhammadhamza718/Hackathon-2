# Kubernetes Deployment Guide for Todo Application

## Overview

This guide provides instructions for deploying the Todo application to Kubernetes using Helm charts. The application consists of a frontend (Next.js) and backend (FastAPI) service.

## Prerequisites

- Docker installed and running
- Minikube installed (version 1.20 or higher) or access to a Kubernetes cluster
- kubectl installed (version 1.20 or higher)
- Helm installed (version 3.x)

## Local Development Setup with Minikube

### 1. Start Minikube Cluster

```bash
minikube start
```

### 2. Set Docker Environment to Minikube

```bash
eval $(minikube docker-env)
```

This ensures that Docker images built locally are available to the Minikube cluster.

### 3. Build Docker Images

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .
```

## Deploying with Helm

### 1. Navigate to Helm Chart Directory

```bash
cd helm/todo-app
```

### 2. Install the Application

```bash
helm install todo-app .
```

### 3. Verify Installation

```bash
kubectl get pods
kubectl get services
kubectl get deployments
```

### 4. Access the Application

```bash
minikube service todo-frontend-service --url
```

## Configuration

### Custom Values

You can customize the deployment by creating a `values.yaml` file with your custom settings and installing with:

```bash
helm install todo-app . --values your-values.yaml
```

### Secrets Management

Sensitive information like database URLs and authentication secrets are managed through Kubernetes Secrets. The Helm chart includes templates for creating these secrets.

Example secret configuration in values.yaml:
```yaml
secrets:
  db-secret:
    data:
      database-url: <base64-encoded-database-url>
  auth-secret:
    data:
      secret: <base64-encoded-auth-secret>
```

## Upgrading the Application

To upgrade the application with new images or configuration:

```bash
# Update your Docker images
docker build -t todo-backend:new-version .
docker build -t todo-frontend:new-version .

# Upgrade the Helm release
helm upgrade todo-app . --set backend.image.tag=new-version,frontend.image.tag=new-version
```

## Health Checks and Monitoring

### Check Pod Status

```bash
kubectl get pods
```

### Check Service Status

```bash
kubectl get services
```

### View Logs

```bash
kubectl logs deployment/todo-backend-deployment
kubectl logs deployment/todo-frontend-deployment
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure you've run `eval $(minikube docker-env)` before building images
2. **Service not accessible**: Check if the pods are running and the service is correctly configured
3. **Database connection errors**: Verify that the database secret is correctly configured

### Debugging Commands

```bash
# Describe a pod for detailed information
kubectl describe pod <pod-name>

# Get detailed service information
kubectl describe service todo-frontend-service

# Check deployment status
kubectl rollout status deployment/todo-backend-deployment
```

## Resource Configuration

The Helm chart includes resource limits and requests for both frontend and backend services:

- Backend: 128Mi-512Mi memory, 100m-500m CPU
- Frontend: 64Mi-256Mi memory, 50m-200m CPU

These can be adjusted in the `values.yaml` file according to your needs.

## Security Considerations

1. Images run as non-root users
2. Secrets are stored using Kubernetes Secrets
3. Network policies can be added for additional security
4. Health checks are implemented for both services

## Quality Gates

- All Dockerfiles follow multi-stage build patterns
- Helm charts are validated using `helm lint`
- Health checks are implemented for both services
- Resource limits and requests are configured