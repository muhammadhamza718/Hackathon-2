# Todo Chatbot Deployment Guide

This document provides instructions for running and deploying the AI-powered Todo Chatbot with MCP integration.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Environment Configuration](#environment-configuration)
4. [Running Locally](#running-locally)
5. [Running with Docker](#running-with-docker)
6. [Configuration Management](#configuration-management)
7. [Health Checks](#health-checks)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Production Deployment](#production-deployment)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+ (or use Neon DB for cloud deployment)
- Docker and Docker Compose (optional, for containerized deployment)
- OpenAI API key (for Gemini integration)
- MCP Server compatible client

## Project Structure

```
Phase-3/
├── backend/                 # Backend API with FastAPI
│   ├── src/
│   │   ├── agents/         # AI agent implementation
│   │   ├── api/            # API endpoints (ChatKit handshake)
│   │   ├── models/         # Database models (SQLModel)
│   │   ├── services/       # Business logic
│   │   ├── config/         # Configuration and logging
│   │   ├── monitoring/     # Monitoring utilities
│   │   └── middleware/     # Security middleware
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   └── services/       # Frontend services
│   └── package.json
├── mcp-server/             # Model Context Protocol server
│   └── src/
│       ├── todo_operations.py  # Todo MCP operations
│       └── database_service.py # Optimized database service
├── docker-compose.yml      # Docker configuration
└── .env.example            # Environment variable examples
```

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
NEON_DB_URL=your_neon_db_url_here

# OpenAI/Gemini Configuration
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_MODEL=gemini-2.5-flash-001  # or gemini-2.0-flash

# MCP Server Configuration
MCP_SERVER_URL=http://localhost:8000

# Application Configuration
PORT=8001
LOG_LEVEL=INFO
LOG_FORMAT_JSON=false

# Security Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8000
```

### MCP Server Environment Variables

The MCP server uses the same `.env` file as the backend for database configuration.

## Running Locally

### Backend

1. Navigate to the backend directory:
```bash
cd Phase-3/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (see above)

5. Run the backend server:
```bash
python -m src.api.server
```

The backend will start on `http://localhost:8001`

### MCP Server

1. Navigate to the MCP server directory:
```bash
cd Phase-3/mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the MCP server:
```bash
python -c "from src.todo_operations import create_mcp_server; import asyncio; asyncio.run(create_mcp_server())"
```

The MCP server will start on `http://localhost:8000`

### Frontend

1. Navigate to the frontend directory:
```bash
cd Phase-3/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Running with Docker

### Using Docker Compose

1. Ensure Docker and Docker Compose are installed

2. Navigate to the project root:
```bash
cd Phase-3
```

3. Create a `.env` file with all required environment variables

4. Build and run the services:
```bash
docker-compose up --build
```

This will start all services:
- Backend API: `http://localhost:8001`
- MCP Server: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Individual Service Docker Commands

To build and run individual services:

**Backend:**
```bash
cd Phase-3/backend
docker build -t todo-backend .
docker run -p 8001:8001 -e DATABASE_URL=... -e OPENAI_API_KEY=... todo-backend
```

**MCP Server:**
```bash
cd Phase-3/mcp-server
docker build -t mcp-server .
docker run -p 8000:8000 -e DATABASE_URL=... mcp-server
```

**Frontend:**
```bash
cd Phase-3/frontend
docker build -t todo-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=... todo-frontend
```

## Configuration Management

### Environment-specific Configurations

The application supports multiple environment configurations through environment variables:

- **Development**: Use local database and API keys
- **Staging**: Use staging database and test API keys
- **Production**: Use production database and production API keys

### Configuration Files

- `backend/src/config/logging_config.py` - Logging configuration
- `backend/src/monitoring/metrics.py` - Metrics collection
- `backend/src/middleware/security.py` - Security middleware
- `docker-compose.yml` - Docker configuration

### Feature Flags

The application supports feature flags through environment variables:
- `ENABLE_CACHING` - Enable/disable caching (default: true)
- `ENABLE_LOGGING` - Enable/disable detailed logging (default: true)
- `LOG_FORMAT_JSON` - Format logs as JSON (default: false)

## Health Checks

### Backend Health Endpoints

- `GET /health` - Basic health check
- `GET /metrics` - Application metrics
- `GET /` - Root endpoint verification

### MCP Server Health Endpoints

- `GET /health` - Basic health check
- `GET /metrics` - MCP server metrics

### Health Check Implementation

Health checks verify:
- Database connectivity
- MCP server connectivity
- Required services availability
- System resource usage

## Monitoring and Logging

### Log Management

The application provides structured logging with the following features:

- **Centralized Logging**: All services use centralized logging configuration
- **JSON Format**: Optional JSON-formatted logs for better parsing
- **Log Levels**: Support for DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation**: Automatic log rotation to prevent disk space issues

### Metrics Collection

The application collects the following metrics:

**Backend Metrics:**
- API request counts
- Response times
- Error rates
- Active connections
- Database operation times

**MCP Server Metrics:**
- Operation counts
- Response times
- Error rates
- Database operation times

### Log Locations

- Backend logs: `logs/todo_chatbot.log`
- MCP server logs: `logs/mcp_todo_server.log`
- Frontend logs: Console output (browser dev tools)

## Production Deployment

### Recommended Infrastructure

- **Database**: Neon Serverless PostgreSQL or AWS RDS
- **Backend**: Containerized deployment with Kubernetes or AWS ECS
- **Frontend**: Static hosting (Vercel, Netlify, or AWS S3 + CloudFront)
- **Load Balancer**: AWS ALB or Nginx
- **Monitoring**: Prometheus + Grafana or AWS CloudWatch

### Deployment Steps

1. **Database Setup**
   - Set up Neon DB or PostgreSQL instance
   - Configure connection pooling
   - Set up backup and monitoring

2. **Backend Deployment**
   - Build Docker images
   - Deploy to container orchestration platform
   - Configure environment variables
   - Set up health checks and monitoring

3. **Frontend Deployment**
   - Build static assets
   - Deploy to CDN or static hosting
   - Configure domain and SSL

4. **MCP Server Deployment**
   - Deploy as separate service
   - Configure connection to database
   - Set up monitoring

### Security Considerations

- Use HTTPS for all communications
- Implement proper authentication and authorization
- Rotate API keys regularly
- Implement rate limiting
- Use environment variables for secrets
- Regular security scanning

## Troubleshooting

### Common Issues

**Issue**: Database connection errors
**Solution**: Verify DATABASE_URL is correct and database is accessible

**Issue**: MCP server not responding
**Solution**: Check MCP_SERVER_URL configuration and ensure MCP server is running

**Issue**: Frontend can't connect to backend
**Solution**: Verify API URL configuration and CORS settings

**Issue**: Slow response times
**Solution**: Check database performance, enable caching, optimize queries

### Debugging Steps

1. Check application logs for error messages
2. Verify all environment variables are set correctly
3. Test database connectivity separately
4. Verify MCP server is accessible
5. Check network connectivity between services

### Log Analysis

For performance issues, check:
- Response times in metrics
- Database operation times
- API request patterns
- Memory and CPU usage

For errors, check:
- Error counts and types
- Stack traces in logs
- Correlation between services
- Recent configuration changes

## Support

For support, please:
1. Check the logs for error messages
2. Verify configuration settings
3. Test connectivity between services
4. Contact the development team if issues persist