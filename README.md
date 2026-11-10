# JobMatch AI

Agente semiautomático de candidaturas. Semana 1: FastAPI, Next.js, PostgreSQL/pgvector, Docker Compose e testes.

## Executar

```powershell
Copy-Item .env.example .env
docker compose -f infra/docker-compose.yml up --build -d
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health
- Readiness: http://localhost:8000/api/v1/ready

As credenciais em `.env.example` são exclusivas de desenvolvimento local. Nunca publique `.env`.
