# Логика общения с LLM

from app.repositories.chat_messages import ChatMessagesStorage
from app.services.openrouter_client import OpenRouterClient
from app.core.enums import MessageRole
from app.core.config import Settings

class ChatUseCase:
    def __init__(
            self, 
            chat_repository: ChatMessagesStorage,
            or_client: OpenRouterClient,
            settings: Settings
            ) -> None :
        self._chat_repository = chat_repository
        self._or_client = or_client
        self._settings = settings

    async def ask(
            self,
            user_id: int,
            prompt: str,
            system_prompt: str | None = None 
            ) -> str:
        messages: list[dict[str, str]] = []

        # Если есть system-сообщение
        if system_prompt:
            messages.append(
                {
                    "role": MessageRole.SYSTEM,
                    "content": system_prompt
                }
            )
        
        # История сообщений 
        history = await self._chat_repository.show_last_n_messages(
            user_id = user_id,
            limit=self._settings.chat_history_limit
        )

        for message in history:
            messages.append(
                {
                    "role": message.role,
                    "content": message.content
                }
            )
        
        # Текущее сообщение 
        messages.append(
            {
                "role": MessageRole.USER,
                "content": prompt
            }
        )

        # Сохранение промпта в БД
        await self._chat_repository.add_message(
            user_id=user_id,
            role=MessageRole.USER,
            content=prompt
        )

        # Запрос к LLM
        response = await self._or_client.chat_completion(
            messages=messages
        )

        content_llm_response = response["choices"][0]["message"]["content"]

        # Сохранение сообщения LLM
        await self._chat_repository.add_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=content_llm_response
        )

        return content_llm_response
