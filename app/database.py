from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from app.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
Session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
