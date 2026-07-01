from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class DomainEvent:
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ExamPerformed(DomainEvent):
    exam_id: UUID = None
    patient_id: UUID = None
    exam_type: str = ""

    def to_dict(self) -> dict:
        return {
            "event": "ExamPerformed",
            "exam_id": str(self.exam_id),
            "patient_id": str(self.patient_id),
            "exam_type": self.exam_type,
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass
class ReportIssued(DomainEvent):
    report_id: UUID = None
    exam_id: UUID = None
    patient_id: UUID = None
    doctor_id: UUID = None

    def to_dict(self) -> dict:
        return {
            "event": "ReportIssued",
            "report_id": str(self.report_id),
            "exam_id": str(self.exam_id),
            "patient_id": str(self.patient_id),
            "doctor_id": str(self.doctor_id),
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass
class ResultAvailable(DomainEvent):
    patient_id: UUID = None
    exam_id: UUID = None

    def to_dict(self) -> dict:
        return {
            "event": "ResultAvailable",
            "patient_id": str(self.patient_id),
            "exam_id": str(self.exam_id),
            "occurred_at": self.occurred_at.isoformat(),
        }
