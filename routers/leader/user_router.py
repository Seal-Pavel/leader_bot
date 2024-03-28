from fastapi import APIRouter, Depends

from models.ticket import TicketRequest

from utils.logger import get_logger

from services.leader_service import UserService
from services.usedesk_service import UsedeskService
from services.telegram_service import TelegramService

from dependencies import (usedesk_service_dependency,
                          user_service_dependency,
                          telegram_service_dependency,
                          ticket_request_dependency)

logger = get_logger(__name__)

router = APIRouter()


@router.post("/user/reactivate-and-notify")
async def reactivate_and_notify_user(ticket_request: TicketRequest = Depends(ticket_request_dependency),
                                     user_service: UserService = Depends(user_service_dependency),
                                     usedesk_service: UsedeskService = Depends(usedesk_service_dependency),
                                     telegram_service: TelegramService = Depends(telegram_service_dependency),
                                     ):
    user_id = user_service.user.id
    user_birthday = user_service.user.birthday
    notify_text = f'🔓 <a href="https://admin.leader-id.ru/users/{user_id}">{user_id}</a> ({user_birthday.year})'

    is_reactivate, reactivate_message = await user_service.reactivate()
    if is_reactivate:
        await usedesk_service.reply_to_reactivated_user(ticket_request, user_birthday)
        await telegram_service.user_reactivation_notification(notify_text)

    return {"message": reactivate_message}
