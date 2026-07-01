from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://medexam:medexam@db:5432/medexam"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    SECRET_KEY: str = "changeme-in-production-use-env-var"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    UPLOAD_DIR: str = "/app/uploads"

    class Config:
        env_file = ".env"


settings = Settings()
