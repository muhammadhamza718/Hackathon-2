# AI-Powered Todo Chatbot with MCP Integration

An AI-powered todo management application that integrates with Model Context Protocol (MCP) servers for todo operations.

## Features

- **AI-Powered Todo Management**: Chat with an AI assistant to manage your todos
- **MCP Integration**: Uses Model Context Protocol for todo operations
- **Real-time Chat**: WebSocket-based real-time communication
- **Multi-user Support**: Separate todo lists for each user session
- **Natural Language Processing**: Understands natural language commands
- **Full CRUD Operations**: Add, list, complete, delete, and update todos
- **Monitoring & Logging**: Comprehensive monitoring and structured logging
- **Security**: Input sanitization, rate limiting, and security middleware

## Architecture

The application consists of three main components:

1. **Frontend**: Next.js application with ChatKit integration
2. **Backend**: FastAPI server with OpenAI agent integration
3. **MCP Server**: Model Context Protocol server for todo operations

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL or Neon DB
- OpenAI API key

### Installation

1. Clone the repository
2. Set up environment variables (see DEPLOYMENT.md)
3. Install dependencies for each service

### Running Locally

1. Start the MCP server:
   ```bash
   cd mcp-server
   python -c "from src.todo_operations import create_mcp_server; import asyncio; asyncio.run(create_mcp_server())"
   ```

2. Start the backend:
   ```bash
   cd backend
   python -m src.api.server
   ```

3. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

Visit `http://localhost:3000` to use the application.

## API Endpoints

### Backend API

- `GET /health` - Health check
- `GET /metrics` - Application metrics
- `POST /chat` - Synchronous chat endpoint
- `GET /chat` - WebSocket endpoint for real-time chat

### MCP Server Endpoints

- `GET /health` - Health check
- `GET /metrics` - MCP server metrics
- MCP operations via MCP protocol

## Environment Variables

See `.env.example` files in each service for required environment variables.

## Documentation

- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [API Documentation](backend/docs/api.md) - API reference (if available)
- [Architecture](docs/architecture.md) - System architecture details (if available)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[License information would go here]

## Support

For support, please check the [Deployment Guide](DEPLOYMENT.md) for troubleshooting information.