from datetime import timedelta

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.modules.account.error import LoginError
from api.modules.account.scheme import AccountDataAccess

from api.modules.account.model import (CreateAccountRequest,
                    CreateAccountResponse,
                    LoginRequest,
                    LoginResponse,
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
                    ConfirmChangePasswordResponse,
                    AccountModel)
from api.modules.account.utils import AccountUtils


class SigninManager(object):

    async def login(self, req: LoginRequest, session: AsyncSession) -> LoginResponse:
        account_model: AccountModel | None = await AccountDataAccess.get_account_by_name(req.signin_name, session)

        if account_model is None:
            return LoginResponse(succeed=False,
                                response_message=f"Cannot find account with name {req.signin_name}",
                                access_token=None,)

        if not account_model.active:
            raise LoginError(f"Account {req.signin_name} not active")

        if AccountUtils.verify_pwd_hash(req.password, account_model.pwd_hash):
            raise LoginError(f"Account password {req.signin_name} does not match")

        # TODO: retrieve role claim later, default: role: admin
        # create little session data

        return LoginResponse(succeed=True,
                            response_message= f"Account logged in successfully",
                            access_token= AccountUtils.create_access_token(user_data = {"name": account_model.signin_name,
                                                                            "role": "admin"},
                                                                            expiry= timedelta(minutes=120),
                                                                            refresh=True)
        )

    def logout(self, req: LogoutRequest, session: AsyncSession) -> LogoutResponse:
        # TODO: recall token or mark the token is expired
        return LogoutResponse(succeed=True)

    def refresh_token(self, req: RefreshTokenRequest) -> NewAccessTokenResponse:
        pass


class AccountManager(object):

    def register_account(self, register_request: CreateAccountRequest, session: AsyncSession) -> CreateAccountResponse:
        pass

    def change_personal_information(self, req: ChangePersonalAccountInformationRequest, session: AsyncSession) -> ChangeAccountInformationResponse:
        pass
    def change_password(self, req: ChangePasswordRequest, session: AsyncSession) -> ChangePasswordResponse:
        pass

    def confirm_change_password(self, req: ConfirmChangePasswordRequest) -> ConfirmChangePasswordResponse:
        pass


