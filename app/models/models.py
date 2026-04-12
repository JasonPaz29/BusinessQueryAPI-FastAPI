from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy import Uuid, String, Boolean, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, onupdate=datetime.utcnow)
    
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")
    businesses: Mapped[List["Business"]] = relationship(back_populates="user")
    
class Business(Base):
    __tablename__ = "businesses"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50))
    avg_rating: Mapped[Optional[float]] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(300))
    address: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    owner: Mapped[User] = relationship(back_populates="businesses")
    reviews: Mapped[List["Review"]] = relationship(back_populates="business")
    
    
    def average_rating(self):
        if not self.reviews:
            return None
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1)
    
class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    business_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("businesses.id"))
    rating: Mapped[int] = mapped_column(Integer)
    body: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None, onupdate=datetime.utcnow)
    
    user: Mapped[User] = relationship(back_populates="reviews")
    business: Mapped[Business] = relationship(back_populates="reviews")
    
    