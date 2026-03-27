import os
import sqlite3
from sqlalchemy import Engine,  event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL","sqlite:////app/test.db" ) 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # רק ל-SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # type: ignore
Base = declarative_base() # type: ignore
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
