from pathlib import Path
from pydantic import BaseModel
import yaml

class AIConfig(BaseModel):
    base_url: str
    api_key: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 400

class ShopConfig(BaseModel):
    name: str = "我的小店"
    owner: str = "店主"
    tone: str = "亲切友好"
    return_policy: str = "7天无理由退换"
    faq: list = []
    forbidden_words: list = []

class SafetyConfig(BaseModel):
    auto_send_positive_review: bool = True
    auto_send_negative_review: bool = False
    auto_send_consultation: bool = True
    manual_review_keywords: list = ["退款", "投诉", "赔偿"]
    negative_rating_threshold: int = 3

class AppConfig(BaseModel):
    ai: AIConfig
    shop: ShopConfig = ShopConfig()
    safety: SafetyConfig = SafetyConfig()

def load_config(path: str = "config/config.yaml") -> AppConfig:
    p = Path(path)
    if not p.exists():
        p = Path("config/config.yaml.example")
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)
