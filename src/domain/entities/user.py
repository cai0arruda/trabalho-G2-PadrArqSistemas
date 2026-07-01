from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class UserRole(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


@dataclass
class User:
    cpf: str
    name: str
    email: str
    role: UserRole
    password_hash: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    def is_doctor(self) -> bool:
        return self.role == UserRole.DOCTOR

    def is_patient(self) -> bool:
        return self.role == UserRole.PATIENT
