from dataclasses import dataclass
from src.application.ports.repositories import IUserRepository
from src.domain.entities.user import User, UserRole
from src.domain.exceptions.domain_exceptions import DuplicateCPF
from src.infrastructure.auth.password_handler import PasswordHandler


@dataclass
class RegisterInput:
    cpf: str
    name: str
    email: str
    password: str
    role: str = "patient"


@dataclass
class RegisterOutput:
    user_id: str
    cpf: str
    name: str
    role: str


class RegisterUseCase:
    def __init__(self, user_repo: IUserRepository, password_handler: PasswordHandler):
        self._user_repo = user_repo
        self._password = password_handler

    def execute(self, input: RegisterInput) -> RegisterOutput:
        existing = self._user_repo.find_by_cpf(input.cpf)
        if existing:
            raise DuplicateCPF(f"CPF {input.cpf} já cadastrado")

        user = User(
            cpf=input.cpf,
            name=input.name,
            email=input.email,
            role=UserRole(input.role),
            password_hash=self._password.hash(input.password),
        )

        saved = self._user_repo.save(user)

        return RegisterOutput(
            user_id=str(saved.id),
            cpf=saved.cpf,
            name=saved.name,
            role=saved.role,
        )
