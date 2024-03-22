import os

import httpx

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routers.endpoints import router as ticket_router

from utils.leader_api_client import LeaderAPIClient, UserNotFoundException
from utils.usedesk_api_client import UsedeskAPIClient
from utils.logger import get_logger

from services.leader_service import LeaderServices
from services.usedesk_service import NotificationService

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.bot import router

from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

app = FastAPI()
app.include_router(ticket_router)

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
storage = RedisStorage.from_url(os.getenv('REDIS_URL'))
dp = Dispatcher(storage=storage)
dp.include_router(router)


@app.exception_handler(HTTPException)
async def fastapi_http_exception_handler(request, exc):
    logger.error(
        f"HTTPException: status code {exc.status_code}, detail: {exc.detail}, path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.exception_handler(httpx.HTTPStatusError)
async def httpx_http_status_error_handler(request, exc):
    logger.error(
        f"httpx.HTTPStatusError: status code {exc.response.status_code}, detail: {exc.response.text}, path: {request.url.path}")
    return JSONResponse(
        status_code=exc.response.status_code,
        content={"message": exc.response.text}
    )


@app.exception_handler(httpx.RequestError)
async def httpx_request_error_handler(request, exc):
    logger.error(
        f"httpx.RequestError: Internal server error occurred while making a request.")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error occurred while making a request."}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        logger.debug(
            f"Validation exception: {exc}, path: {request.url.path}")
    else:
        logger.error(
            f"Unhandled exception: {exc}, path: {request.url.path}")

    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    logger.info(
        f"UserNotFoundException: {str(exc)}, path: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )


@app.on_event("startup")
async def startup():
    """
    Webhook registration and API clients initialization.
    """
    webhook_url = f"{os.getenv('BOT_WEBHOOK_URL')}{os.getenv('BOT_WEBHOOK_PATH')}"
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook URL: {webhook_url}")

    app.state.leader_api_client = LeaderAPIClient()
    app.state.usedesk_api_client = UsedeskAPIClient()

    app.state.leader_services = LeaderServices(app.state.leader_api_client)
    app.state.usedesk_service = NotificationService(app.state.usedesk_api_client)

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
