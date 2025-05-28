from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
import asyncio
from app.config import settings
from app.routes import trading
from app.cache import reset_cache_periodically

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    app.state.redis = redis_client

    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

    task = asyncio.create_task(reset_cache_periodically(app))

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    await redis_client.aclose()


app.include_router(trading.router, prefix="/trading", tags=["trading"])
