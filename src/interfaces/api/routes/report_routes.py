from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.interfaces.api.schemas.schemas import CreateReportRequest
from src.interfaces.api.dependencies.deps import require_doctor, get_broker, get_current_user
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.report_repository import SQLAlchemyReportRepository
from src.infrastructure.database.repositories.exam_repository import SQLAlchemyExamRepository
from src.infrastructure.database.repositories.patient_repository import SQLAlchemyPatientRepository
from src.application.use_cases.report.create_report import CreateReportUseCase, CreateReportInput
from src.domain.exceptions.domain_exceptions import ExamNotFound

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", status_code=201)
def create_report(
    body: CreateReportRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_doctor),
    broker=Depends(get_broker),
):
    report_repo = SQLAlchemyReportRepository(db)
    exam_repo = SQLAlchemyExamRepository(db)
    patient_repo = SQLAlchemyPatientRepository(db)
    use_case = CreateReportUseCase(report_repo, exam_repo, patient_repo, broker)

    try:
        return use_case.execute(CreateReportInput(
            exam_id=body.exam_id,
            doctor_id=current_user["sub"],
            content=body.content,
            conclusion=body.conclusion,
        ))
    except ExamNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/exam/{exam_id}", dependencies=[Depends(get_current_user)])
def get_report_by_exam(exam_id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyReportRepository(db)
    from uuid import UUID
    report = repo.find_by_exam_id(UUID(exam_id))
    if not report:
        raise HTTPException(status_code=404, detail="Laudo não encontrado")
    return report
