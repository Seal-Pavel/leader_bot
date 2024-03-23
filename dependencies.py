from fastapi import Request


def usedesk_service_dependency(request: Request):
    return request.app.state.usedesk_service


def user_service_dependency(request: Request):
    return request.app.state.leader_services.user_service


def event_service_dependency(request: Request):
    return request.app.state.leader_services.event_service
