# Логика общения с LLM

from app.repositories.chat_messages import ChatMessagesStorage
from app.db.models import ChatMessage
from app.services.openrouter_client import OpenRouterClient
from app.core.enums import MessageRole

class ChatUseCase:
    def __init__(
            self, 
            chat_repository: ChatMessagesStorage,
            or_client: OpenRouterClient
            ) -> None :
        self._chat_repository = chat_repository
        self._or_client = or_client
    
    async def get_chat_history(
            self,
            user_id: int,
            limit: int 
    ) -> list[ChatMessage]:
        history = await self._chat_repository.show_last_n_messages(
            user_id,
            limit
        )
        return history
    
    async def delete_history(
            self,
            user_id: int
    ) -> None:
        await self._chat_repository.delete_chat_history(user_id)

    async def ask(
            self,
            user_id: int,
            prompt: str,
            temperature: float,
            max_history: int,
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
        history = await self.get_chat_history(
            user_id,
            max_history
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
            messages=messages,
            temperature=temperature
        )

        content_llm_response = response["choices"][0]["message"]["content"]

        # Сохранение сообщения LLM
        await self._chat_repository.add_message(
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=content_llm_response
        )

        return content_llm_response
