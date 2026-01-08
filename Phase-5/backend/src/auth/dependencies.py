"""
Authentication dependencies for FastAPI endpoints
"""
from fastapi import Depends
from backend.src.models.user import User
from .security import get_current_active_user

# Dependency that requires an authenticated, active user
get_current_active_user_dep = Depends(get_current_active_user)

# Type alias for current active user
CurrentUser = Depends(get_current_active_user)


def get_current_active_user_dependency():
    """
    Returns a dependency that requires an authenticated, active user
    """
    return Depends(get_current_active_user)


# Commonly used dependency
def get_current_user() -> User:
    """
    Returns the current authenticated user
    """
    return Depends(get_current_active_user)