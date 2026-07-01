from dataclasses import dataclass
from uuid import UUID
from src.application.ports.repositories import IReportRepository, IExamRepository, IPatientRepository
from src.application.ports.message_broker import IMessageBroker
from src.domain.entities.report import Report
from src.domain.events.domain_events import ReportIssued, ResultAvailable
from src.domain.exceptions.domain_exceptions import ExamNotFound


@dataclass
class CreateReportInput:
    exam_id: str
    doctor_id: str
    content: str
    conclusion: str


@dataclass
class CreateReportOutput:
    report_id: str
    exam_id: str
    doctor_id: str
    conclusion: str
    created_at: str


class CreateReportUseCase:
    def __init__(
        self,
        report_repo: IReportRepository,
        exam_repo: IExamRepository,
        patient_repo: IPatientRepository,
        broker: IMessageBroker,
    ):
        self._report_repo = report_repo
        self._exam_repo = exam_repo
        self._patient_repo = patient_repo
        self._broker = broker

    def execute(self, input: CreateReportInput) -> CreateReportOutput:
        exam = self._exam_repo.find_by_id(UUID(input.exam_id))
        if not exam:
            raise ExamNotFound(f"Exame {input.exam_id} não encontrado")

        report = Report(
            exam_id=UUID(input.exam_id),
            doctor_id=UUID(input.doctor_id),
            content=input.content,
            conclusion=input.conclusion,
        )

        saved = self._report_repo.save(report)

        # Marca exame como concluído
        exam.complete()
        self._exam_repo.save(exam)

        # Publica dois eventos: laudo emitido + resultado disponível para paciente
        self._broker.publish("report.issued", ReportIssued(
            report_id=saved.id,
            exam_id=exam.id,
            patient_id=exam.patient_id,
            doctor_id=UUID(input.doctor_id),
        ))

        self._broker.publish("result.available", ResultAvailable(
            patient_id=exam.patient_id,
            exam_id=exam.id,
        ))

        return CreateReportOutput(
            report_id=str(saved.id),
            exam_id=str(saved.exam_id),
            doctor_id=str(saved.doctor_id),
            conclusion=saved.conclusion,
            created_at=saved.created_at.isoformat(),
        )
