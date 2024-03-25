from fastapi import Request


def usedesk_service_dependency(request: Request):
    return request.app.state.usedesk_service


def telegram_service_dependency(request: Request):
    return request.app.state.telegram_service


async def user_service_dependency(request: Request):
    user_service = request.app.state.leader_services.user_service
    body = await request.json()
    user_email = body['data']['client_email']
    await user_service.load_user(user_email)
    return user_service


def event_service_dependency(request: Request):
    return request.app.state.leader_services.event_service
