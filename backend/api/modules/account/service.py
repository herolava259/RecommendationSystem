from datetime import timedelta

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.modules.account.error import LoginError,RefreshTokenRequiredError,SignupAccountError
from api.modules.account.domain import AccountDataAccess

from api.modules.account.model import (AccountModel,AccountClaimPrincipalModel,)



from api.modules.account.adapters import (CreateAccountRequest,
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
                                        EmailConfirmationResponse,
                                        EmailVerificationRequest
                                        )
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

        if AccountUtils.verify_pwd_hash(req.password, account_model.salt ,account_model.pwd_hash):
            raise LoginError(f"Account password {req.signin_name} does not match")

        # TODO: retrieve role claim later, default: role: admin
        # create little session data

        # get principal model
        principal = await AccountDataAccess.get_claim_principal_of_account(account_model.id, session)
        if principal is None:
            principal  = AccountClaimPrincipalModel.no_claim()

        return LoginResponse(succeed=True,
                            response_message= f"Account logged in successfully",
                            access_token= AccountUtils.create_access_token(principal,
                                                                            expiry= timedelta(minutes=120),
                                                                            refresh=True)
        )

    def logout(self, req: LogoutRequest, session: AsyncSession) -> LogoutResponse:
        # TODO: recall token or mark the token is expired if persistence in server side
        # hash and save temporary in redis to validate
        # can using bloom filters to check presence of recalled access token
        return LogoutResponse(succeed=True)

    def refresh_token(self, req: RefreshTokenRequest) -> NewAccessTokenResponse:


        AccountUtils.verify_access_token(req.current_access_token, verify_for_refresh= True)

        curr_access_token = req.current_access_token

        if curr_access_token is None or curr_access_token.get("refresh", False) is False:
            raise RefreshTokenRequiredError("Current Access token is not permitted require new access token")

        return NewAccessTokenResponse(succeed=True,
                                      new_access_token=AccountUtils.create_access_token(
                                          curr_access_token.get("user", {}),
                                          expiry= timedelta(minutes=120),
                                          refresh=True
                                      ))

class AccountManager(object):

    async def register_account(self, register_request: CreateAccountRequest, session: AsyncSession) -> CreateAccountResponse:
        # step 1: validate input following by policy like password length, diversity of password, check email valid correct syntax
        # validate signin-name is unique, one email only signup only one account

        # step 2: retrieve information from persistence db to check include: exists of the email, sign name intent register,

        if await AccountDataAccess.exists_account_with_fields(mapping_fields={"signin_name": register_request.signin_name,"email": register_request.email}, session = session, and_between=True):
            raise SignupAccountError("signed-name or email are already registered")


        # step 3: persist user name-email

        signup_account_model = register_request.to_account_model()



        # step 4: background doing create and save some related data for Account Model include: Account-Activation, Private-information (if avail)
        # , initializing ClaimPrincipal of the account

        # step 5: background job or sending a task to message broker about activating account, especially about sending email to activate account

        pass

    def confirm_the_email_for_signup(self, req: EmailVerificationRequest) -> EmailConfirmationResponse:
        pass

    def change_personal_information(self, req: ChangePersonalAccountInformationRequest, session: AsyncSession) -> ChangeAccountInformationResponse:
        pass
    def change_password(self, req: ChangePasswordRequest, session: AsyncSession) -> ChangePasswordResponse:
        pass

    def confirm_change_password(self, req: ConfirmChangePasswordRequest) -> ConfirmChangePasswordResponse:
        pass


