from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .model import (CreateAccountRequest,
                    CreateAccountResponse,
                    LoginRequest,
                    AccessTokenResponse,
                    LogoutResponse,
                    LogoutRequest,
                    RefreshTokenRequest,
                    NewAccessTokenResponse,
                    ChangePersonalAccountInformationRequest,
                    ChangeAccountInformationResponse,
                    ChangePasswordRequest,
                    ChangePasswordResponse,
                    ConfirmChangePasswordRequest,
                    ConfirmChangePasswordResponse)

class SigninManager(object):
    def register_account(self, register_request: CreateAccountRequest, session: AsyncSession) -> CreateAccountResponse:
        pass

    def login(self, req: LoginRequest, session: AsyncSession) -> AccessTokenResponse:
        pass

    def logout(self, req: LogoutRequest, session: AsyncSession) -> LogoutResponse:
        pass

    def refresh_token(self, req: RefreshTokenRequest) -> NewAccessTokenResponse:
        pass


class AccountManager(object):
    def change_personal_information(self, req: ChangePersonalAccountInformationRequest, session: AsyncSession) -> ChangeAccountInformationResponse:
        pass
    def change_password(self, req: ChangePasswordRequest, session: AsyncSession) -> ChangePasswordResponse:
        pass

    def confirm_change_password(self, req: ConfirmChangePasswordRequest) -> ConfirmChangePasswordResponse:
        pass


