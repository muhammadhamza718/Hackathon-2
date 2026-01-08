"""Todo ChatKit Backend - Main FastAPI Application"""

from dotenv import load_dotenv

# Load environment variables FIRST, before any other imports that might need them
load_dotenv()

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Any
from chatkit.server import StreamingResult
import os

# Import the ChatKit server
from server import TodoChatServer

# Import database initialization
from src.models.database import create_db_and_tables

# Import existing REST routers
from api.tasks import router as tasks_router
from api.admin import router as admin_router

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Todo Hybrid API (REST + ChatKit)")

@app.on_event("startup")
async def on_startup():
    logger.info("🔧 Running database initialization on startup...")
    try:
        # Create tables synchronously to avoid async event loop conflicts during startup
        create_db_and_tables()
        from sqlalchemy import inspect
        from src.models.database import sync_engine
        inspector = inspect(sync_engine)
        tables = inspector.get_table_names()
        logger.info(f"✅ Database tables verified/created: {tables}")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Outgoing Status: {response.status_code}")
    return response

# Include REST Routers
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

from api.deps import get_current_user

# Initialize the ChatKit server
chatkit_server = TodoChatServer()

@app.get("/")
async def root():
    return {
        "message": "Todo Hybrid API is Online",
        "status": "running",
        "chatkit_endpoint": "/chatkit",
        "rest_api_prefix": "/api"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    return {
        "status": "healthy",
        "service": "todo-backend",
        "version": "1.0.0"
    }

@app.post("/chatkit")
@app.post("//chatkit")
@app.post("/api/chatkit")
@app.post("//api/chatkit")
async def chatkit_endpoint(
    request: Request,
    current_user: Any = Depends(get_current_user)
) -> Response:
    """Unified endpoint for ChatKit Handshake, Session, and Messages (Authenticated)"""
    auth_header = request.headers.get("Authorization")
    logger.info(f"ChatKit request from User: {current_user.id} (Auth header present: {bool(auth_header)})")
    
    try:
        payload = await request.body()
        
        # Pass both request and user_id in the context
        # SqlModelStore will use this for user isolation
        result = await chatkit_server.process(payload, {
            "request": request,
            "user_id": current_user.id
        })

        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        
        if hasattr(result, "json"):
            return Response(content=result.json, media_type="application/json")
            
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"ChatKit Endpoint Error: {str(e)}", exc_info=True)
        return JSONResponse({"error": "Failed to process ChatKit request"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Todo Hybrid Backend on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)