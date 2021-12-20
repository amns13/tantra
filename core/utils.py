from datetime import datetime, timedelta
from typing import Any, Optional

import jwt
from django.conf import settings


def is_dev_environment() -> bool:
    """Checks if currently working on dev."""
    return settings.ENVIRONMENT == 'dev'


def get_token(expires_in: timedelta, **kwargs: str) -> str:
    payload: dict[str, Any] = {'exp': datetime.now() + expires_in, **kwargs}
    return jwt.encode(payload=payload, key=settings.SECRET_KEY,
                      algorithm=settings.ENCRYPTION_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=[
            settings.ENCRYPTION_ALGORITHM])
