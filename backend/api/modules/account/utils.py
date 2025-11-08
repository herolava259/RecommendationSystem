import logging
import uuid

from datetime import datetime, timedelta

from itsdangerous import URLSafeTimedSerializer
import jwt
from passlib.context import CryptContext

from app.api.config import Config
from typing import Any
passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRY = 3600 * 2

serializer = URLSafeTimedSerializer(
    secret_key = Config.JWT_SECRET, salt="email"
)


class AccountUtils:

    @staticmethod
    def generate_pwd_hash(password) -> str:
        hsh = passwd_context.hash(password)

        return hsh
    @staticmethod
    def verify_pwd_hash(pwd: str, hsh: str) -> bool:
        return passwd_context.verify(pwd, hsh)

    @staticmethod
    def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):

        payload = {}

        payload["user"] = user_data
        payload["exp"] = datetime.now() + (expiry or timedelta(second=ACCESS_TOKEN_EXPIRY))
        payload["jti"] = str(uuid.uuid4())

        payload["refresh"] = refresh

        token = jwt.encode(payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            token_data = jwt.decode(
                jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
            )
            return token_data
        except jwt.PyJWTError as err:
            logging.exception(err)
            return None

    @staticmethod
    def decode_url_safe_token(token: str) -> Any:
        try:
            token_data = serializer.loads(token)
            return token_data
        except Exception as err:
            logging.error(str(err))
