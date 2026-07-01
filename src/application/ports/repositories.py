from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.entities.patient import Patient
from src.domain.entities.exam import Exam
from src.domain.entities.report import Report


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[User]: ...

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]: ...


class IPatientRepository(ABC):
    @abstractmethod
    def save(self, patient: Patient) -> Patient: ...

    @abstractmethod
    def find_by_id(self, patient_id: UUID) -> Optional[Patient]: ...

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[Patient]: ...

    @abstractmethod
    def list_all(self) -> list[Patient]: ...


class IExamRepository(ABC):
    @abstractmethod
    def save(self, exam: Exam) -> Exam: ...

    @abstractmethod
    def find_by_id(self, exam_id: UUID) -> Optional[Exam]: ...

    @abstractmethod
    def find_by_patient_id(self, patient_id: UUID) -> list[Exam]: ...

    @abstractmethod
    def list_all(self) -> list[Exam]: ...


class IReportRepository(ABC):
    @abstractmethod
    def save(self, report: Report) -> Report: ...

    @abstractmethod
    def find_by_id(self, report_id: UUID) -> Optional[Report]: ...

    @abstractmethod
    def find_by_exam_id(self, exam_id: UUID) -> Optional[Report]: ...
