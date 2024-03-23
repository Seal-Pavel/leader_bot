import asyncio


class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        """
        :param rate: Скорость добавления токенов в ведро в токенах в секунду.
        :param capacity: Максимальное количество токенов в ведре.
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.updated_at = asyncio.get_event_loop().time()

    async def wait_for_token(self, amount: int = 1):
        while self.tokens < amount:
            await self._add_tokens()
            if self.tokens < amount:
                sleep_time = (amount - self.tokens) / self.rate
                await asyncio.sleep(sleep_time)
            else:
                break
        self.tokens -= amount

    async def _add_tokens(self):
        now = asyncio.get_event_loop().time()
        elapsed = now - self.updated_at
        self.updated_at = now
        self.tokens = min(self.tokens + elapsed * self.rate, self.capacity)
