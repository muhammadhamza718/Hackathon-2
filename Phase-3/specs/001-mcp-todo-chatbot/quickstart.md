# Quickstart Guide: AI-Powered Todo Chatbot with MCP Integration

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Access to Neon DB (PostgreSQL-compatible serverless database)
- OpenAI API key (or access to Gemini API for free usage)
- Git for version control

## Setup Instructions

### 1. Clone and Initialize the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

#### Create Python Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Python Dependencies
```bash
pip install fastapi uvicorn openai-agents sqlmodel python-mcp psycopg2-binary python-dotenv
```

#### Set up Environment Variables
Create a `.env` file in the backend directory:
```env
NEON_DATABASE_URL=your_neon_db_connection_string
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key  # If using Gemini
MCP_SERVER_URL=http://localhost:8001  # URL for MCP server
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Node Dependencies
```bash
npm install
# or
yarn install
```

#### Set up Environment Variables
Create a `.env` file in the frontend directory:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 4. MCP Server Setup

#### Navigate to MCP Server Directory
```bash
cd mcp-server
```

#### Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install python-mcp sqlmodel psycopg2-binary python-dotenv
```

#### Set up Environment Variables
Create a `.env` file in the mcp-server directory:
```env
NEON_DATABASE_URL=your_neon_db_connection_string
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
```

## Running the Application

### 1. Start the MCP Server
```bash
cd mcp-server
python -m uvicorn src.todo_operations:app --host 0.0.0.0 --port 8001
```

### 2. Start the Backend Server
```bash
cd backend
python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8000
```

### 3. Start the Frontend Development Server
```bash
cd frontend
npm run dev
# or
yarn dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- MCP Server: http://localhost:8001

## Configuration

### Database Configuration
The application uses SQLModel with Neon DB. Make sure your `NEON_DATABASE_URL` is properly configured in both the backend and mcp-server environments.

### Agent Configuration
The agent uses the existing Gemini configuration pattern from Phase 2. The `agent.py` file will connect to the MCP server to access todo operations as tools.

### MCP Server Configuration
The MCP server exposes todo operations (add, list, complete, delete, update) as tools that the agent can access. Ensure the MCP server is running before starting the main backend.

## Key Components

### Backend Components
- `src/agents/agent.py`: OpenAI Agent with MCP integration
- `src/api/server.py`: ChatKit handshake server
- `src/models/todo.py`: Todo data model
- `src/services/todo_service.py`: Business logic for todo operations

### Frontend Components
- `src/components/TodoChat.js`: Chat interface component
- `src/components/TodoList.js`: Todo list display component
- `src/services/chatService.js`: Service for chat communication

### MCP Server Components
- `src/todo_operations.py`: MCP server implementation for todo operations
- `src/config.py`: Configuration for MCP server

## Testing the Application

1. Navigate to http://localhost:3000 in your browser
2. You should see the chat interface
3. Try sending messages like:
   - "Add a todo: Buy groceries"
   - "Show my todos"
   - "Complete the first todo"
   - "Delete the todo 'Buy groceries'"

The AI assistant should respond appropriately by calling the MCP server to perform todo operations.

## Troubleshooting

### Common Issues

1. **MCP Server Connection Error**: Ensure the MCP server is running on the correct port before starting the backend
2. **Database Connection Error**: Verify your Neon DB connection string is correct
3. **API Key Issues**: Check that your API keys are properly set in the environment variables

### Logs
- Backend logs: Check the terminal where you started the backend server
- MCP Server logs: Check the terminal where you started the MCP server
- Frontend logs: Check browser console and terminal output