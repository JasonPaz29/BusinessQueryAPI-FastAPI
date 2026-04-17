from fastapi import Depends, ApiRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Business, Review
from app.schemas.business_schemas import BusinessCreate, BusinessResponse, BusinessUpdate
from app.core.deps import get_current_user
from typing import List
import uuid

router = ApiRouter(prefix="/api", tags=["api"])

@router.get("/businesses")
def businesses(search: str | None = None, category: str | None = None, city: str | None = None, db: Session = Depends(get_db), skip: int = 0, limit: int = 10) -> List[BusinessResponse]:
    business_query = db.query(Business)
    if search:
        business_query = business_query.filter(Business.name.ilike(f"%{search}%"))
    if category:
        business_query = business_query.filter(Business.category.ilike(f"%{category}%"))
    if city:
        business_query = business_query.filter(Business.city.ilike(f"%{city}%"))
    business_query = business_query.offset(skip).limit(limit)
    return business_query.all()

@router.get("/businesses/{id}")
def get_business_by_id(id: uuid.UUID, db: Session = Depends(get_db)) -> BusinessResponse:
    business = db.query(Business).filter(Business.id == id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not Found."
        )
    return business

#TODO: Create endpoints for creating, updating, and deleting businesses

@router.post("/businesses")
def create_business(business: BusinessCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> BusinessResponse:
    new_business = Business(name=business.name, category=business.category, description=business.description, address=business.address, city=business.city, owner_id=current_user.id)

    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    
    return new_business

@router.put("/businesses/{id}")
def update_business(id: uuid.UUID, update: BusinessUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> BusinessResponse:
    business = db.query(Business).filter(Business.id == id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not Found."
        )
    
    if business.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to do this action."
        )
    
    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(business, key, value)
    
    db.commit()
    db.refresh(business)
    
    return business
    
    
@router.delete("/businesses/{id}")
def delete_business(id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    business = db.query(Business).filter(Business.id == id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not Found."
        )
        
    if business.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to do this action."
        )
    
    db.delete(business)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
      
      
        