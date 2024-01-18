from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""

    REDIS_SERVER: str = "127.0.0.1"
    REDIS_PORT: int = 6379

    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    MONGO_ROOT_USERNAME: str = ""
    MONGO_ROOT_PASSWORD: str = ""
    MONGO_SERVER: str = "127.0.0.1"
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str = ""

    MONGO_EXPRESS_LOGIN: str = ""
    MONGO_EXPRESS_PASSWORD: str = ""

    DEBUG: bool = True
    db_echo_log: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
