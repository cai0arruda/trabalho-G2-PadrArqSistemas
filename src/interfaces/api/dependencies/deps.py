from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.infrastructure.database.repositories.patient_repository import SQLAlchemyPatientRepository
from src.infrastructure.database.repositories.exam_repository import SQLAlchemyExamRepository
from src.infrastructure.database.repositories.report_repository import SQLAlchemyReportRepository
from src.infrastructure.auth.jwt_handler import JWTHandler
from src.infrastructure.auth.password_handler import PasswordHandler
from src.infrastructure.messaging.rabbitmq_broker import FakeBroker

bearer = HTTPBearer()
jwt_handler = JWTHandler()
password_handler = PasswordHandler()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    try:
        payload = jwt_handler.decode_token(credentials.credentials)
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )


def require_doctor(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") not in ("doctor", "admin"):
        raise HTTPException(status_code=403, detail="Acesso restrito a médicos")
    return current_user


def get_broker():
    return FakeBroker()
