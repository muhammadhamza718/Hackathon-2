"""
Security utilities for authentication and authorization
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlmodel import Session, select
from backend.src.models.user import User
from backend.db.session import get_session

# Security schemes
security = HTTPBearer()

# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key-change-in-production"  # Should be loaded from environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the given data and expiration time
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify the JWT token and return the user
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Get the current user from the token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(credentials.credentials, credentials_exception)

    user = session.exec(select(User).where(User.email == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Get the current active user (verifies user is active)
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user