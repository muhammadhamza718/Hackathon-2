from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.tasks import router as tasks_router
from api.admin import router as admin_router
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlmodel import SQLModel
from db.session import async_engine
# Import models to ensure they are registered in metadata
from models.user import User
from models.task import Task
from models.session import Session

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run table creation on startup
    print("Executing startup table creation...")
    await create_tables()
    
    # FORCE ADMIN PROMOTION
    try:
        import os
        from db.session import async_engine
        admin_id = os.getenv("ADMIN_USER_ID")
        if admin_id:
            print(f"FORCE ADMIN: checking role for {admin_id}...")
            async with async_engine.begin() as conn:
                await conn.execute(text(f"UPDATE \"user\" SET role = 'admin' WHERE id = '{admin_id}'"))
                print("FORCE ADMIN: Role updated to 'admin'")
        else:
            print("FORCE ADMIN: No ADMIN_USER_ID found in environment")
    except Exception as e:
        print(f"FORCE ADMIN ERROR: {e}")
        
    yield

app = FastAPI(title="Todo App Backend", version="1.0.0", lifespan=lifespan)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Todo App Backend API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "now"}