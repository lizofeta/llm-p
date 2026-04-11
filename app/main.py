from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes_auth import auth_router
from app.api.routes_chat import chat_router
from app.core.config import get_settings


def create_app():
    settings = get_settings()

    app = FastAPI(title=settings.app_name)

    # routers
    app.include_router(auth_router)
    app.include_router(chat_router)

    # health
    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "environment": settings.env
        }
    
    # root
    @app.get("/")
    def root():
        return {"message": "Welcome!"}
    
    # глобальный обработчик неожиданных ошибок
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
    
    return app


app = create_app()
