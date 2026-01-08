# Quickstart: Kubernetes Deployment for Todo Application

## Prerequisites

- Docker installed and running
- Minikube installed (version 1.20 or higher)
- kubectl installed (version 1.20 or higher)
- Helm installed (version 3.x)
- kubectl-ai plugin (optional, for AI-assisted operations)
- Kagent (optional, for AI-assisted health analysis)

## Setup Local Environment

1. **Start Minikube Cluster**
   ```bash
   minikube start
   ```

2. **Verify Kubernetes Connection**
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

## Build Application Images

1. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

2. **Build Backend Docker Image**
   ```bash
   docker build -t todo-backend:latest .
   ```

3. **Navigate to Frontend Directory**
   ```bash
   cd ../frontend
   ```

4. **Build Frontend Docker Image**
   ```bash
   docker build -t todo-frontend:latest .
   ```

## Deploy Using Helm

1. **Navigate to Helm Charts Directory**
   ```bash
   cd helm/todo-app
   ```

2. **Install the Application**
   ```bash
   helm install todo-app . --values values.yaml
   ```

3. **Verify Installation**
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get deployments
   ```

## Access the Application

1. **Get Frontend Service URL**
   ```bash
   minikube service todo-frontend-service --url
   ```

2. **Or use port forwarding for development**
   ```bash
   kubectl port-forward service/todo-frontend-service 3000:80
   ```

## Alternative: Deploy Using Raw Kubernetes Manifests

1. **Navigate to Kubernetes Manifests Directory**
   ```bash
   cd k8s/base
   ```

2. **Apply Base Manifests**
   ```bash
   kubectl apply -f .
   ```

## Health Checks and Monitoring

1. **Check Pod Status**
   ```bash
   kubectl get pods
   ```

2. **Check Service Status**
   ```bash
   kubectl get services
   ```

3. **View Logs**
   ```bash
   kubectl logs deployment/todo-backend-deployment
   kubectl logs deployment/todo-frontend-deployment
   ```

4. **Using Kagent for Health Analysis** (if available)
   ```bash
   kagent analyze --component todo-backend-deployment
   ```

## Local Development Workflow

1. **Make Code Changes**
   - Edit source code in backend/src or frontend/src

2. **Rebuild Docker Images**
   ```bash
   cd backend && docker build -t todo-backend:latest .
   cd ../frontend && docker build -t todo-frontend:latest .
   ```

3. **Redeploy Changes**
   ```bash
   # Update the image tags in your deployments or use Helm upgrade
   helm upgrade todo-app . --values values.yaml
   ```

## Troubleshooting

- **Minikube Issues**: Run `minikube delete` and restart
- **Image Pull Issues**: Ensure images are built locally or pushed to registry
- **Service Not Available**: Check `kubectl describe service/todo-frontend-service`
- **Pod Failures**: Check `kubectl describe pod <pod-name>` and `kubectl logs <pod-name>`