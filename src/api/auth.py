import uuid

from fastapi_users import FastAPIUsers

from auth.db import User
from auth.manager import get_user_manager
from auth.auth import auth_backend

auth_router = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = auth_router.current_user(optional=True)
