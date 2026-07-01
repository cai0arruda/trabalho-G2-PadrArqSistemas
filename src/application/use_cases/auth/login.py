from dataclasses import dataclass
from src.application.ports.repositories import IUserRepository
from src.domain.exceptions.domain_exceptions import InvalidCredentials, UserNotFound
from src.infrastructure.auth.jwt_handler import JWTHandler
from src.infrastructure.auth.password_handler import PasswordHandler


@dataclass
class LoginInput:
    cpf: str
    password: str


@dataclass
class LoginOutput:
    access_token: str
    token_type: str
    user_id: str
    role: str
    name: str


class LoginUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        jwt_handler: JWTHandler,
        password_handler: PasswordHandler,
    ):
        self._user_repo = user_repo
        self._jwt = jwt_handler
        self._password = password_handler

    def execute(self, input: LoginInput) -> LoginOutput:
        user = self._user_repo.find_by_cpf(input.cpf)
        if not user:
            raise InvalidCredentials("CPF ou senha inválidos")

        if not self._password.verify(input.password, user.password_hash):
            raise InvalidCredentials("CPF ou senha inválidos")

        token = self._jwt.create_token(
            {"sub": str(user.id), "role": user.role, "cpf": user.cpf}
        )

        return LoginOutput(
            access_token=token,
            token_type="bearer",
            user_id=str(user.id),
            role=user.role,
            name=user.name,
        )
