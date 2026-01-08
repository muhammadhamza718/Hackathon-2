# Data Model: Kubernetes Deployment for Todo Application

## Kubernetes Resources

### Docker Images
- **Frontend Image**: Containerized Node.js application with optimized build
  - Properties: Base image, build dependencies, runtime dependencies, build artifacts
  - Configuration: Environment variables, working directory, exposed ports

- **Backend Image**: Containerized Python application with optimized build
  - Properties: Base image, Python dependencies, application code, environment settings
  - Configuration: Environment variables, working directory, exposed ports

### Helm Chart Components
- **Chart Metadata**: Name, version, description, dependencies
- **Values Configuration**: Default and override values for deployments
- **Template Resources**: Kubernetes manifests with variable substitution

### Kubernetes Deployments
- **Backend Deployment**: Pod template for backend service
  - Properties: Container image, resource limits, environment variables, volume mounts
  - Configuration: Replicas, update strategy, health checks

- **Frontend Deployment**: Pod template for frontend service
  - Properties: Container image, resource limits, environment variables, volume mounts
  - Configuration: Replicas, update strategy, health checks

### Kubernetes Services
- **Backend Service**: Internal service for backend access
  - Properties: Service type, port, target port, selector
  - Configuration: ClusterIP, internal DNS name

- **Frontend Service**: Service for frontend access (potentially LoadBalancer or NodePort for local dev)
  - Properties: Service type, port, target port, selector
  - Configuration: External access for local development

### Kubernetes ConfigMaps
- **Application Configuration**: Non-sensitive environment configuration
  - Properties: Key-value pairs for application settings
  - Configuration: Environment-specific values

### Kubernetes Secrets
- **Sensitive Credentials**: Secure storage for secrets (API keys, auth secrets)
  - Properties: Encrypted key-value pairs for sensitive data
  - Configuration: Access permissions, encryption

### Kubernetes Ingress (Optional)
- **External Access**: Routing rules for external access
  - Properties: Host rules, path mappings, TLS configuration
  - Configuration: Path-based routing, load balancing

## Validation Rules

### Docker Build Validation
- Images must be buildable from provided Dockerfiles
- Images must contain only necessary dependencies
- Images must have appropriate security configurations

### Kubernetes Resource Validation
- All resources must have proper resource limits and requests
- Services must have appropriate selectors for deployments
- Health checks must be properly configured

### Security Validation
- Sensitive data must be stored in Secrets, not ConfigMaps
- Images must use non-root users where possible
- Network policies should restrict unnecessary communication

## State Transitions

### Deployment States
- **Pending**: Pod is created but not yet scheduled
- **Running**: Pod is scheduled and running
- **Succeeded**: Pod completed successfully (for jobs)
- **Failed**: Pod failed to complete
- **Unknown**: State could not be determined

### Service States
- **Available**: Service is ready to receive traffic
- **Degraded**: Service is partially available
- **Unavailable**: Service is not available