from typing import Annotated

from fastapi import APIRouter, Depends, status, BackgroundTasks, Query, HTTPException, Path, Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse

from modules.account.dependency import get_current_user, RefreshTokenBearer, AccessTokenBearer
from modules.account.service import AccountManager, SigninManager
from modules.account.utils import AccountUtils
from modules.account.ports import (
    CreateAccountResponse,
    CreateAccountRequest, EmailConfirmationResponse, EmailVerificationRequest, LoginRequest, LogoutResponse,
    LogoutRequest, RefreshTokenRequest
)
from infrastructures.persistence.postgresql.db import get_session

account_router = APIRouter(prefix="/account", tags=["account"])
account_manager = AccountManager()
signin_manager = SigninManager()

#############
## account register segment
############

@account_router.post("/signup", status_code=status.HTTP_201_CREATED,
                     response_model=CreateAccountResponse)
async def create_account(
        model: CreateAccountRequest,
        session: AsyncSession = Depends(get_session)
):
    return await account_manager.register_account(model, session)


@account_router.post("/confirm-email", status_code=status.HTTP_200_OK,
                     response_model=EmailConfirmationResponse)
async def confirm_email_directly(mreq: EmailVerificationRequest, session: AsyncSession = Depends(get_session)):
    return await account_manager.verify_email(mreq, session)


@account_router.get("confirm-email-by-link/", status_code=status.HTTP_202_ACCEPTED,
                    response_model=EmailConfirmationResponse)
async def confirm_email_by_link(token: Annotated[str | None, Path(max_length=128, default="123")],
                                session: AsyncSession = Depends(get_session)):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    return await account_manager.verify_email_by_link(token, session)


###########
## sign-in segment
##########

@account_router.post("signin/")
async def login_account(signin_req: LoginRequest, session: AsyncSession = Depends(get_session)):

    resp = await signin_manager.login(signin_req, session)

    if not resp:
        return JSONResponse(content= {"message": "Login failed."}, status_code=status.HTTP_401_UNAUTHORIZED)
    if not resp.succeed:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=resp.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=resp.model_dump())


@account_router.post("logout", status_code=status.HTTP_202_ACCEPTED,
                     response_model=LogoutResponse)
async def logout_account(logout_model: LogoutRequest,session: AsyncSession = Depends(get_session)):

    return await signin_manager.logout(logout_model, session)


@account_router.post("/refresh-token-test")
async def test_refresh_token(req: Request, resp: Response, session: AsyncSession = Depends(get_session)):
    pass


@account_router.post("/refresh-token")
async def refresh_token(req: RefreshTokenRequest,session: AsyncSession = Depends(get_session)):
    cnt = await signin_manager.refresh_token(req, session)

    if cnt.succeed:
        return JSONResponse(status_code=status.HTTP_200_OK, content=cnt.model_dump())
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=cnt.model_dump())




