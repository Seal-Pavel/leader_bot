import os
import httpx

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils.api_clients.leader_api_client import UserNotFoundException, CaptchaNotSetException
from utils.api_clients.telegram_api_client import TelegramAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)

TEAM_TELEGRAM_CHAT_ID = os.getenv('TEAM_TELEGRAM_CHAT_ID')


async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        f"HTTPException: status code {exc.status_code}, detail: {exc.detail}, path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def httpx_http_status_error_handler(request: Request, exc: httpx.HTTPStatusError):
    logger.error(
        f"httpx.HTTPStatusError: status code {exc.response.status_code}, detail: {exc.response.text}, path: {request.url.path}")

    if exc.response.status_code == 401:
        telegram_api_client: TelegramAPIClient = request.app.state.telegram_api_client
        await telegram_api_client.send_message(text=exc.response.text, chat_id=TEAM_TELEGRAM_CHAT_ID)

    return JSONResponse(
        status_code=exc.response.status_code,
        content={"message": exc.response.text}
    )


async def httpx_request_error_handler(request: Request, exc: httpx.RequestError):
    logger.error(
        f"httpx.RequestError: Internal server error occurred while making a request: {exc}, path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error occurred while making a request."}
    )


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


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    logger.info(
        f"UserNotFoundException: {str(exc)}, path: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )


async def captcha_not_set_exception_handler(request: Request, exc: CaptchaNotSetException):
    logger.error(
        f"CaptchaNotSetException: Captcha error, detail: {exc.message}, path: {request.url.path}")
    return JSONResponse(
        status_code=422,
        content={"message": "Captcha is required", "server_response": exc.message}
    )
