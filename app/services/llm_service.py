import asyncio
from app.core.config import settings
from groq import AsyncGroq

class LLMService:
    def __init__(self):
        self.async_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    def generate_response(self, prompt: str) -> str:
        from groq import Groq
        sync_client = Groq(api_key=settings.GROQ_API_KEY)
        response = sync_client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1024
        )
        chat_response = response.choices[0].message.content
           
        return chat_response if chat_response else "No response generated."
    
    async def generate_stream(self, prompt: str, demo_mode: bool = False):
        stream = await self.async_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1024,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                if demo_mode:
                    await asyncio.sleep(0.05)