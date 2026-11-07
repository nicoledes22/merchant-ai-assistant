import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import load_config
from app.ai.engine import AIEngine

def main():
    cfg = load_config()
    if "your-api-key" in cfg.ai.api_key:
        print("⚠️  请先在 config/config.yaml 填入真实 API Key"); return
    e = AIEngine(cfg)
    print("\n=== 咨询 ===")
    print(e.reply_consultation("M码多大？160能穿吗？", "卫衣", 99).reply_text)
    print("\n=== 好评 ===")
    print(e.reply_positive_review("质量很好，物流快！", 5, "卫衣").reply_text)
    print("\n=== 差评 ===")
    r = e.reply_negative_review("收到就破了，太差", 1, "卫衣", 99)
    print(r.reply_text, "\n需人工:", r.need_human_review)

if __name__ == "__main__":
    main()
