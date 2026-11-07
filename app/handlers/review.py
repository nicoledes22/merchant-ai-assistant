from app.models.schemas import IncomingMessage, ProcessResult
from app.config import AppConfig
from app.ai.engine import AIEngine

def handle_review(msg: IncomingMessage, cfg: AppConfig) -> ProcessResult:
    engine = AIEngine(cfg)
    order = msg.order_info or {}
    item = order.get("item_title", "未知商品")
    amount = order.get("order_amount", 0)
    stars = msg.rating or 5
    is_negative = stars <= cfg.safety.negative_rating_threshold
    if is_negative:
        reply = engine.reply_negative_review(msg.content, stars, item, amount)
        action = "auto_sent" if not reply.need_human_review else "queued_for_review"
        note = "差评已处理" if action == "auto_sent" else "差评草稿待人工审核"
    else:
        reply = engine.reply_positive_review(msg.content, stars, item)
        action = "auto_sent" if not reply.need_human_review else "queued_for_review"
        note = "好评感谢已发送" if action == "auto_sent" else "好评草稿待审核"
    return ProcessResult(reply=reply, action=action, message=note)
