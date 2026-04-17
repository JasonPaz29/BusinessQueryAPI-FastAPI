from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

class BusinessCreate(BaseModel):
    name: str
    category: str
    description: str
    address: str
    city: str
    
class BusinessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    category: str
    description: str
    avg_rating: Optional[float]
    address: str
    city: str
    created_at: datetime

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None