from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Report:
    exam_id: UUID
    doctor_id: UUID
    content: str
    conclusion: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update(self, content: str, conclusion: str) -> None:
        self.content = content
        self.conclusion = conclusion
        self.updated_at = datetime.utcnow()
