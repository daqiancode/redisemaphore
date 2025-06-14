import pytest
import time
from redis import Redis
from redisemaphore import RedisSemaphore

@pytest.fixture(scope="module")
def redis_client():
    client = Redis(host="localhost", port=6379, decode_responses=True)
    yield client

def test_semaphore_acquire_and_release(redis_client):
    semaphore = RedisSemaphore(redis_client, "test_semaphore", max_concurrency=2, lease_time=5, wait_timeout=5)

    with semaphore.acquire():
        current = int(redis_client.get(semaphore._counter_key) or 0)
        assert current == 1

    current_after = int(redis_client.get(semaphore._counter_key) or 0)
    assert current_after == 0
