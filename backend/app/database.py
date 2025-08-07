# Handles database connection and session management

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL database URL
DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/job-tracker"

#The Engine is a   FACTORY that can create new database connections for us, which also holds onto connections inside of a Connection Pool for fast reuse. 
engine= create_engine(DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_status():
    try:
        with engine.connect() as connection:
            return {connection.dialect.name: "connected"}
    except Exception as e:
        return {connection.dialect.name: "disconnected", "error": str(e)}