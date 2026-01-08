# Quickstart: Phase-5 Advanced Todo Features

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube for development, AKS/GKE for production)
- Dapr CLI installed
- Node.js 18+ and npm/yarn
- Python 3.11+ with pip

## Local Development Setup

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dapr

```bash
dapr init
```

### 3. Start Local Infrastructure

```bash
# Start Kafka/Redpanda, PostgreSQL, and other services
docker-compose up -d
```

### 4. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
# Run database migrations
python -m db.migrate
# Start the backend service with Dapr
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 -- python main.py
```

### 5. Set Up Frontend

```bash
cd frontend
npm install
npm run dev
```

## Key Components

### Backend Services
- **todo-backend**: Main API service with advanced task features
- **notification-service**: Handles sending notifications and reminders
- **recurring-task-service**: Manages recurring task generation
- **audit-service**: Logs all operations for compliance

### Dapr Components
- **State Store**: For persisting application state
- **Pub/Sub**: For event-driven communication between services
- **Secret Store**: For managing sensitive configuration

### Event Streams
- **task-events**: Stream for task lifecycle events
- **reminder-events**: Stream for reminder scheduling
- **audit-events**: Stream for audit logging

## API Endpoints

### Tasks API
- `GET /api/v1/tasks` - List tasks with search, filter, sort
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task

### Recurring Tasks API
- `GET /api/v1/recurring-tasks` - List recurring task templates
- `POST /api/v1/recurring-tasks` - Create a recurring task template
- `PUT /api/v1/recurring-tasks/{id}` - Update a template
- `DELETE /api/v1/recurring-tasks/{id}` - Delete a template

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Kafka/Redpanda
KAFKA_BROKERS=localhost:9092

# Dapr
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001

# Notification settings
EMAIL_SERVICE_URL=http://email-service:3000
PUSH_SERVICE_URL=http://push-service:3000
```

## Validation Commands

### Backend Validation
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run contract tests
python -m pytest tests/contract/
```

### Frontend Validation
```bash
# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e
```

### Dapr Validation
```bash
# Check Dapr status
dapr status -k

# View Dapr dashboard
dapr dashboard
```

## Kubernetes Deployment

### Local (Minikube)
```bash
minikube start
kubectl apply -f k8s/base/
```

### Production
```bash
# Apply production configuration
kubectl apply -f k8s/overlays/prod/
```

## Troubleshooting

### Common Issues

1. **Dapr sidecar not starting**: Ensure Dapr is properly initialized and the sidecar is configured in your deployment manifests.

2. **Kafka connection issues**: Verify that Kafka/Redpanda is running and accessible from your services.

3. **Database migration failures**: Check database connection settings and ensure the database is accessible.

4. **Event processing delays**: Monitor Kafka consumer lag and Dapr pub/sub components.