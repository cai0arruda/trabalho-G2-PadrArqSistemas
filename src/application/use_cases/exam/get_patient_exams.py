from dataclasses import dataclass
from uuid import UUID
from src.application.ports.repositories import IExamRepository, IPatientRepository
from src.domain.exceptions.domain_exceptions import PatientNotFound, UnauthorizedAccess
from src.domain.entities.user import UserRole


@dataclass
class GetPatientExamsInput:
    patient_id: str
    requester_id: str
    requester_role: str


class GetPatientExamsUseCase:
    def __init__(self, exam_repo: IExamRepository, patient_repo: IPatientRepository):
        self._exam_repo = exam_repo
        self._patient_repo = patient_repo

    def execute(self, input: GetPatientExamsInput) -> list:
        patient = self._patient_repo.find_by_id(UUID(input.patient_id))
        if not patient:
            raise PatientNotFound()

        # Paciente só acessa seus próprios exames
        if input.requester_role == UserRole.PATIENT:
            if str(patient.user_id) != input.requester_id:
                raise UnauthorizedAccess("Acesso negado")

        exams = self._exam_repo.find_by_patient_id(UUID(input.patient_id))
        return [
            {
                "exam_id": str(e.id),
                "exam_type": e.exam_type,
                "status": e.status,
                "performed_at": e.performed_at.isoformat(),
                "notes": e.notes,
            }
            for e in exams
        ]
