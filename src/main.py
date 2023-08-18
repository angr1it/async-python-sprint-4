from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import app_settings
from api import api_router
from api.auth import auth_router
from auth.auth import auth_backend
from schemas.auth import UserRead, UserCreate

app = FastAPI(
    title=app_settings.app_title,
    docs_url="/api/docs",
    openapi_url="/api/docs.json",
    default_response_class=ORJSONResponse,
)


app.include_router(
    router=api_router,
    prefix="/api",
)
app.include_router(
    router=auth_router.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    router=auth_router.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
