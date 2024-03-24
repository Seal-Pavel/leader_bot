import httpx
import asyncio
from utils.token_bucket import TokenBucket
from dotenv import load_dotenv

load_dotenv()


class BaseAPIClient:
    def __init__(
            self,
            base_url="",
            retry_attempts=3,
            retry_delay=1.0,
            bucket_rate=5,
            bucket_capacity=5
    ):
        self.base_url = base_url
        self.retry_attempts = retry_attempts  # Кол-во повторных вызовов.
        self.retry_delay = retry_delay  # Задержка в секундах между повторными вызовами.
        self.bucket_rate = bucket_rate  # Скорость добавления токенов в ведро в токенах в секунду.
        self.bucket_capacity = bucket_capacity  # Максимальное количество токенов в ведре.
        self.client = httpx.AsyncClient(base_url=base_url)
        self.bucket = TokenBucket(rate=self.bucket_rate, capacity=self.bucket_capacity)

    async def make_request(self,
                           method: str,
                           endpoint: str,
                           should_retry: bool = True,
                           attempts: int = None,
                           delay: int = None,
                           **kwargs) -> httpx.Response:
        # Use default values
        if attempts is None:
            attempts = self.retry_attempts
        if delay is None:
            delay = self.retry_delay

        while attempts > 0:
            attempts -= 1
            try:
                await self.bucket.wait_for_token()  # Waiting for the token to be available before each request
                response = await self.client.request(method, endpoint, **kwargs)
                response.raise_for_status()
                return response

            except (httpx.HTTPStatusError, httpx.RequestError) as httpx_error:
                if not should_retry or attempts <= 0:
                    raise httpx_error
            except Exception as e:
                if attempts <= 0:
                    raise e

            await asyncio.sleep(delay)

    async def close(self):
        await self.client.aclose()
