from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.config import load_config
from app.handlers.router import router as message_router
from app.web.dashboard import router as dashboard_router

app = FastAPI(title="Merchant AI Assistant", version="1.0.0")
app.state.config = load_config()
app.include_router(message_router, prefix="/webhook")
app.include_router(dashboard_router, prefix="/dashboard")

@app.get("/")
def root():
    return RedirectResponse(url="/dashboard/")

@app.get("/health")
def health():
    return {"status": "ok", "shop": app.state.config.shop.name}
