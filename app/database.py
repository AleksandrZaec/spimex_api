from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings
from sqlalchemy.orm import declarative_base

Base = declarative_base()


engine = create_async_engine(settings.DB_URL, pool_pre_ping=True, echo=True)
Session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
