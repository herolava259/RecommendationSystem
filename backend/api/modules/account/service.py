import textwrap
from datetime import timedelta

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.templating import Jinja2Templates

from modules.account.error import LoginError,RefreshTokenRequiredError,SignupAccountError
from modules.account.domain import AccountDataAccess

from modules.account.model import (AccountModel,AccountClaimPrincipalModel,EmailVerificationModel,)

from infrastructures.task_workers.celery.tasks import send_email

import logging

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="api/infrastructures/emails/templates")


from modules.account.adapters import (CreateAccountRequest,
                                       CreateAccountResponse,
                                       LoginRequest,
                                       LoginResponse,
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
from modules.account.utils import AccountUtils


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

        # get principal data
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

        if await AccountDataAccess.exists_account_with_fields(mapping_fields={"signin_name": register_request.signin_name,
                                                                              "email": register_request.email,
                                                                              "email_verified": True
                                                                              }, session = session, and_between=True):
            raise SignupAccountError("signed-name or email are already registered")


        # step 3: persist user name-email

        signup_account_model = register_request.to_account_model()

        saved_account_model = await AccountDataAccess.insert_new_account(signup_account_model, session = session)

        if not saved_account_model:
            raise SignupAccountError("Failed to create new account")

        # create email_verification
        email_verify_model = EmailVerificationModel.create_new(signup_account_model)

        new_verify_model = await AccountDataAccess.insert_verification(email_verify_model, session = session)

        if not new_verify_model:
            return CreateAccountResponse(succeed=True,
                                        response_message = "Create new account successfully. Failed to email verification",
                                        navigate_home = False,
                                        need_verify_email= False,
                                        )
        # step 4:  doing create and save some related data for Account Model include: Account-Activation, Private-information (if avail)
        # , initializing ClaimPrincipal of the account

        new_principal = AccountClaimPrincipalModel.create_new(saved_account_model, custom_claims= {"pi": saved_account_model.personal_identifier})
        new_principal = await AccountDataAccess.insert_new_claim_principal(new_principal,session)
        if new_principal is None:
            navigate_home = False
        else:
            navigate_home = True

        # step 5: background job or sending a task to message broker about activating account, especially about sending email to activate account
        verify_link=AccountUtils.gen_email_verification_link(email=new_verify_model.email,
            activation_key=new_verify_model.activation_key,
            pi=saved_account_model.personal_identifier,)


        email_content=templates.get_template("email-verification.html").render(
            {"activation_key":new_verify_model.activation_key,
             "navigation_verification_link":verify_link,})
        send_email.delays([(register_request.signin_name,new_verify_model.email)],
            "Verification your account",
            email_content,)

        return CreateAccountResponse(succeed=True,
                                     response_message = "Created new account successfully, Please verify account to step next.",
                                     navigate_home = navigate_home,
                                     need_verify_email= True,
                                     additional_info= {"token": AccountUtils.create_access_token(new_principal,
                                                                                                expiry= timedelta(minutes=60),
                                                                                                refresh = False),

                                                       "personal_key": saved_account_model.personal_identifier})

    @classmethod
    async def _verify_password(cls, signin_name: str, pwd_plain: str) -> bool:
        account_model = await AccountDataAccess.find_account_by_signin_name(signin_name)

        if account_model is None:
            raise LoginError("Failed to find account with given name")

        return AccountUtils.verify_pwd_hash(pwd_plain, account_model.salt, account_model.pwd_hash)

    @classmethod
    async def _core_verify_email(cls, email: str, activation_key: int, pi: str, session: AsyncSession) -> bool:
        account = await AccountDataAccess.get_account_by_pi(pi, session = session)

        if account is None:
            return False
        email_used = await AccountDataAccess.exists_account_with_fields(mapping_fields={"email": email, "email_verified": True}, session = session, and_between=True)
        if email_used:
            return False

        return await AccountDataAccess.verify_email(account.id,email, activation_key, session = session)

    async def verify_email(self, req: EmailVerificationRequest, session: AsyncSession) -> EmailConfirmationResponse :

        if not await AccountDataAccess.exists_account_with_fields(mapping_fields={"signin_name": req.signin_name,}):
            raise SignupAccountError(f"Arguments {req.signin_name} is not exsited")

        confirmed = await AccountManager._core_verify_email(req.email, req.activation_key, req.personal_key, session)

        return EmailConfirmationResponse(
            succeed=confirmed,
            resp_msg="Email confirmed." if confirmed else "Email not confirmed.",
        )


    async def verify_email_by_link(self, token: str, session: AsyncSession) -> EmailConfirmationResponse:
        token_data: dict = AccountUtils.decode_url_safe_token(token)

        signature = token_data.pop("signature")

        if not AccountUtils.verify_signature(token_data,signature):
            raise SignupAccountError("Failed to verify email")
        confirmed = await self._core_verify_email(email=token_data["email"],
                                                  activation_key=token_data["activation_key"],
                                                  pi=token_data["pi"], session=session)
        return EmailConfirmationResponse(
            succeed=confirmed,
            resp_msg="Email confirmed." if confirmed else "Email not confirmed.",
        )

    def change_personal_information(self, req: ChangePersonalAccountInformationRequest, session: AsyncSession) -> ChangeAccountInformationResponse:
        pass


    def change_password(self, req: ChangePasswordRequest, session: AsyncSession) -> ChangePasswordResponse:
        pass

    def confirm_change_password(self, req: ConfirmChangePasswordRequest) -> ConfirmChangePasswordResponse:
        pass


