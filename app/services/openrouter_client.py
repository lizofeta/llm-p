# Клиент OpenRouter / LLM

import httpx 
from typing import Any 

from app.core.errors import ExternalServiceError
from app.core.config import Settings

class OpenRouterClient:
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openrouter_api_key
        self._base_url = settings.openrouter_base_url
        self._model = settings.openrouter_model
        self._referer = settings.openrouter_site_url
        self._title = settings.openrouter_app_name
    
    def _build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._referer,
            "X-Title": self._title,
            "Content-Type": "application/json"
        }
    
    async def chat_completion(
            self,
            messages: list[dict[str, str]],
            timeout: int = 20
            ) -> dict[str, Any]:
        payload = {
            "model": self._model,
            "messages": messages
        }

        url = f"{self._base_url}/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    url,
                    headers=self._build_headers(),
                    json=payload
                )
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Ошибка сети: {e}")
        
        if response.status_code != 200:
            raise ExternalServiceError(
                f"Ошибка OpenRouter {response.status_code}: {response.text}"
                )
        
        try:
            return response.json()
        except ValueError:
            raise ExternalServiceError("Некорректный JSON в ответе OpenRouter")
        