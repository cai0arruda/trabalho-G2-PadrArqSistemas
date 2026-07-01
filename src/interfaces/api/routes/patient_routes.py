from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.interfaces.api.schemas.schemas import CreatePatientRequest
from src.interfaces.api.dependencies.deps import get_current_user, require_doctor
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.patient_repository import SQLAlchemyPatientRepository
from src.application.use_cases.patient.create_patient import CreatePatientUseCase, CreatePatientInput
from src.domain.exceptions.domain_exceptions import DuplicateCPF

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", status_code=201, dependencies=[Depends(require_doctor)])
def create_patient(body: CreatePatientRequest, db: Session = Depends(get_db)):
    repo = SQLAlchemyPatientRepository(db)
    use_case = CreatePatientUseCase(repo)
    try:
        return use_case.execute(CreatePatientInput(**body.model_dump()))
    except DuplicateCPF as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", dependencies=[Depends(require_doctor)])
def list_patients(db: Session = Depends(get_db)):
    repo = SQLAlchemyPatientRepository(db)
    return repo.list_all()
