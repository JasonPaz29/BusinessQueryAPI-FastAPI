from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
class UserLogin(BaseModel):
    email: str
    password: str

    