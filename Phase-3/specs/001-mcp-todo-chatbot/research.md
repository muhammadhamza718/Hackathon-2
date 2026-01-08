# Research: AI-Powered Todo Chatbot with MCP Integration

## MCP (Model Context Protocol) Python SDK Implementation

### Key Findings
- MCP is a protocol that allows AI models to access external tools and resources securely
- The Python SDK provides tools to create MCP servers that can be connected to AI agents
- MCP servers expose tools as endpoints that agents can call during conversations
- The protocol handles authentication, tool discovery, and secure communication

### Implementation Patterns
- Create an MCP server using the official Python SDK
- Define tools as functions with proper type hints and descriptions
- Use the mcp.server decorator to register tools
- Handle errors gracefully and provide meaningful error messages

## Existing Architecture from @[02_Backend]

### Agent Implementation (agent.py)
- Uses OpenAI Agents SDK to create AI assistants
- Implements Gemini configuration for free API usage
- Contains logic for processing user requests and calling tools
- Needs to be modified to connect to MCP server instead of local functions

### Server Implementation (server.py)
- Implements ChatKit handshake for frontend communication
- Handles real-time messaging between frontend and backend
- Maintains conversation state and history
- Can be reused with minimal modifications

### Database Implementation (SQLModel + Neon DB)
- Uses SQLModel for ORM operations
- Implements proper data models with validation
- Handles connection pooling and session management
- Follows best practices for async database operations

## Connecting OpenAI Agent to MCP Server

### Key Considerations
- The agent needs to establish a connection to the MCP server
- Tool discovery happens automatically through the MCP protocol
- The agent will call MCP tools instead of local functions
- Error handling needs to account for network calls to MCP server

### Implementation Approach
- Initialize MCP client in the agent
- Register MCP tools during agent setup
- Handle tool calls as external API requests
- Implement proper timeout and retry mechanisms

## Todo Operations for MCP Server

### Required Operations
1. **Add Todo**: Create a new todo item with text content
2. **List Todos**: Retrieve all todo items for the current user
3. **Complete Todo**: Mark a todo item as completed
4. **Delete Todo**: Remove a todo item
5. **Update Todo**: Modify the content of an existing todo

### Implementation Details
- Each operation should be a separate MCP tool
- Operations should follow RESTful principles where applicable
- Proper error handling for cases like "todo not found"
- Validation of input parameters before database operations

## Technical Decisions

### Architecture Decision: MCP Server as Separate Service
- **Decision**: Implement MCP server as a separate service from the main backend
- **Rationale**: Allows for independent scaling and maintenance of tool operations
- **Alternative Considered**: Embedding MCP server in main backend
- **Why Rejected**: Would create tight coupling and potential performance issues

### Architecture Decision: Database Connection for MCP Server
- **Decision**: MCP server will connect directly to Neon DB
- **Rationale**: Avoids additional network hops and maintains data consistency
- **Alternative Considered**: MCP server calling backend API for database operations
- **Why Rejected**: Would add unnecessary complexity and latency

## Next Steps

1. Implement the MCP server with todo operations
2. Modify the agent to connect to the MCP server
3. Integrate with the existing ChatKit server
4. Set up the database models and services
5. Test the complete integration