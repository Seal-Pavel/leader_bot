from fastapi import APIRouter, HTTPException, Request, Body

from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/update-leader-token")
async def update_token(request: Request, token: str = Body(..., embed=True)):
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing")

    await request.app.state.leader_services.update_token(token)

    logger.info("Token updated successfully.")
    return {"message": "Token updated successfully"}
