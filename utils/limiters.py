import time
import asyncio

from collections import deque
from datetime import timedelta


class AsyncTokenBucketLimiter:
    def __init__(self, add_speed: float, rate: float):
        """
        :param rate: Maximum number of tokens in a bucket.
        :param add_speed: Speed of adding tokens to the bucket in tokens per second.
        """
        self.rate = rate
        self.add_speed = add_speed
        self.tokens = rate
        self.updated_at = asyncio.get_event_loop().time()

    async def wait_for_token(self, amount: int = 1):
        while self.tokens < amount:
            await self._add_tokens()
            if self.tokens < amount:
                sleep_time = (amount - self.tokens) / self.add_speed
                await asyncio.sleep(sleep_time)
            else:
                break
        self.tokens -= amount

    async def _add_tokens(self):
        now = asyncio.get_event_loop().time()
        elapsed = now - self.updated_at
        self.updated_at = now
        self.tokens = min(self.tokens + elapsed * self.add_speed, self.rate)


class AsyncSlidingWindowLimiter:
    def __init__(self,
                 rate: int = 5,
                 period: timedelta = timedelta(seconds=1)):
        """
        :param rate: Maximum number of transactions per period. Default 5.
        :param period: Duration of the period in seconds. Default 1.
        """
        self.rate = rate
        self.period = period.total_seconds()
        self.timestamps = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.monotonic()

            # Clean up stale timestamps
            while self.timestamps and now - self.timestamps[0] > self.period:
                self.timestamps.popleft()

            # Wait if limit reached
            if len(self.timestamps) >= self.rate:
                sleep_time = (self.timestamps[0] + self.period) - now
                await asyncio.sleep(sleep_time)
                now = time.monotonic()  # After waiting, update the current time and continue the loop

            self.timestamps.append(now)  # Add a timestamp for the current operation
