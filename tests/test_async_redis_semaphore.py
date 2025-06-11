import asyncio
import pytest
import time
from redis.asyncio import Redis
from redisemaphore import AsyncRedisSemaphore
import pytest_asyncio

@pytest_asyncio.fixture(scope="module")
async def redis_client():
    client = Redis(host="localhost", port=6379, decode_responses=True)
    yield client
    await client.aclose()

@pytest.mark.asyncio
async def test_acquire_and_release(redis_client):
    semaphore = AsyncRedisSemaphore(redis_client, "test_async", max_concurrency=2, lease_time=5, wait_timeout=5)

    async with semaphore.acquire():
        current = int(await redis_client.get(semaphore._counter_key) or 0)
        assert current == 1

    current_after = int(await redis_client.get(semaphore._counter_key) or 0)
    assert current_after == 0

