from fastapi import Request, Depends

from models.ticket import TicketRequest

from utils.logger import get_logger

logger = get_logger(__name__)


def usedesk_service_dependency(request: Request):
    logger.debug(f"logger in usedesk_service_dependency")
    return request.app.state.usedesk_service


# -------------------


def telegram_service_dependency(request: Request):
    logger.debug(f"logger in telegram_service_dependency")
    return request.app.state.telegram_service


# -------------------


# TODO: Сделать типа load_ticket (usedesk_service.py)
async def ticket_request_dependency(ticket_request: TicketRequest):
    logger.debug(f"logger in ticket_request_dependency")
    return ticket_request


# TODO: Нельзя использовать зависимость в во всех ручках. Для нее сейчас требуются конкретно данные из тикета Usedesk.
async def user_service_dependency(request: Request, ticket_request: TicketRequest = Depends(ticket_request_dependency)):
    logger.debug(f"logger in user_service_dependency")
    logger.debug(f"{ticket_request=}")
    user_service = request.app.state.leader_services.user_service
    await user_service.load_user(ticket_request.client_email)
    return user_service


# -------------------

def event_service_dependency(request: Request):
    logger.debug(f"logger in event_service_dependency")
    return request.app.state.leader_services.event_service
