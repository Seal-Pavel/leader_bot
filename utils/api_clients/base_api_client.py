import httpx
import asyncio

from utils.limiters import AsyncSlidingWindowLimiter

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class BaseAPIClient:

    def __init__(
            self,
            base_url="",
            retry_attempts=3,
            retry_delay=1.0,
            limiter_rate: int | None = None,
            limiter_period: timedelta | None = None):
        """
            :param base_url: API base url.

            :param retry_attempts: Number of repeated calls. Default 3.
            :param retry_delay: Delay between repeated calls in seconds. Default 1.

            :param limiter_rate: Maximum number of transactions per period.
            :param limiter_period: Duration of the period.
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.limiter = AsyncSlidingWindowLimiter(
            rate=limiter_rate if limiter_rate is not None else 5,
            period=limiter_period if limiter_period is not None else timedelta(seconds=1)
        )

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
                await self.limiter.acquire()  # Obtaining permission from the limiter
                response = await self.client.request(method, endpoint, **kwargs)
                response.raise_for_status()
                return response

            except (httpx.HTTPStatusError, httpx.RequestError) as httpx_error:
                if not should_retry or attempts <= 0:
                    raise httpx_error
            except Exception as e:
                if attempts <= 0:
                    raise e

            if attempts != 0:
                await asyncio.sleep(delay)

    async def close(self):
        await self.client.aclose()
