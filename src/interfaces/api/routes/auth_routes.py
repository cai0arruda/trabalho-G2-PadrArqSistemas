from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.interfaces.api.schemas.schemas import RegisterRequest, LoginRequest, TokenResponse
from src.interfaces.api.dependencies.deps import get_broker, password_handler, jwt_handler
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.application.use_cases.auth.login import LoginUseCase, LoginInput
from src.application.use_cases.auth.register import RegisterUseCase, RegisterInput
from src.domain.exceptions.domain_exceptions import InvalidCredentials, DuplicateCPF

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    use_case = RegisterUseCase(repo, password_handler)
    try:
        result = use_case.execute(RegisterInput(**body.model_dump()))
        return result
    except DuplicateCPF as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    use_case = LoginUseCase(repo, jwt_handler, password_handler)
    try:
        result = use_case.execute(LoginInput(**body.model_dump()))
        return result
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))
