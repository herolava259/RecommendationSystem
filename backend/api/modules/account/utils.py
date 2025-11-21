import logging
import string
import uuid

from datetime import datetime, timedelta

from itsdangerous import URLSafeTimedSerializer

import jwt
from passlib.context import CryptContext

from config import Config
from typing import Any,Dict,Sequence

from cryptography.fernet import Fernet, MultiFernet
import base64
import json
from config import Config
from typing import Tuple
import secrets

from modules.account.error import VerifyTokenError,InvalidTokenError
from modules.account.model import AccountClaimPrincipalModel

import hmac
import hashlib
import base64

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRY = 3600 * 2

serializer = URLSafeTimedSerializer(
    secret_key = Config.JWT_SECRET, salt="email"
)


class AccountUtils:

    @staticmethod
    def generate_random_string():
        return Fernet.generate_key().decode("utf-8")

    @staticmethod
    def create_random_token(length=32):
        return secrets.token_urlsafe(length)
    @staticmethod
    def random_choice(seq: Sequence) -> Sequence:
        return secrets.choice(seq)

    @staticmethod
    def random_number(num_digits = 10) -> int:
        rand_numb = "".join(secrets.choice(string.digits) for _ in range(num_digits))
        return int(rand_numb)

    @staticmethod
    def create_key():
        return Fernet.generate_key().decode("utf-8")


    @staticmethod
    def sym_encrypt_object(data: Any, key: str| bytes | None = None) -> Tuple[bytes, bytes]:
        if key is None:
            key = Config.JWT_SECRET
        elif isinstance(key, str):
            key = base64.urlsafe_b64decode(key)

        fernet = Fernet(key)
        serialized_data = json.dumps(data).encode("utf-8")

        return key, fernet.encrypt(serialized_data)

    @staticmethod
    def sym_decrypt_object(data: bytes,target_type: type| None = None, key: str | bytes | None = None) -> Tuple[bytes, bytes]:
        if isinstance(key, str):
            key = base64.urlsafe_b64decode(key)
        elif key is None:
            key = Config.JWT_SECRET

        fernet = Fernet(key)
        plain_data = fernet.decrypt(data)
        deserialized_data = json.loads(plain_data)

        if target_type is None:
            return deserialized_data

        return target_type(**deserialized_data)

    @staticmethod
    def password_salt_format(pwd_plain: str, salt: str) -> str:
        return f"${salt}$-${pwd_plain}$"

    @staticmethod
    def generate_pwd_hash(password, salt: str) -> str:

        pwd_salt = AccountUtils.password_salt_format(password, salt)
        hsh = passwd_context.hash(pwd_salt)

        return hsh

    @staticmethod
    def verify_pwd_hash(pwd: str, salt: str, hsh: str) -> bool:
        pwd_salt = AccountUtils.password_salt_format(pwd, salt)

        return passwd_context.verify(pwd_salt, hsh)

    @staticmethod
    def create_access_token(account_claim_principal: AccountClaimPrincipalModel, expiry: timedelta = None, refresh: bool = False)\
            -> dict:

        payload: Dict[str, Any] = dict()

        payload["user"] = account_claim_principal.get_claim_of_account()
        payload["exp"] = datetime.now() + (expiry or timedelta(second=ACCESS_TOKEN_EXPIRY))
        payload["jti"] = str(uuid.uuid4())
        payload["refresh"] = refresh


        token = jwt.encode(payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        payload["token"] = token

        return payload

    @staticmethod
    def verify_access_token(payload: dict[str, Any], verify_for_refresh: bool = False) -> bool:

        if payload is None:
            raise VerifyTokenError("Payload is None")

        if payload.get("token", None) is None\
            and payload.get("exp", None) is None\
            and payload.get("jti", None) is None\
            and payload.get("refresh") is None:
            raise VerifyTokenError("Not information for verification token")

        plain_data=payload.copy()

        plain_data.pop("token")

        signature = jwt.encode(plain_data,key=Config.JWT_SECRET,algorithm=Config.JWT_ALGORITHM)

        if signature != payload["token"]:
            raise InvalidTokenError("Invalid token")

        if (not verify_for_refresh) and datetime.now() > payload["exp"]:
            raise InvalidTokenError("Token expired")




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
    def decode_url_safe_token(token: str) -> Any | dict:
        try:
            token_data = serializer.loads(token)
            return token_data
        except Exception as err:
            logging.error(str(err))

    @staticmethod
    def create_signature(data: dict) -> str:
        # need implementation
        h = hmac.new(Config.SecretKey.encode(), json.dumps(data).encode(), hashlib.sha512)
        digest = h.digest()
        return base64.b64encode(digest).decode()

    @staticmethod
    def verify_signature(data: dict, signature: str) -> bool:

        real_signature = AccountUtils.create_signature(data)

        return hmac.compare_digest(real_signature, signature)


    @staticmethod
    def encode_url_save_token(data: dict) -> str:

        token = serializer.dumps(data)
        return token

    @staticmethod
    def gen_email_verification_link(**kwargs) -> str:

        signature = AccountUtils.create_signature(kwargs)

        kwargs["signature"] = signature

        token = AccountUtils.encode_url_save_token(kwargs)

        return f"{Config.DOMAIN}/{Config.VERIFIER_URL}/account/email-verification?token={token}"

if __name__ == "__main__":
    print("Module: ", jwt)
    print("DIR", dir(jwt))
    print("FILE:",getattr(jwt,"__file__",None))