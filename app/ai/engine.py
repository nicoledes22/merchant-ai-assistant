from openai import OpenAI
from app.config import AppConfig
from app.ai import prompts
from app.models.schemas import AIReply

class AIEngine:
    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.client = OpenAI(base_url=cfg.ai.base_url, api_key=cfg.ai.api_key)

    def _chat(self, system, user):
        resp = self.client.chat.completions.create(
            model=self.cfg.ai.model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=self.cfg.ai.temperature,
            max_tokens=self.cfg.ai.max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()

    def classify_risk(self, content: str) -> str:
        if any(kw in content for kw in self.cfg.safety.manual_review_keywords):
            return "high"
        if any(kw in content for kw in ["太差", "失望", "退货", "不满意"]):
            return "medium"
        try:
            out = self._chat("你是质检员，只输出一个词。",
                             prompts.RISK_CLASSIFIER_PROMPT.format(content=content)).lower().strip().strip("。.")
            if out in ("low", "medium", "high"):
                return out
        except Exception:
            pass
        return "low"

    def reply_consultation(self, content, item, amount):
        system = prompts.system_prompt(self.cfg.shop.name, self.cfg.shop.tone,
            self.cfg.shop.return_policy, self.cfg.shop.faq, self.cfg.shop.forbidden_words)
        user = prompts.CONSULTATION_USER_TMPL.format(content=content, item=item, amount=amount)
        text = self._chat(system, user)
        escalate = text.startswith("[ESCALATE]")
        if escalate:
            text = text.replace("[ESCALATE]", "").strip()
        risk = self.classify_risk(content)
        return AIReply(reply_text=text, category="consultation", risk_level=risk,
                       need_human_review=escalate or risk == "high",
                       reason="命中高危词" if risk == "high" else "")

    def reply_positive_review(self, content, stars, item):
        system = prompts.system_prompt(self.cfg.shop.name, self.cfg.shop.tone,
            self.cfg.shop.return_policy, self.cfg.shop.faq, self.cfg.shop.forbidden_words)
        user = prompts.POSITIVE_REVIEW_USER_TMPL.format(content=content, stars=stars, item=item)
        text = self._chat(system, user)
        return AIReply(reply_text=text, category="positive_review", risk_level="low",
                       need_human_review=not self.cfg.safety.auto_send_positive_review)

    def reply_negative_review(self, content, stars, item, amount):
        system = prompts.system_prompt(self.cfg.shop.name, self.cfg.shop.tone,
            self.cfg.shop.return_policy, self.cfg.shop.faq, self.cfg.shop.forbidden_words)
        user = prompts.NEGATIVE_REVIEW_USER_TMPL.format(content=content, stars=stars, item=item, amount=amount)
        text = self._chat(system, user)
        return AIReply(reply_text=text, category="negative_review", risk_level="high",
                       need_human_review=not self.cfg.safety.auto_send_negative_review,
                       reason="差评默认进入人工审核")
