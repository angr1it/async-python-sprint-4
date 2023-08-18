from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)

from core.config import app_settings

COOKIE_MAX_AGE = 3600
COOKIE_NAME = f"{app_settings.app_title}"


cookie_transport = CookieTransport(
    cookie_name=COOKIE_NAME,
    cookie_max_age=COOKIE_MAX_AGE,
    cookie_secure=False,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=app_settings.jwt_secret,
        lifetime_seconds=COOKIE_MAX_AGE,
    )


auth_backend = AuthenticationBackend(
    name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy
)
