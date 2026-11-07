from fastapi import APIRouter, Request
from app.models.schemas import IncomingMessage, ProcessResult
from app.handlers.consultation import handle_consultation
from app.handlers.review import handle_review

router = APIRouter()

@router.post("/message", response_model=ProcessResult)
async def receive_message(req: Request, msg: IncomingMessage):
    cfg = req.app.state.config
    if msg.type == "review":
        return handle_review(msg, cfg)
    return handle_consultation(msg, cfg)
