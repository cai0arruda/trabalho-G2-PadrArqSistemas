from dataclasses import dataclass
from datetime import date
from uuid import UUID
from src.application.ports.repositories import IPatientRepository
from src.domain.entities.patient import Patient
from src.domain.exceptions.domain_exceptions import DuplicateCPF


@dataclass
class CreatePatientInput:
    cpf: str
    name: str
    birth_date: str  # ISO format: YYYY-MM-DD
    phone: str
    user_id: str


@dataclass
class CreatePatientOutput:
    patient_id: str
    cpf: str
    name: str


class CreatePatientUseCase:
    def __init__(self, patient_repo: IPatientRepository):
        self._patient_repo = patient_repo

    def execute(self, input: CreatePatientInput) -> CreatePatientOutput:
        existing = self._patient_repo.find_by_cpf(input.cpf)
        if existing:
            raise DuplicateCPF(f"Paciente com CPF {input.cpf} já existe")

        patient = Patient(
            cpf=input.cpf,
            name=input.name,
            birth_date=date.fromisoformat(input.birth_date),
            phone=input.phone,
            user_id=UUID(input.user_id),
        )

        saved = self._patient_repo.save(patient)

        return CreatePatientOutput(
            patient_id=str(saved.id),
            cpf=saved.cpf,
            name=saved.name,
        )
