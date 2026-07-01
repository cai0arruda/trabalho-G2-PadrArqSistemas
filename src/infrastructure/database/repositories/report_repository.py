from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.application.ports.repositories import IReportRepository
from src.domain.entities.report import Report
from src.infrastructure.database.models.models import ReportModel


class SQLAlchemyReportRepository(IReportRepository):
    def __init__(self, db: Session):
        self._db = db

    def save(self, report: Report) -> Report:
        model = ReportModel(
            id=report.id, exam_id=report.exam_id,
            doctor_id=report.doctor_id, content=report.content,
            conclusion=report.conclusion, created_at=report.created_at,
            updated_at=report.updated_at,
        )
        self._db.merge(model)
        self._db.commit()
        return report

    def find_by_id(self, report_id: UUID) -> Optional[Report]:
        m = self._db.query(ReportModel).filter_by(id=report_id).first()
        return self._to_entity(m) if m else None

    def find_by_exam_id(self, exam_id: UUID) -> Optional[Report]:
        m = self._db.query(ReportModel).filter_by(exam_id=exam_id).first()
        return self._to_entity(m) if m else None

    def _to_entity(self, m: ReportModel) -> Report:
        return Report(
            id=m.id, exam_id=m.exam_id, doctor_id=m.doctor_id,
            content=m.content, conclusion=m.conclusion,
            created_at=m.created_at, updated_at=m.updated_at,
        )
