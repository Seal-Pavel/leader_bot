from fastapi import APIRouter, HTTPException, Request, Body
from models.ticket import TicketRequest
from utils.logger import get_logger

from services.leader_service import UserService
from services.usedesk_service import UsedeskService

logger = get_logger(__name__)

router = APIRouter()


@router.post("/user/reactivate-and-notify")
async def reactivate_and_notify_user(request: TicketRequest):
    user_service: UserService = request.app.state.leader_services.user_service
    usedesk_service: UsedeskService = request.app.state.usedesk_service

    await user_service.load_user(request.data.client_email)

    if not user_service.is_user_blocked() and user_service.user.id != 1127536:
        return {"message": "Ticket processed successfully"}

    await user_service.unlocking_and_approve()
    logger.info(f'User with ID {user_service.user.id} and date of birth {user_service.user.birthday} is unblocked')

    is_mistake_in_age = True if int(user_service.user.birthday.year) > 2012 else False
    if not is_mistake_in_age:
        text, files = notification_service.get_minor_notification()
    else:
        text, files = notification_service.get_incorrect_birth_year_notification()

    send_message(ticket=ticket_id, message=text, fls=files)

    return {"message": "Ticket processed successfully"}


@router.post("/update-token")
async def update_token(request: Request, token: str = Body(..., embed=True)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    await request.app.state.api_client.update_token(token)
    logger.info("Token updated successfully")
    return {"message": "Token updated successfully"}
