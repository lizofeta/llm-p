# Доменные исключения

class LLMPError(Exception):
    """ Базовая ошибка приложения """
    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(message)

# 4xx-like ошибки

class ConflictError(LLMPError):
    """ 
    Исключение, возникающее при конфликтах, например:
    - Пользователь с таким email уже зарегистрирован 
    - Имя пользователя уже занято 
    """
    pass

class UnauthorizedError(LLMPError):
    """ 
    Ошибка аутентификации (неверный пароль / токен)
    """
    pass

class ForbiddenError(LLMPError):
    """ Отсутствие прав доступа """
    pass

class NotFoundError(LLMPError):
    """ Объект не найден """
    pass

# Внешние сервисы

class ExternalServiceError(LLMPError):
    """ Ошибка при обращении к внешнему сервису """
    def __init__(self, message = None):
        super().__init__(message)

class ExternalServiceTimeout(ExternalServiceError):
    pass

# Более узкие ошибки конкретных кейсов

class EmailAlreadyExistsError(ConflictError):
    def __init__(self):
        super().__init__("Пользователь с таким email уже зарегистрирован")

class WrongPasswordError(UnauthorizedError):
    def __init__(self):
        super().__init__("Введён неверный пароль")
