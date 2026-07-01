from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.application.ports.repositories import IUserRepository
from src.domain.entities.user import User, UserRole
from src.infrastructure.database.models.models import UserModel


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, db: Session):
        self._db = db

    def save(self, user: User) -> User:
        existing = self._db.query(UserModel).filter_by(id=user.id).first()
        if existing:
            existing.name = user.name
            existing.email = user.email
            existing.is_active = user.is_active
        else:
            model = UserModel(
                id=user.id,
                cpf=user.cpf,
                name=user.name,
                email=user.email,
                role=user.role,
                password_hash=user.password_hash,
                is_active=user.is_active,
                created_at=user.created_at,
            )
            self._db.add(model)
        self._db.commit()
        return user

    def find_by_cpf(self, cpf: str) -> Optional[User]:
        model = self._db.query(UserModel).filter_by(cpf=cpf).first()
        return self._to_entity(model) if model else None

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        model = self._db.query(UserModel).filter_by(id=user_id).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, m: UserModel) -> User:
        return User(
            id=m.id,
            cpf=m.cpf,
            name=m.name,
            email=m.email,
            role=m.role,
            password_hash=m.password_hash,
            is_active=m.is_active,
            created_at=m.created_at,
        )
