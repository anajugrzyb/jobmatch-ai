# JobMatch AI

Agente semiautomático para descoberta de vagas, análise de compatibilidade e currículos personalizados. **Semana 1: fundação executável**.

## Requisitos

Docker Desktop com Docker Compose v2 (Windows: WSL 2). Para desenvolvimento sem Docker: Python 3.11+, Node.js 22+ e PostgreSQL 17 com pgvector.

## Iniciar com Docker

Na raiz do projeto:

```powershell
Copy-Item .env.example .env
docker compose -f infra/docker-compose.yml up --build -d
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/api/v1/health
- API + banco: http://localhost:8000/api/v1/ready
- Swagger: http://localhost:8000/docs

O serviço API aplica as migrations com Alembic ao iniciar.

## Logs e parada

```bash
docker compose -f infra/docker-compose.yml ps
docker compose -f infra/docker-compose.yml logs -f api
docker compose -f infra/docker-compose.yml down
```

Para apagar os dados locais (irreversível): `docker compose -f infra/docker-compose.yml down -v`.

## Testes

```bash
cd apps/api
pip install -e '.[dev]'
ruff check app tests
pytest -q
cd ../web
npm install
npm run lint
npm run build
```

## Estrutura

- `apps/api`: FastAPI, modelos, migrations e testes
- `apps/web`: Next.js, TypeScript e Tailwind CSS
- `infra`: Docker Compose
- `docs`: arquitetura
- `.github/workflows`: CI

## Segurança e escopo

O `.env.example` contém apenas valores ilustrativos para uso local. **Nunca publique `.env` nem use as senhas de exemplo em produção.** As portas são vinculadas a 127.0.0.1. Não há autenticação, agentes de IA, upload de currículo ou candidaturas automáticas nesta etapa. Próxima etapa: perfil profissional e extração de currículos.
