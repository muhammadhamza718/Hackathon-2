"""ChatKit handshake server for the Todo Chatbot"""

import os
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from ..middleware.security import security_middleware
from contextlib import asynccontextmanager
import asyncio
import logging
from dotenv import load_dotenv
from datetime import datetime

from ..agents.agent import TodoAgent
from ..config.logging_config import get_logger, log_api_call, log_error
from ..config.app_config import get_config
from ..monitoring.metrics import (
    metrics_collector,
    increment_api_requests,
    increment_api_errors,
    record_response_time,
    increment_active_connections,
    decrement_active_connections,
    get_api_metrics
)

# Load environment variables
load_dotenv()

# Setup centralized logging
logger = get_logger(__name__)

# Global agent instance
todo_agent: Optional[TodoAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the agent when the application starts"""
    global todo_agent
    logger.info("Initializing Todo Agent...")
    todo_agent = TodoAgent()

    # Connect to MCP server
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    await todo_agent.connect_to_mcp_server(mcp_server_url)

    logger.info("Todo Agent initialized and connected to MCP server")
    yield
    # Cleanup on shutdown
    logger.info("Shutting down Todo Agent...")


# Create FastAPI app
app = FastAPI(
    title="Todo Chatbot API",
    description="API for the AI-Powered Todo Chatbot with MCP Integration",
    version="1.0.0",
    lifespan=lifespan
)

# Import and include routers
print("DEBUG: Importing routers...")
from .routers import admin_router, tasks_router
print("DEBUG: Routers imported successfully")
print("DEBUG: Including admin_router...")
app.include_router(admin_router)
print("DEBUG: Including tasks_router...")
app.include_router(tasks_router)
print("DEBUG: All routers included successfully")

# Get configuration
config = get_config()

# Add CORS middleware
if config.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins_list or ["*"],  # Use configured origins or wildcard
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add security middleware
app.middleware("http")(security_middleware.__call__)


class ConnectionManager:
    """Manage WebSocket connections"""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        increment_active_connections()
        logger.info(f"New WebSocket connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket connection closed. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.copy():  # Use copy to avoid modification during iteration
            try:
                await connection.send_text(message)
            except:
                # Remove connection if sending fails
                try:
                    self.disconnect(connection)
                except:
                    pass  # Connection might already be removed


manager = ConnectionManager()


@app.get("/")
async def root():
    """Root endpoint to verify the server is running"""
    return {"message": "Todo Chatbot API is running", "status": "ok"}


@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    import time
    start_time = time.time()

    # Check database connectivity
    db_healthy = True
    try:
        from ..models.database import get_sync_session
        with get_sync_session() as session:
            # Execute a simple query to check DB connectivity
            session.execute("SELECT 1")
    except Exception:
        db_healthy = False

    # Check MCP server connectivity
    mcp_healthy = True
    try:
        import httpx
        mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{mcp_url}/health")
            mcp_healthy = response.status_code == 200
    except Exception:
        mcp_healthy = False

    # Calculate response time
    response_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds

    status = "healthy" if (db_healthy and mcp_healthy) else "unhealthy"

    return {
        "status": status,
        "service": "todo-chatbot-api",
        "timestamp": datetime.utcnow().isoformat(),
        "response_time_ms": response_time,
        "checks": {
            "database": "healthy" if db_healthy else "unhealthy",
            "mcp_server": "healthy" if mcp_healthy else "unhealthy"
        }
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint - checks if the service is ready to accept traffic"""
    import time
    start_time = time.time()

    # Check if the agent is initialized
    agent_ready = todo_agent is not None

    # Check database connectivity
    db_ready = True
    try:
        from ..models.database import get_sync_session
        with get_sync_session() as session:
            # Execute a simple query to check DB connectivity
            session.execute("SELECT 1")
    except Exception:
        db_ready = False

    # Calculate response time
    response_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds

    status = "ready" if (agent_ready and db_ready) else "not ready"

    return {
        "status": status,
        "service": "todo-chatbot-api",
        "timestamp": datetime.utcnow().isoformat(),
        "response_time_ms": response_time,
        "checks": {
            "agent_initialized": agent_ready,
            "database": db_ready
        }
    }


@app.get("/metrics")
async def get_metrics():
    """Metrics endpoint for monitoring"""
    return get_api_metrics()


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    start_time = datetime.now()
    await manager.connect(websocket)
    increment_api_requests()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")

            # Parse the message (expecting JSON with 'message' field)
            try:
                message_data = json.loads(data)
                raw_message = message_data.get("message", "")
                from ..utils.input_sanitizer import InputSanitizer
                user_message = InputSanitizer.sanitize_user_message(raw_message)
            except json.JSONDecodeError:
                raw_message = data  # If not JSON, treat the whole data as the message
                from ..utils.input_sanitizer import InputSanitizer
                user_message = InputSanitizer.sanitize_user_message(raw_message)

            # Validate that we have an agent
            if not todo_agent:
                error_msg = json.dumps({"error": "Agent not initialized"})
                await manager.send_personal_message(error_msg, websocket)
                continue

            # Process the message with the agent
            try:
                response_start_time = datetime.now()
                response = todo_agent.send_message(user_message)
                response_duration = (datetime.now() - response_start_time).total_seconds()
                duration = (datetime.now() - start_time).total_seconds()

                # Record response time for the agent processing
                record_response_time(response_duration, "/websocket/agent_process")

                logger.info(f"Agent response: {response} (processed in {response_duration:.3f}s, total: {duration:.3f}s)")

                # Send response back to client
                response_data = {
                    "type": "response",
                    "message": response,
                    "timestamp": asyncio.get_event_loop().time()
                }
                await manager.send_personal_message(json.dumps(response_data), websocket)
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                record_response_time(duration, "/websocket/error")
                increment_api_errors()
                log_error(e, {"message": user_message, "duration": duration})

                # Handle the error and provide user-friendly feedback
                from ..services.error_handlers import handle_generic_error
                error_response_obj = handle_generic_error(e)

                error_response = {
                    "type": "error",
                    "message": error_response_obj.user_friendly_message,
                    "original_error": str(e),  # Only include for debugging, consider removing in production
                    "timestamp": asyncio.get_event_loop().time()
                }
                await manager.send_personal_message(json.dumps(error_response), websocket)

    except WebSocketDisconnect:
        duration = (datetime.now() - start_time).total_seconds()
        record_response_time(duration, "/websocket/disconnect")
        logger.info(f"WebSocket disconnected after {duration:.3f}s")
        manager.disconnect(websocket)


@app.post("/chat")
async def chat_sync(request: Request):
    """Synchronous chat endpoint for non-WebSocket clients"""
    start_time = datetime.now()
    request_id = f"req_{int(start_time.timestamp())}_{hash(str(request.client)) % 10000}"

    increment_api_requests()

    try:
        data = await request.json()
        raw_message = data.get("message", "")
        from ..utils.input_sanitizer import InputSanitizer
        user_message = InputSanitizer.sanitize_user_message(raw_message)

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Validate that we have an agent
        if not todo_agent:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        # Process the message with the agent
        response = todo_agent.send_message(user_message)
        duration = (datetime.now() - start_time).total_seconds()

        # Record response time
        record_response_time(duration, "/chat")

        # Log the API call
        log_api_call("/chat", "POST", 200, duration, request_id=request_id)
        logger.info(f"Chat API call completed in {duration:.3f}s", extra={'request_id': request_id})

        return {
            "success": True,
            "response": response,
            "user_message": user_message,
            "request_id": request_id
        }
    except HTTPException:
        duration = (datetime.now() - start_time).total_seconds()
        record_response_time(duration, "/chat")
        log_api_call("/chat", "POST", 422, duration, request_id=request_id)  # Using 422 for validation errors
        raise
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        record_response_time(duration, "/chat")
        increment_api_errors()
        log_api_call("/chat", "POST", 500, duration, request_id=request_id)
        log_error(e, {"message": user_message, "duration": duration, "request_id": request_id})

        # Handle the error and provide user-friendly feedback
        from ..services.error_handlers import handle_generic_error
        error_response_obj = handle_generic_error(e)

        raise HTTPException(status_code=500, detail=error_response_obj.user_friendly_message)


@app.get("/todos")
async def get_todos():
    """Get all todos (for testing/debugging)"""
    if not todo_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    # This would call the agent to list todos
    response = todo_agent.send_message("List all my todos")
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    config = get_config()
    uvicorn.run(
        app,
        host=config.api_host,
        port=config.api_port,
        workers=config.api_workers
    )