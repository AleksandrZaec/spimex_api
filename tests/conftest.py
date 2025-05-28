import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
from datetime import date, timedelta
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from app.main import app
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)  # all
def ensure_test_env():
    mode = settings.MODE
    assert mode == "TEST", f"Тесты запускаются только при MODE=TEST, а сейчас MODE={mode!r}"


@pytest_asyncio.fixture  # all
async def test_session():
    engine = create_async_engine(settings.DB_URL, echo=False)
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture(scope="class")  # crud
async def date_range():
    end = date.today()
    start = end - timedelta(days=30)
    return start, end


@pytest.fixture(scope="class")  # crud
async def filters():
    return {
        "oil_id": "BRN",
        "delivery_type_id": "1",
        "delivery_basis_id": "2",
    }


@pytest.fixture  # api
async def ac():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture()  # all
async def test_cache():
    test_redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    app.state.redis = test_redis_client
    FastAPICache.init(RedisBackend(test_redis_client), prefix="fastapi-cache")
    yield test_redis_client
    await test_redis_client.flushdb()
    await test_redis_client.aclose()


@pytest.fixture
async def example_result_item():
    return {
        "id": 1,
        "exchange_product_id": "prod_001",
        "exchange_product_name": "Product Name",
        "oil_id": "oil_123",
        "delivery_basis_id": "basis_xyz",
        "delivery_basis_name": "Basis Name",
        "delivery_type_id": "type_abc",
        "volume": 100,
        "total": 2000.0,
        "count": 10,
        "date": "2024-01-01",
        "created_on": "2024-01-01T00:00:00Z",
        "updated_on": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def example_item():
    return {
        "date": "2024-01-01",
        "limit": 5,
    }
