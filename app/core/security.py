from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import get_settings
from datetime import datetime, timedelta

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    
    return hashed_password

def verify_password(plain: str, hashed: str) -> bool:
    is_correct = pwd_context.verify(plain, hashed)
    
    return is_correct

def create_access_token(sub_dict: dict) -> str:
    data = sub_dict.copy()
    data["exp"] =  datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token = jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)
    
    return token

def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        
        data = payload["sub"]
        
        return data
    
    except JWTError:
        return None
    
