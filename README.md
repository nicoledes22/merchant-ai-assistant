# 🤖 Merchant AI Assistant

个体商家智能客服助手 — 自动接咨询、回好评、处理差评。

## 功能
- 💬 智能咨询应答（基于商品知识库）
- ⭐ 好评自动感谢
- 😠 差评危机处理（道歉+方案+人工审核）
- 🛡️ 高风险词命中自动转人工
- 🔌 通用 Webhook 接入，预留多平台适配器

## 快速开始
```bash
pip install -r requirements.txt
cp config/config.yaml.example config/config.yaml  # 填入你的大模型 API Key
uvicorn app.main:app --port 8000
```

打开 http://localhost:8000/dashboard/
