from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class ExamType(str, Enum):
    ECOGRAPHY = "ecography"
    ECG = "ecg"


class ExamStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Exam:
    patient_id: UUID
    exam_type: ExamType
    performed_by: UUID  # doctor user_id
    file_path: str
    id: UUID = field(default_factory=uuid4)
    status: ExamStatus = ExamStatus.PENDING
    performed_at: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""

    def complete(self) -> None:
        self.status = ExamStatus.COMPLETED

    def cancel(self) -> None:
        self.status = ExamStatus.CANCELLED
