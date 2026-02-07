from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from jose import JWTError
from core.security import verify_token
from models.user import User
from db.session import get_async_session
from sqlmodel import select


security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Get the current user from the JWT token OR database session.
    1. Try decoding as JWT.
    2. If invalid format, try looking up as opaque token in 'session' table.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    if credentials:
        token = credentials.credentials
    
    # Fallback: Try query parameter 'token' if header is missing
    # This is required for ChatKit Web Component which has issues sending headers with custom URL
    if not token and request.query_params.get("token"):
        token = request.query_params.get("token")

    if not token:
         raise credentials_exception

    user_id: Optional[str] = None
    user_role: str = "user"  # Default role if not found in token

    # 1. Try JWT Verification
    # Only attempt if it looks like a JWT (3 parts separated by dots)
    if len(token.split('.')) == 3:
        try:
            payload = verify_token(token)
            if payload:
                user_id = payload.get("sub")
                user_role = payload.get("role", "user")
                print(f"DEBUG: JWT Valid. UserID: {user_id}")
        except JWTError:
            pass  # Fallthrough to Session check

    # 2. If no JWT, Try Opaque Session Verification
    if not user_id:
        print(f"DEBUG: Checking DB for Opaque Token: {token[:15]}...")
        from models.session import Session as DbSession
        from datetime import datetime
        
        # Query session table
        query = select(DbSession).where(DbSession.token == token)
        result = await session.execute(query)
        db_session = result.scalar_one_or_none()
        
        if db_session:
            # Check expiration
            # Ensure proper timezone handling
            from datetime import timezone
            expires_at = db_session.expiresAt
            if expires_at.tzinfo is None:
                # If naive, assume UTC
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            
            # Use now(timezone.utc) for correct aware datetime
            now_utc = datetime.now(timezone.utc)

            if expires_at > now_utc:
                user_id = db_session.userId
                print(f"DEBUG: Opaque Session Valid. UserID: {user_id}")
            else:
                print("DEBUG: Opaque Session Expired")
        else:
            print("DEBUG: Opaque Session Not Found")

    if not user_id:
        raise credentials_exception

    # 3. Get user from database
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.first()

    if user is None:
        raise credentials_exception

    user = user[0]  # Extract user from tuple

    # --- AUTO-PROMOTION Logic ---
    # Automatically grant 'admin' role if the email matches ADMIN_EMAIL from env
    import os
    admin_email_env = os.getenv("ADMIN_EMAIL")
    if admin_email_env and user.email == admin_email_env and user.role != "admin":
        print(f"AUTO-PROMOTION: Setting Admin role for {user.email}")
        user.role = "admin"
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user



async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current admin user.
    Verifies that the current user has admin role.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed, admin access required"
        )
    return current_user