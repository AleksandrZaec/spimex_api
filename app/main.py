from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
import asyncio
from app.config import redis_url
from app.routes import trading
from app.cache import reset_cache_periodically

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    app.state.redis = redis_client
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

    task = asyncio.create_task(reset_cache_periodically(app))


@app.on_event("shutdown")
async def on_shutdown():
    await app.state.redis.close()


app.include_router(trading.router, prefix="/trading", tags=["trading"])
