# error from Account module
from api.common.errors import ApplicationException


class AccountException(ApplicationException):
    pass
class VerifyEmailError(AccountException):
    pass

class InvalidTokenError(AccountException):
    pass

class LoginError(AccountException):
    pass

class AccessTokenRequiredError(AccountException):
    pass

class RefreshTokenRequiredError(AccountException):
    pass

class AccountAlreadyExistsError(AccountException):
    pass

class InvalidCredentialsError(AccountException):
    pass


class AccountNotVerifiedError(AccountException):
    pass


class InsufficientPermissionError(AccountException):
    pass