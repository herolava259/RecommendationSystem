from typing import List, override, Set

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import Annotated

from infrastructures.caching.redis import token_in_blocklist
from infrastructures.persistence.postgresql.db import get_session
from modules.account.domain import AccountDataAccess

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
from .model import AccountModel, AccountClaimPrincipalModel

from .service import SigninManager
from .utils import AccountHelper

signin_manager = SigninManager()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error = auto_error)


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None | dict:

        def _token_valid(enc_token: str):
            token_info = AccountHelper.decode_token(enc_token)

            return token_info is not None
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = AccountHelper.decode_token(token)

        if not _token_valid(token):
            raise InvalidTokenError()

        if await token_in_blocklist(token):
            raise InsufficientPermissionError()

        self.verify_token_data(token_data)

        return token_data

    @staticmethod
    def token_valid(token: str) -> bool:
        token_data = AccountHelper.decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError()

class AccessTokenBearer(TokenBearer):

    @override
    def verify_token_data(self, token_data):
        if token_data and not token_data["refresh"]:
            raise AccessTokenRequiredError()


class RefreshTokenBearer(TokenBearer):

    @override
    def verify_token_data(self, token_data):
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequiredError()




async def get_current_user(
        token_details: Annotated[dict, Depends(AccessTokenBearer())],
        session: AsyncSession = Depends(get_session)
) -> AccountModel:
    user_email = token_details["user"]["email"]

    user = await AccountDataAccess.get_account_by_email(user_email, session, include_properties="claim_principal")

    return user



# failover

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles: Set[str] = set(allowed_roles)

    def __call__(self, current_user: AccountModel = Depends(get_current_user)) -> bool:

        if not current_user.active:
            raise AccountNotVerifiedError()
        claim_principal: AccountClaimPrincipalModel = current_user.claim_principal

        if claim_principal is None:
            raise AccountNotVerifiedError()
        roles = claim_principal.query_by_key("roles")

        if not (roles & self.allowed_roles):
            raise InsufficientPermissionError()

        return True


