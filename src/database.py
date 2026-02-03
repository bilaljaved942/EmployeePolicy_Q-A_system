"""Database configuration and connection setup"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from .config import DATABASE_URL

# Create engine with connection pooling disabled for better Render compatibility
engine = create_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,  # Disable connection pooling for Render
    connect_args={"connect_timeout": 10}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
