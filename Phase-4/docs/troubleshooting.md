# Troubleshooting Guide for Kubernetes Deployment

## Common Issues and Solutions

### 1. ImagePullBackOff Error

**Symptoms**: Pods stuck in "ImagePullBackOff" status

**Causes and Solutions**:
- **Minikube not configured**: Ensure you ran `eval $(minikube docker-env)` before building images
- **Image doesn't exist**: Verify the image exists locally with `docker images | grep todo-`
- **Wrong image tag**: Check that your Helm values match the built image tags

**Solution**:
```bash
# Make sure Minikube docker environment is set
eval $(minikube docker-env)

# Build images again
cd backend && docker build -t todo-backend:latest .
cd ../frontend && docker build -t todo-frontend:latest .

# Redeploy
helm upgrade todo-app . --reuse-values
```

### 2. Pod Stuck in "ContainerCreating" or "Pending" State

**Symptoms**: Pods never reach "Running" state

**Causes and Solutions**:
- **Insufficient resources**: Minikube may not have enough memory/CPU allocated
- **Persistent volume issues**: Storage claims not being satisfied
- **Image pull secrets**: Private registry access issues

**Solution**:
```bash
# Check pod status and events
kubectl describe pod <pod-name>

# Check resource allocation
kubectl top nodes

# Restart with more resources
minikube delete
minikube start --memory=4096 --cpus=2
```

### 3. Service Not Accessible

**Symptoms**: Cannot access application via service URL

**Causes and Solutions**:
- **Pods not ready**: Application not starting properly
- **Service configuration**: Port mismatch or selector issues
- **Ingress not configured**: For external access

**Solution**:
```bash
# Check if pods are running and ready
kubectl get pods

# Verify service configuration
kubectl get services
kubectl describe service todo-frontend-service

# Test internal connectivity
kubectl exec -it <pod-name> -- nslookup todo-backend-service

# For Minikube, get service URL
minikube service todo-frontend-service --url
```

### 4. Application Startup Errors

**Symptoms**: Pods crash or restart continuously

**Causes and Solutions**:
- **Missing environment variables**: Secrets or ConfigMaps not mounted
- **Database connection failures**: Network issues or wrong connection strings
- **Health check failures**: Application not responding to health endpoints

**Solution**:
```bash
# Check application logs
kubectl logs -l app.kubernetes.io/name=todo-backend
kubectl logs -l app.kubernetes.io/name=todo-frontend

# Check environment variables
kubectl exec -it <pod-name> -- env

# Check if health endpoints are accessible
kubectl exec -it <pod-name> -- curl localhost:8000/health
```

### 5. Database Connection Issues

**Symptoms**: Backend fails to connect to database

**Causes and Solutions**:
- **Secret not configured**: Database URL not properly set
- **Network issues**: Service name resolution problems
- **Database not running**: External database unavailable

**Solution**:
```bash
# Check if database secret exists
kubectl get secrets

# Verify secret contents (decode from base64)
kubectl get secret db-secret -o yaml

# Test database connectivity from backend pod
kubectl exec -it <backend-pod> -- ping <db-host>
```

### 6. Authentication Issues

**Symptoms**: Users cannot authenticate or API returns 401 errors

**Causes and Solutions**:
- **Auth secret missing**: BETTER_AUTH_SECRET not properly configured
- **JWT token issues**: Token validation problems
- **Configuration mismatch**: Auth settings between frontend and backend

**Solution**:
```bash
# Verify auth secret exists and is properly configured
kubectl get secret auth-secret -o yaml

# Check if the secret is mounted in the backend pod
kubectl describe pod <backend-pod> | grep -A 10 -B 10 auth-secret
```

## Debugging Commands

### General Status Checks
```bash
# Overall cluster status
kubectl cluster-info

# All pods in all namespaces
kubectl get pods --all-namespaces

# Events for troubleshooting
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Pod-Specific Debugging
```bash
# Detailed pod information
kubectl describe pod <pod-name>

# Pod logs with timestamps
kubectl logs <pod-name> --timestamps

# Follow logs in real-time
kubectl logs -f <pod-name>

# Execute commands in running pod
kubectl exec -it <pod-name> -- /bin/sh
```

### Service and Network Debugging
```bash
# Service configuration
kubectl describe service <service-name>

# Endpoint information
kubectl get endpoints <service-name>

# Network connectivity test
kubectl run debug --image=nicolaka/netshoot -it --rm -- bash
```

## Helm-Specific Issues

### Chart Installation Failures
```bash
# Validate chart syntax
helm lint .

# Dry-run installation
helm install todo-app . --dry-run --debug

# Check what would be deployed
helm template todo-app .
```

### Upgrade Issues
```bash
# Check release status
helm status todo-app

# Rollback to previous version
helm rollback todo-app

# Check history of releases
helm history todo-app
```

## Resource Optimization

### Check Resource Usage
```bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes

# Get resource limits and requests
kubectl describe pod <pod-name> | grep -A 10 Resources
```

### Adjust Resource Limits
Update values.yaml to modify resource constraints:
```yaml
backend:
  resources:
    requests:
      memory: "256Mi"
      cpu: "200m"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

## Performance Troubleshooting

### Slow Application Response
- Check if pods are using too much CPU/memory
- Verify database connection performance
- Check for network latency between services

### High Memory Usage
- Review application memory configuration
- Check for memory leaks
- Adjust resource limits appropriately

### Deployment Rollout Issues
```bash
# Check rollout status
kubectl rollout status deployment/<deployment-name>

# Check rollout history
kubectl rollout history deployment/<deployment-name>

# Undo rollout if needed
kubectl rollout undo deployment/<deployment-name>
```

## Minikube-Specific Issues

### Minikube Not Starting
```bash
# Clear Minikube state
minikube delete

# Start with specific driver
minikube start --driver=docker

# Check Minikube status
minikube status
```

### Docker Environment Issues
```bash
# Verify Docker environment is set
docker images

# Reset Docker environment
eval $(minikube docker-env)
```