import os

import httpx

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError

import exception_handlers as eh

from routers.leader.user_router import router as leader_user_router
from routers.leader.token_router import router as leader_token_router
from routers.usedesk.ticket_router import router as usedesk_ticket_router

from utils.leader_api_client import LeaderAPIClient, UserNotFoundException, CaptchaNotSetException
from utils.usedesk_api_client import UsedeskAPIClient
from utils.logger import get_logger

from services.leader_service import LeaderServices
from services.usedesk_service import UsedeskService

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.bot import router

from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

app = FastAPI()

app.add_exception_handler(HTTPException, eh.fastapi_http_exception_handler)
app.add_exception_handler(httpx.HTTPStatusError, eh.httpx_http_status_error_handler)
app.add_exception_handler(httpx.RequestError, eh.httpx_request_error_handler)
app.add_exception_handler(RequestValidationError, eh.generic_exception_handler)
app.add_exception_handler(Exception, eh.generic_exception_handler)
app.add_exception_handler(UserNotFoundException, eh.user_not_found_exception_handler)
app.add_exception_handler(CaptchaNotSetException, eh.captcha_not_set_exception_handler)

app.include_router(leader_user_router, prefix="/api/v1/leader", tags=["Leader-ID"])
app.include_router(leader_token_router, prefix="/api/v1/leader", tags=["Leader-ID"])
app.include_router(usedesk_ticket_router, prefix="/api/v1/usedesk", tags=["Usedesk"])

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
storage = RedisStorage.from_url(os.getenv('REDIS_URL'))
dp = Dispatcher(storage=storage)
dp.include_router(router)


@app.on_event("startup")
async def startup():
    """
    Webhook registration and API clients initialization.
    """
    webhook_url = f"{os.getenv('BOT_WEBHOOK_URL')}{os.getenv('BOT_WEBHOOK_PATH')}"
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook URL: {webhook_url}")

    # API clients
    app.state.leader_api_client = LeaderAPIClient()
    app.state.usedesk_api_client = UsedeskAPIClient()

    # Services
    app.state.leader_services = LeaderServices(app.state.leader_api_client)
    app.state.usedesk_service = UsedeskService(app.state.usedesk_api_client)

    # Authenticate
    await app.state.leader_services.authenticate()
    await app.state.usedesk_service.authenticate()


@app.on_event("shutdown")
async def shutdown():
    await app.state.leader_api_client.close()
    await app.state.usedesk_api_client.close()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post(os.getenv('BOT_WEBHOOK_PATH'))
async def receive_update(request: Request):
    """
    Processing incoming updates from a webhook.
    """
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}
