from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-for-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the given data and expiration time.
    This function is provided for completeness but Better Auth typically handles token creation.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify the JWT token and return the payload if valid.
    """
    try:
        # DEBUG LOGGING
        print(f"DEBUG: Verifying token: {token[:20]}...")
        print(f"DEBUG: Using Secret: {SECRET_KEY[:5]}...")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Token Valid! Payload: {payload}")
        return payload
    except JWTError as e:
        print(f"DEBUG: Token Validation Failed: {str(e)}")
        return None


def decode_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode the token payload without verification (useful for debugging).
    In production, always use verify_token for security.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        return payload
    except JWTError:
        return None