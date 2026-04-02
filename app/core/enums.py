from enum import StrEnum

class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"

class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
