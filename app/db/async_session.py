from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Async engine
print("database url::", settings.async_db_url)
async_engine = create_async_engine(settings.async_db_url, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
