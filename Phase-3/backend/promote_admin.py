import asyncio
from sqlmodel import select
from db.session import get_async_session, async_engine
from models.user import User

async def promote_user_to_admin(email: str):
    print(f"Attempting to promote user {email} to admin...")
    
    # Manually create session since we're in a script
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.asyncio import AsyncSession
    
    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with AsyncSessionLocal() as session:
        # Find user
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"Error: User with email {email} not found.")
            print("Please sign up first via the frontend.")
            return
            
        print(f"Found user: {user.name} (Current role: {user.role})")
        
        if user.role == "admin":
            print("User is already an admin.")
            return

        # Update role
        user.role = "admin"
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        print(f"Success! User {user.name} is now an ADMIN.")

if __name__ == "__main__":
    email = "mhamza77188@gmail.com"
    asyncio.run(promote_user_to_admin(email))
