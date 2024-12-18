from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL
# Updated DATABASE_URL to use asyncpg
DATABASE_URL = "postgresql+asyncpg://postgres:heheboii420@localhost:5432/chatbot_history"


# Async engine and session setup
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session
