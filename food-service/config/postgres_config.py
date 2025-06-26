from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:root@localhost:5432/cinema-food"

engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,  
    autoflush=False, 
    bind=engine,       
    class_=Session
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()