import asyncio

from app.services.gemini_provider import GeminiProvider


async def main():
    provider = GeminiProvider()

    response = await provider.generate_response(
        "Say hello in one short sentence. Your name is Viumsa."
    )

    print(response)


asyncio.run(main())