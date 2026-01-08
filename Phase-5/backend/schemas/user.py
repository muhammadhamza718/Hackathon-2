from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserRead(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    role: str
    created_at: datetime