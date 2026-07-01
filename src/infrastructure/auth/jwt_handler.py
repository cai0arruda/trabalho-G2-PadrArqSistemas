from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.infrastructure.config.settings import settings


class JWTHandler:
    def create_token(self, data: dict) -> str:
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except JWTError:
            raise ValueError("Token inválido ou expirado")
