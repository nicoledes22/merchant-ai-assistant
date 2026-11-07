from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()
DASHBOARD_DIR = Path(__file__).parent / "static"

@router.get("/")
def index():
    return FileResponse(DASHBOARD_DIR / "index.html")

@router.get("/api/status")
def status(req: Request):
    cfg = req.app.state.config
    return {"shop": cfg.shop.name, "ai_model": cfg.ai.model,
            "auto_consult": cfg.safety.auto_send_consultation,
            "auto_pos_review": cfg.safety.auto_send_positive_review,
            "auto_neg_review": cfg.safety.auto_send_negative_review}
