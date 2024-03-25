from fastapi import APIRouter, Depends

from models.ticket import TicketRequest

from utils.logger import get_logger

from services.leader_service import UserService
from services.usedesk_service import UsedeskService

from dependencies import usedesk_service_dependency, user_service_dependency

logger = get_logger(__name__)

router = APIRouter()


@router.post("/user/reactivate-and-notify")
async def reactivate_and_notify_user(request: TicketRequest,
                                     user_service: UserService = Depends(user_service_dependency),
                                     usedesk_service: UsedeskService = Depends(usedesk_service_dependency)
                                     ):
    is_reactivate, reactivate_message = await user_service.reactivate(request.data.client_email)
    if is_reactivate:
        await usedesk_service.reply_to_reactivated_user(request.data, user_service.user.birthday)
        # <- telegram
    return {"message": reactivate_message}
