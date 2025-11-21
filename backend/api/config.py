import os

from pydantic import NaiveDatetime
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class NaiveSettings(object):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    SECRET_KEY: str
    API_VERSION: int

    @classmethod
    def from_env_variables(cls) -> "NaiveSettings":
        types=Settings.__annotations__
        primitive_types=(int,float,str,bool)

        new_instance=cls()

        for n,t in types.items():
            if not issubclass(t,primitive_types):
                continue
            var=os.getenv(n,None)
            if not os.getenv(n,None):
                var = t()
            setattr(new_instance,n,var)
        return new_instance



from dotenv import load_dotenv

load_dotenv(".example.env")

Config = NaiveSettings.from_env_variables()



broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True