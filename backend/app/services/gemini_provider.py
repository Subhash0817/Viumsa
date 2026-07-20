from google import genai

from app.core.config import settings
from app.services.ai_service import AIProvider


class GeminiProvider(AIProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def generate_response(
        self,
        message: str,
        history: list[dict] | None = None
    ) -> str:

        conversation_context = ""

        if history:
            for item in history:
                role = item["role"]
                content = item["content"]

                if role == "user":
                    speaker = "User"
                else:
                    speaker = "Viumsa"

                conversation_context += (
                    f"{speaker}: {content}\n"
                )

        prompt = f"""
You are Viumsa, an AI assistant designed to help people learn, explore,
solve problems, and get things done.

Your name is Viumsa.
Be helpful, clear, natural, and concise.
Use the conversation history when it is relevant.
Do not claim that Viumsa created or trained the underlying AI model.
If specifically asked about your underlying model or provider, answer truthfully.

Conversation history:
{conversation_context}

Current user message:
User: {message}

Viumsa:
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        return response.text or ""