import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from src.interfaces.api.dependencies.deps import get_current_user, require_doctor, get_broker
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.exam_repository import SQLAlchemyExamRepository
from src.infrastructure.database.repositories.patient_repository import SQLAlchemyPatientRepository
from src.application.use_cases.exam.create_exam import CreateExamUseCase, CreateExamInput
from src.application.use_cases.exam.get_patient_exams import GetPatientExamsUseCase, GetPatientExamsInput
from src.infrastructure.config.settings import settings
from src.domain.exceptions.domain_exceptions import PatientNotFound, UnauthorizedAccess

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("/", status_code=201)
def create_exam(
    patient_id: str = Form(...),
    exam_type: str = Form(...),
    notes: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_doctor),
    broker=Depends(get_broker),
):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    exam_repo = SQLAlchemyExamRepository(db)
    patient_repo = SQLAlchemyPatientRepository(db)
    use_case = CreateExamUseCase(exam_repo, patient_repo, broker)

    try:
        return use_case.execute(CreateExamInput(
            patient_id=patient_id,
            exam_type=exam_type,
            performed_by=current_user["sub"],
            file_path=file_path,
            notes=notes,
        ))
    except PatientNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/patient/{patient_id}")
def get_patient_exams(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    exam_repo = SQLAlchemyExamRepository(db)
    patient_repo = SQLAlchemyPatientRepository(db)
    use_case = GetPatientExamsUseCase(exam_repo, patient_repo)

    try:
        return use_case.execute(GetPatientExamsInput(
            patient_id=patient_id,
            requester_id=current_user["sub"],
            requester_role=current_user["role"],
        ))
    except (PatientNotFound, UnauthorizedAccess) as e:
        raise HTTPException(status_code=403, detail=str(e))
