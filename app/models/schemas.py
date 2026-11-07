from pydantic import BaseModel
from typing import Optional, Literal

class IncomingMessage(BaseModel):
    platform: str = "generic"
    type: Literal["consultation", "review"] = "consultation"
    user_id: str
    user_name: str = "顾客"
    content: str
    rating: Optional[int] = None
    order_info: Optional[dict] = None

class AIReply(BaseModel):
    reply_text: str
    category: str
    risk_level: Literal["low", "medium", "high"] = "low"
    need_human_review: bool = False
    reason: str = ""

class ProcessResult(BaseModel):
    reply: AIReply
    action: str
    message: str = ""
