import asyncio
from datetime import datetime, timedelta


def seconds_until_next_1411() -> int:
    now = datetime.now()
    target = now.replace(hour=14, minute=11, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


async def reset_cache_periodically(app):
    redis_client = app.state.redis
    while True:
        wait_seconds = seconds_until_next_1411()
        print(f"Waiting {wait_seconds} seconds until next cache reset at 14:11")
        await asyncio.sleep(wait_seconds)
        print("Resetting Redis cache at 14:11")
        await redis_client.flushdb()
        print("Cache reset complete")
