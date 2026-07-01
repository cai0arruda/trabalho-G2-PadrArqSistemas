from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from src.infrastructure.database.connection import engine
from src.infrastructure.database.models.models import Base
from src.interfaces.api.routes import auth_routes, patient_routes, exam_routes, report_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria tabelas no banco ao iniciar
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MedExam Platform",
    description="Plataforma de gerenciamento de exames médicos",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(patient_routes.router, prefix="/api/v1")
app.include_router(exam_routes.router, prefix="/api/v1")
app.include_router(report_routes.router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "medexam"}
