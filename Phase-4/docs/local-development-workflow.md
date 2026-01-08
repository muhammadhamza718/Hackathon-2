# Local Development Workflow with Kubernetes

## Overview

This document describes the local development workflow for the Todo application using Kubernetes and Minikube.

## Initial Setup

### 1. Install Prerequisites

Ensure you have the following tools installed:
- Docker
- Minikube
- kubectl
- Helm

### 2. Start Minikube

```bash
minikube start
```

### 3. Configure Docker Environment

```bash
eval $(minikube docker-env)
```

## Development Cycle

### 1. Make Code Changes

Edit source code in:
- `backend/src/` for backend changes
- `frontend/src/` for frontend changes

### 2. Build New Docker Images

```bash
# Backend
cd backend
docker build -t todo-backend:latest .

# Frontend
cd ../frontend
docker build -t todo-frontend:latest .
```

### 3. Redeploy Changes

```bash
# Option 1: Upgrade existing Helm release
helm upgrade todo-app . --reuse-values

# Option 2: If you want to do a fresh install
helm uninstall todo-app
helm install todo-app .
```

## Testing Changes

### 1. Verify Pods are Running

```bash
kubectl get pods
```

### 2. Check Application Logs

```bash
kubectl logs -l app.kubernetes.io/name=todo-backend
kubectl logs -l app.kubernetes.io/name=todo-frontend
```

### 3. Access the Application

```bash
minikube service todo-frontend-service --url
```

## Fast Iteration Tips

### 1. Use Skaffold (Optional)

For faster development cycles, consider using Skaffold which automates the build and deploy process:

```bash
skaffold dev
```

### 2. Port Forwarding for Quick Testing

Instead of exposing services, you can use port forwarding:

```bash
kubectl port-forward service/todo-frontend-service 3000:80
kubectl port-forward service/todo-backend-service 8000:8000
```

Then access the application at `http://localhost:3000`.

### 3. Hot Reload Limitations

Note that with the current containerized setup, you won't have hot reload functionality. For faster iteration during development, consider running the applications directly outside Kubernetes.

## Debugging in Kubernetes

### 1. Exec into a Pod

```bash
kubectl exec -it deployment/todo-backend-deployment -- /bin/sh
kubectl exec -it deployment/todo-frontend-deployment -- /bin/sh
```

### 2. Check Resource Usage

```bash
kubectl top pods
```

### 3. View Events

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Performance Considerations

### 1. Minikube Resources

Allocate sufficient resources to Minikube:

```bash
minikube start --memory=4096 --cpus=2
```

### 2. Image Pull Policy

The Helm chart is configured to use `IfNotPresent` pull policy to avoid pulling images unnecessarily during development.

### 3. Cleanup

When finished with development:

```bash
helm uninstall todo-app
minikube stop
```

## Troubleshooting Common Issues

### 1. Image Not Found

If you get "ImagePullBackOff" errors:
- Ensure you ran `eval $(minikube docker-env)` before building images
- Verify the image exists: `docker images | grep todo-`

### 2. Service Not Responding

Check if the pods are ready:
```bash
kubectl get pods
kubectl describe pod <pod-name>
```

### 3. Resource Constraints

If Minikube is slow or pods fail to start:
- Increase Minikube resources
- Check available disk space and memory