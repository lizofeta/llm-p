# Pydantic схема запроса к чату и схема ответа

from pydantic import BaseModel, Field 
from typing import Optional


class ChatRequest(BaseModel):
    prompt: str 
    system: Optional[str] = None 
    max_history: int = Field(default=10, ge=0, le=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    answer: str
