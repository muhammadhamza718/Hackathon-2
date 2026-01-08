# Todo Application Helm Chart

This Helm chart deploys the Todo application with both frontend and backend services to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `todo-app`:

```bash
helm install todo-app .
```

To install with custom values:

```bash
helm install todo-app . --values values.yaml
```

## Uninstalling the Chart

To uninstall/delete the `todo-app` release:

```bash
helm delete todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.replicaCount` | Number of backend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `ingress.enabled` | Enable ingress | `false` |

## Local Development

For local development with Minikube:

1. Start Minikube:
   ```bash
   minikube start
   ```

2. Build and load your Docker images:
   ```bash
   eval $(minikube docker-env)
   cd ../backend && docker build -t todo-backend:latest .
   cd ../frontend && docker build -t todo-frontend:latest .
   ```

3. Install the chart:
   ```bash
   helm install todo-app .
   ```

4. Access the application:
   ```bash
   minikube service todo-frontend-service
   ```