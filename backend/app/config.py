from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/qmweb"
    REDIS_URL: str = "redis://localhost:6379/0"

    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""

    ALIYUN_ACCESS_KEY: str = ""
    ALIYUN_ACCESS_SECRET: str = ""

    JWT_SECRET_KEY: str = "change-me-to-a-random-secret"
    JWT_EXPIRE_HOURS: int = 24

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
