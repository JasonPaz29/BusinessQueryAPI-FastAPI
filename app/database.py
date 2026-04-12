from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

#Change this later to the actual database
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


