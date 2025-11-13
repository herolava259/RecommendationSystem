from api.common.errors import ApplicationException


class RoleException(ApplicationException):
    pass
class InvalidCredentialError(RoleException):
    pass
