from fastapi import Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Business, Review
from app.schemas.review_schemas import ReviewCreate, ReviewResponse, ReviewUpdate
from app.core.deps import get_current_user
from typing import List
import uuid

router = APIRouter(prefix="/reviews", tags=["review"])

@router.get("/{business_id}")
def reviews(business_id: uuid.UUID, db: Session = Depends(get_db)) -> List[ReviewResponse]:
    reviews = db.query(Review).filter(Review.business_id == business_id).all()
        
    return reviews

@router.post("/{business_id}")
def create_review(review: ReviewCreate, business_id: uuid.UUID, current_user: Session = Depends(get_current_user), db: Session = Depends(get_db)) -> ReviewResponse:
    new_review = Review(user_id=current_user.id, business_id=business_id, rating=review.rating, body=review.body)
        
    
    db.add(new_review)
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Business not found."
    )
    business.avg_rating = business.average_rating()
    
    db.commit()
    db.refresh(new_review)
    db.refresh(business)
    
    return new_review

@router.put("/{business_id}/{review_id}")
def update_review(business_id: uuid.UUID, review_id: uuid.UUID, update: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ReviewResponse:
    review = db.query(Review).filter(Review.business_id == business_id, Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this review!",
        )
    
    update_data = update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(review, key, value)

    business = db.query(Business).filter(Business.id == business_id).first()
    business.avg_rating = business.average_rating()
    
    
    db.commit()
    db.refresh(review)
    db.refresh(business)
    
    return review

@router.delete("/{business_id}/{review_id}")
def delete_review(business_id: uuid.UUID, review_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Response:
    review = db.query(Review).filter(Review.business_id == business_id, Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not Found."
        )
    
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this review!",
        )
    
    db.delete(review)
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Business not found."
    )
    business.avg_rating = business.average_rating()
    
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
