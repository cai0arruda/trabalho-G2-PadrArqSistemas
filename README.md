# MedExam Platform

Plataforma de gerenciamento de exames médicos — Trabalho de Arquitetura de Software.

## Arquitetura

- **Estilo**: Monolito Modular
- **Arquitetura Interna**: Clean Architecture + EDA
- **Comunicação**: REST + AMQP (RabbitMQ)
- **CQRS**: Avaliado — não implementado (ver ADR-03)

```
src/
├── domain/           # Entidades, eventos, exceções — zero dependências externas
│   ├── entities/
│   ├── events/
│   └── exceptions/
├── application/      # Casos de uso + ports (interfaces/contratos)
│   ├── use_cases/
│   └── ports/
├── infrastructure/   # Adaptadores: banco, RabbitMQ, JWT
│   ├── database/
│   ├── messaging/
│   └── auth/
└── interfaces/       # Controllers FastAPI (HTTP)
    └── api/
```

## Como rodar

```bash
# Subir tudo
docker compose up --build

# API disponível em:
http://localhost:8000
http://localhost:8000/docs      # Swagger UI

# RabbitMQ Management:
http://localhost:15672          # guest/guest
```

## Fluxo de eventos (EDA)

| Evento | Fila | Disparado por |
|--------|------|---------------|
| `ExamPerformed` | `exam.performed` | Cadastro de exame |
| `ReportIssued` | `report.issued` | Emissão de laudo |
| `ResultAvailable` | `result.available` | Laudo emitido → paciente notificado |

## Endpoints principais

| Método | Rota | Acesso |
|--------|------|--------|
| POST | `/api/v1/auth/register` | Público |
| POST | `/api/v1/auth/login` | Público |
| POST | `/api/v1/patients/` | Médico |
| GET  | `/api/v1/patients/` | Médico |
| POST | `/api/v1/exams/` | Médico |
| GET  | `/api/v1/exams/patient/{id}` | Médico ou próprio paciente |
| POST | `/api/v1/reports/` | Médico |
| GET  | `/api/v1/reports/exam/{id}` | Autenticado |
| GET  | `/health` | Público |
