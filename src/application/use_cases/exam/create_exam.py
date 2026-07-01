from dataclasses import dataclass
from uuid import UUID
from src.application.ports.repositories import IExamRepository, IPatientRepository
from src.application.ports.message_broker import IMessageBroker
from src.domain.entities.exam import Exam, ExamType
from src.domain.events.domain_events import ExamPerformed
from src.domain.exceptions.domain_exceptions import PatientNotFound


@dataclass
class CreateExamInput:
    patient_id: str
    exam_type: str
    performed_by: str
    file_path: str
    notes: str = ""


@dataclass
class CreateExamOutput:
    exam_id: str
    patient_id: str
    exam_type: str
    status: str
    file_path: str


class CreateExamUseCase:
    def __init__(
        self,
        exam_repo: IExamRepository,
        patient_repo: IPatientRepository,
        broker: IMessageBroker,
    ):
        self._exam_repo = exam_repo
        self._patient_repo = patient_repo
        self._broker = broker

    def execute(self, input: CreateExamInput) -> CreateExamOutput:
        patient = self._patient_repo.find_by_id(UUID(input.patient_id))
        if not patient:
            raise PatientNotFound(f"Paciente {input.patient_id} não encontrado")

        exam = Exam(
            patient_id=UUID(input.patient_id),
            exam_type=ExamType(input.exam_type),
            performed_by=UUID(input.performed_by),
            file_path=input.file_path,
            notes=input.notes,
        )

        saved = self._exam_repo.save(exam)

        # Publica evento de domínio — EDA em ação
        event = ExamPerformed(
            exam_id=saved.id,
            patient_id=saved.patient_id,
            exam_type=saved.exam_type,
        )
        self._broker.publish("exam.performed", event)

        return CreateExamOutput(
            exam_id=str(saved.id),
            patient_id=str(saved.patient_id),
            exam_type=saved.exam_type,
            status=saved.status,
            file_path=saved.file_path,
        )
