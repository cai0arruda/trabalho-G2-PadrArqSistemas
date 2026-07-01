from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.application.ports.repositories import IPatientRepository
from src.domain.entities.patient import Patient
from src.infrastructure.database.models.models import PatientModel


class SQLAlchemyPatientRepository(IPatientRepository):
    def __init__(self, db: Session):
        self._db = db

    def save(self, patient: Patient) -> Patient:
        model = PatientModel(
            id=patient.id,
            cpf=patient.cpf,
            name=patient.name,
            birth_date=patient.birth_date,
            phone=patient.phone,
            user_id=patient.user_id,
            created_at=patient.created_at,
        )
        self._db.merge(model)
        self._db.commit()
        return patient

    def find_by_id(self, patient_id: UUID) -> Optional[Patient]:
        m = self._db.query(PatientModel).filter_by(id=patient_id).first()
        return self._to_entity(m) if m else None

    def find_by_cpf(self, cpf: str) -> Optional[Patient]:
        m = self._db.query(PatientModel).filter_by(cpf=cpf).first()
        return self._to_entity(m) if m else None

    def list_all(self) -> list[Patient]:
        return [self._to_entity(m) for m in self._db.query(PatientModel).all()]

    def _to_entity(self, m: PatientModel) -> Patient:
        return Patient(
            id=m.id, cpf=m.cpf, name=m.name,
            birth_date=m.birth_date, phone=m.phone,
            user_id=m.user_id, created_at=m.created_at,
        )
