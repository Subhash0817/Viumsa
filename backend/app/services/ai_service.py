from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    async def generate_response(
        self,
        message: str,
        history: list[dict] | None = None
    ) -> str:
        pass


class AIService:

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def chat(
        self,
        message: str,
        history: list[dict] | None = None
    ) -> str:

        if not message.strip():
            raise ValueError("Message cannot be empty")

        return await self.provider.generate_response(
            message=message,
            history=history
        )