from app.models.schemas import IncomingMessage, ProcessResult
from app.config import AppConfig
from app.ai.engine import AIEngine

def handle_consultation(msg: IncomingMessage, cfg: AppConfig) -> ProcessResult:
    engine = AIEngine(cfg)
    order = msg.order_info or {}
    item = order.get("item_title", "未知商品")
    amount = order.get("order_amount", 0)
    reply = engine.reply_consultation(msg.content, item, amount)
    if reply.need_human_review:
        action, note = "queued_for_review", "已生成草稿，等待人工审核"
    elif cfg.safety.auto_send_consultation:
        action, note = "auto_sent", "已自动回复"
    else:
        action, note = "queued_for_review", "咨询自动发送已关闭"
    return ProcessResult(reply=reply, action=action, message=note)
