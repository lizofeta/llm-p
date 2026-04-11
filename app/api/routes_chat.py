# HTTP-ендпоинты чата

from fastapi import APIRouter, HTTPException, status 

from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.api.deps import ChatUseCaseDep, UserIDDEP
from app.core.errors import ExternalServiceError, ExternalServiceTimeout

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_message(
    user_id: UserIDDEP,
    data: ChatRequest,
    chat_usecase: ChatUseCaseDep
) -> ChatResponse:
    try:
        llm_response = await chat_usecase.ask(
            user_id,
            prompt=data.prompt,
            temperature=data.temperature,
            max_history=data.max_history,
            system_prompt=data.system
        )
        return ChatResponse(answer=llm_response)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
    except ExternalServiceTimeout as e:
        raise HTTPException(
            status_code=504,
            detail=f"Ошибка сети: {e}"
        )


@chat_router.get(
    "/history",
    response_model=list[ChatHistoryResponse],
    status_code=status.HTTP_200_OK
)
async def history(
    max_history: int,
    user_id: UserIDDEP,
    chat_usecase: ChatUseCaseDep
) -> list[ChatHistoryResponse]:
    chat_history = await chat_usecase.get_chat_history(
        user_id, limit=max_history
    )
    return chat_history


@chat_router.delete(
    "/history",
    status_code=status.HTTP_200_OK
)
async def delete(
    user_id: UserIDDEP,
    chat_usecase: ChatUseCaseDep
) -> None:
    await chat_usecase.delete_history(user_id)
    return "История диалога успешно удалена"
