from pydantic import BaseModel
from typing import Optional


# Auth
class RegisterRequest(BaseModel):
    cpf: str
    name: str
    email: str
    password: str
    role: str = "patient"


class LoginRequest(BaseModel):
    cpf: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    role: str
    name: str


# Patient
class CreatePatientRequest(BaseModel):
    cpf: str
    name: str
    birth_date: str
    phone: str
    user_id: str


# Exam
class CreateExamRequest(BaseModel):
    patient_id: str
    exam_type: str  # ecography | ecg
    notes: Optional[str] = ""


# Report
class CreateReportRequest(BaseModel):
    exam_id: str
    content: str
    conclusion: str
