from typing import Any, List

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

# from src.db.main import get_session
# from src.db.models import User
# from src.db.redis import token_in_blocklist

from modules.account.error import (
    InvalidTokenError,
    RefreshTokenRequiredError,
    AccessTokenRequiredError,
    InsufficientPermissionError,
    AccountNotVerifiedError
)

from .service import AccountManager, SigninManager
from .utils import AccountUtils

signin_manager = SigninManager()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error = auto_error)


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:

        def _token_valid(token_data: str):
            token_info = AccountUtils.decode_token(token_data)

            return token_info is not None
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = AccountUtils.decode_token(token)

        if not _token_valid(token):
            raise InvalidTokenError()



