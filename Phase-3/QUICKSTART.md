# Todo Chatbot Quickstart Guide

Welcome to the AI-Powered Todo Chatbot with MCP Integration! This guide will help you set up and run the application quickly.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Setup](#quick-setup)
3. [Running with Docker](#running-with-docker)
4. [Manual Setup](#manual-setup)
5. [Environment Configuration](#environment-configuration)
6. [First Steps](#first-steps)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before getting started, ensure you have:

- **Python 3.9+** installed
- **Node.js 18+** installed
- **PostgreSQL** or **Neon DB** account
- **Docker** and **Docker Compose** (recommended)
- **OpenAI API Key** (for Gemini integration)

### Verify Prerequisites

```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check Docker (if using containerized deployment)
docker --version
docker-compose --version
```

## Quick Setup (Recommended)

### Option 1: Using Docker Compose (Easiest)

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Phase-3
```

2. **Set up environment variables:**
```bash
# Copy the example environment files
cp backend/.env.example backend/.env
cp mcp-server/.env.example mcp-server/.env
cp frontend/.env.example frontend/.env
```

3. **Update environment variables:**
Edit the `.env` files with your actual configuration:
- `OPENAI_API_KEY` in backend/.env
- `DATABASE_URL` in backend/.env and mcp-server/.env

4. **Start all services:**
```bash
docker-compose up --build
```

5. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- MCP Server: http://localhost:8000

### Option 2: Manual Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Phase-3
```

2. **Set up the database:**
```bash
# Create PostgreSQL database or Neon DB
# Update DATABASE_URL in backend/.env and mcp-server/.env
```

3. **Install backend dependencies:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Install MCP server dependencies:**
```bash
cd ../mcp-server
pip install -r requirements.txt
```

5. **Install frontend dependencies:**
```bash
cd ../frontend
npm install
```

6. **Start all services:**
```bash
# Terminal 1: Start MCP Server
cd mcp-server
python -c "from src.todo_operations import create_mcp_server; import asyncio; asyncio.run(create_mcp_server())"

# Terminal 2: Start Backend
cd backend
python -m src.api.server

# Terminal 3: Start Frontend
cd frontend
npm run dev
```

## Environment Configuration

### Backend Configuration (backend/.env)

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot

# OpenAI/Gemini Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=8001
LOG_LEVEL=INFO

# MCP Server
MCP_SERVER_URL=http://localhost:8000
```

### MCP Server Configuration (mcp-server/.env)

```env
# Database Configuration (should match backend)
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration (frontend/.env)

```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8000
```

## Available Scripts

### Backend
- `python -m src.api.server` - Start the backend server
- Health check: `GET /health`
- Metrics: `GET /metrics`
- Ready check: `GET /ready`

### MCP Server
- `python -c "from src.todo_operations import create_mcp_server; import asyncio; asyncio.run(create_mcp_server())"` - Start MCP server
- Health check: `GET /health` (via HTTP extension)
- Metrics: `GET /metrics` (via HTTP extension)

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- Health check: `GET /api/health`
- Ready check: `GET /api/ready`

## First Steps

### 1. Verify Services Are Running

Check that all services are healthy:

```bash
# Backend health
curl http://localhost:8001/health

# MCP Server health (when HTTP extensions are available)
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000/api/health
```

Expected response format:
```json
{
  "status": "healthy",
  "service": "todo-chatbot-api",
  "timestamp": "2025-01-01T00:00:00.000000",
  "response_time_ms": 15.23,
  "checks": {
    "database": "healthy",
    "mcp_server": "healthy"
  }
}
```

### 2. Interact with the Chatbot

1. Open your browser to `http://localhost:3000`
2. Start chatting with the AI assistant:
   - "Add a new todo: Buy groceries"
   - "List all my todos"
   - "Complete todo 1"
   - "Delete todo 2"
   - "Update todo 3 to 'Buy milk and bread'"

### 3. API Usage Examples

#### Add a Todo
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a new todo: Learn MCP integration"}'
```

#### List Todos
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "List all my todos"}'
```

## Key Features

### MCP Integration
- Todo operations are handled via Model Context Protocol
- Separated concerns between AI agent and data operations
- Scalable architecture for future MCP tools

### Real-time Chat
- WebSocket support for real-time interaction
- ChatKit-style handshake for frontend integration
- Concurrent user support

### Advanced Capabilities
- Natural language processing for todo management
- Smart completion and categorization
- Context-aware responses
- Error recovery and user feedback

### Monitoring & Health
- Comprehensive health checks
- Performance metrics
- Structured logging
- Caching for performance

## Troubleshooting

### Common Issues

#### Issue: Database Connection Error
**Symptoms:** Error connecting to database
**Solution:**
1. Verify `DATABASE_URL` is correct
2. Check that PostgreSQL/Neon DB is running
3. Ensure credentials are valid

#### Issue: MCP Server Not Responding
**Symptoms:** Timeout or connection refused errors
**Solution:**
1. Verify MCP server is running on port 8000
2. Check `MCP_SERVER_URL` in backend configuration
3. Ensure network connectivity between services

#### Issue: Frontend Can't Connect to Backend
**Symptoms:** Network errors in browser console
**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` is set correctly
2. Check CORS configuration
3. Ensure backend is running on specified port

#### Issue: OpenAI API Errors
**Symptoms:** Authentication errors or rate limits
**Solution:**
1. Verify `OPENAI_API_KEY` is valid
2. Check API quota and billing
3. Ensure proper internet connectivity

### Debugging Commands

#### Check Service Status
```bash
# Check running containers (Docker)
docker-compose ps

# Check logs (Docker)
docker-compose logs backend
docker-compose logs mcp-server
docker-compose logs frontend
```

#### Test Endpoints
```bash
# Test health endpoints
curl -v http://localhost:8001/health
curl -v http://localhost:3000/api/health

# Test database connection
python -c "from backend.src.models.database import get_sync_session; print('DB Connection OK' if get_sync_session() else 'DB Connection Failed')"
```

### Getting Help

1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup instructions
2. Review the [README.md](README.md) for architecture overview
3. Examine the [config/](config/) directory for environment-specific settings
4. Check service logs for detailed error information

## Next Steps

1. **Customize the bot** - Modify prompts in `backend/src/agents/agent.py`
2. **Extend functionality** - Add new MCP operations in `mcp-server/src/todo_operations.py`
3. **Enhance UI** - Update components in `frontend/src/components/`
4. **Scale deployment** - Review production configuration in `config/production.json`

## Support

For additional help:
- Check the service health endpoints
- Review the logs in the `logs/` directory
- Verify all environment variables are set correctly
- Ensure all prerequisites are properly installed

---

Happy coding! Your AI-powered Todo Chatbot with MCP Integration is now ready to use.