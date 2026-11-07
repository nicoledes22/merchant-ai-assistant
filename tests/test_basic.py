from app.ai.prompts import system_prompt
from app.config import AIConfig, AppConfig

def test_prompt():
    p = system_prompt("测试店", "亲切", "7天无理由", ["FAQ"], ["不知道"])
    assert "测试店" in p and "FAQ" in p

def test_cfg():
    c = AppConfig(ai=AIConfig(base_url="x", api_key="y"))
    assert c.shop.name
