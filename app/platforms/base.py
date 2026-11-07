from abc import ABC, abstractmethod
from app.models.schemas import IncomingMessage, AIReply

class PlatformAdapter(ABC):
    @abstractmethod
    def parse_incoming(self, raw: dict) -> IncomingMessage: ...
    @abstractmethod
    def send_reply(self, user_id: str, reply: AIReply) -> bool: ...
