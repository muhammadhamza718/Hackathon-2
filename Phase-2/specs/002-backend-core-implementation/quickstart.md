# Quickstart Guide: Backend Core Implementation

## Prerequisites
- Python 3.11+
- Node.js (for frontend integration)
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Better Auth account/config

## Setup Instructions

### 1. Clone and Navigate to Backend
```bash
cd backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
BETTER_AUTH_SECRET=your-secret-key-here
```

### 5. Run Database Migrations
```bash
# This will be implemented as part of the backend setup
python -m backend.db.init
```

## Running the Application

### Development Mode
```bash
# Start the backend server
uvicorn main:app --reload --port 8000

# The API will be available at http://localhost:8000
```

### With Docker
```bash
# From the project root
docker-compose up --build
```

## API Endpoints

### Standard User Endpoints
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

### Admin Endpoints
- `GET /api/admin/users` - List all users (admin only)
- `GET /api/admin/users/{id}/tasks` - Get specific user's tasks (admin only)

## Authentication
All endpoints (except health checks) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

Admin endpoints additionally require the user to have `role="admin"` in their JWT token.

## Testing
```bash
# Run backend tests
pytest tests/
```

## Database Models
- **User**: id, email, name, role, created_at, updated_at
- **Task**: id, title, description, completed, user_id, created_at, updated_at

## Development Workflow
1. Create your feature branch
2. Implement changes following the specs in `specs/`
3. Write/update tests
4. Run tests to ensure everything works
5. Submit a pull request

## Troubleshooting
- If you get database connection errors, verify your DATABASE_URL is correct
- If authentication fails, check that your JWT token includes the required claims
- For role-based access issues, ensure the user has the correct role in the database