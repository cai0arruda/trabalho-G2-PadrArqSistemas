from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.application.ports.repositories import IExamRepository
from src.domain.entities.exam import Exam, ExamType, ExamStatus
from src.infrastructure.database.models.models import ExamModel


class SQLAlchemyExamRepository(IExamRepository):
    def __init__(self, db: Session):
        self._db = db

    def save(self, exam: Exam) -> Exam:
        model = ExamModel(
            id=exam.id, patient_id=exam.patient_id,
            exam_type=exam.exam_type, performed_by=exam.performed_by,
            file_path=exam.file_path, status=exam.status,
            notes=exam.notes, performed_at=exam.performed_at,
        )
        self._db.merge(model)
        self._db.commit()
        return exam

    def find_by_id(self, exam_id: UUID) -> Optional[Exam]:
        m = self._db.query(ExamModel).filter_by(id=exam_id).first()
        return self._to_entity(m) if m else None

    def find_by_patient_id(self, patient_id: UUID) -> list[Exam]:
        return [self._to_entity(m) for m in self._db.query(ExamModel).filter_by(patient_id=patient_id).all()]

    def list_all(self) -> list[Exam]:
        return [self._to_entity(m) for m in self._db.query(ExamModel).all()]

    def _to_entity(self, m: ExamModel) -> Exam:
        return Exam(
            id=m.id, patient_id=m.patient_id, exam_type=m.exam_type,
            performed_by=m.performed_by, file_path=m.file_path,
            status=m.status, notes=m.notes, performed_at=m.performed_at,
        )
