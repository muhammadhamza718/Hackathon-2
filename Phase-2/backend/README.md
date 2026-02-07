---
title: Backend API
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Todo App Backend (Phase II)

This is the FastAPI-based backend for the Phase II Todo Application. It provides a secure REST API with JWT-based authentication and Role-Based Access Control (RBAC).

## 🚀 Technology Stack

- **FastAPI**: Modern, high-performance web framework for building APIs with Python.
- **SQLModel**: An ORM that combines the power of SQLAlchemy with the simplicity of Pydantic.
- **Better Auth Integration**: Backend integration with the Next.js Better Auth system for shared authentication state.
- **Neon PostgreSQL**: Serverless PostgreSQL for persistent storage.
- **JWT (Python-jose)**: Secure token verification and data isolation.

## 🔐 Security & Authentication

The backend verifies JWT tokens issued by Better Auth.

- **Shared Secret**: The `BETTER_AUTH_SECRET` must be identical in both frontend and backend.
- **User Isolation**: All task-related endpoints are prefixed with `{user_id}`. The backend verifies that the token's `sub` claim matches the URL parameter.
- **RBAC**: Administrator access is controlled via a `role` field in the `user` table.

## 🗺️ API Endpoints

### 📍 General Endpoints

- `GET /health`: Health check endpoint to verify service status.
- `GET /`: Welcome message.

### 📍 Task Endpoints (`/api`)

All task endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.

- `GET /api/{user_id}/tasks`: List all tasks for the specific user.
- `POST /api/{user_id}/tasks`: Create a new task for the user.
- `GET /api/{user_id}/tasks/{id}`: Get details for a specific task.
- `PUT /api/{user_id}/tasks/{id}`: Update a task.
- `DELETE /api/{user_id}/tasks/{id}`: Delete a task.
- `PATCH /api/{user_id}/tasks/{id}/complete`: Toggle task completion status.

### 📍 Admin Endpoints (`/api/admin`)

Requires a valid JWT token with the `admin` role.

- `GET /api/admin/users`: List all registered users.
- `GET /api/admin/users/{user_id}/tasks`: View tasks for any specific user.

## ⚙️ Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your_32_char_secret_key
ADMIN_USER_ID=your_auth_user_id_for_promotion
```

## 🛠️ Running Locally

1. **Setup Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Start Server**:
   ```bash
   uvicorn main:app --port 8000 --reload
   ```
