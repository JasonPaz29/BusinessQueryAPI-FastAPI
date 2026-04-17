from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    is_active: bool
    is_owner: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: str
    password: str

    