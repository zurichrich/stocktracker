from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use SQLite for local development
DATABASE_URL = 'sqlite:///./stockdata.db'

# Create engine with SQLite
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get database session with proper error handling"""
    db = SessionLocal()
    try:
        # Test connection with properly declared text
        db.execute(text("SELECT 1"))
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        db.close()