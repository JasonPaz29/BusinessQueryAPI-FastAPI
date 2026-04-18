from pydantic import BaseModel, ConfigDict
import uuid
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int
    body: Optional[str] = None
    
class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    business_id: uuid.UUID
    rating: int
    body: Optional[str] = None
    created_at: datetime
    
class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    body: Optional[str] = None
    