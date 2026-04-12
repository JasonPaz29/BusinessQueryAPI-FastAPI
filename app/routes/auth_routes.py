from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_schemas import UserCreate, UserResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

    
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    existing = db.query(User).filter(or_(User.email.ilike(user.email), User.username == user.username)).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists.",
        )
    
    new_user = User(username=user.username, email=user.email, hashed_password=hash_password(user.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
@router.post("/login")
def login(uinfo: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email.ilike(uinfo.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No User found with that email.",
        )
    if not verify_password(uinfo.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password doesn't match."
        )
        
    return {"access_token": create_access_token({"sub": str(user.id)}), "token_type": "bearer"}
