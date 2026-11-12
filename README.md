# JobMatch AI

Agente semiautomático para descoberta de vagas, análise de compatibilidade e currículos personalizados.

## Semana 3 — busca de vagas

Importação manual de oportunidades de duas fontes públicas (Remotive e Arbeitnow), normalização, deduplicação por identificador de origem e filtros de pesquisa local.

Veja [a documentação da Semana 3](docs/week-3.md), [a Semana 2](docs/week-2.md) e [a arquitetura](docs/architecture.md).

### Executar

Requisitos: Docker Desktop + Docker Compose.

```powershell
Copy-Item .env.example .env
docker compose -f infra/docker-compose.yml up --build -d
```

Se já existe um `.env`, mantenha-o. A migration da Semana 3 roda automaticamente ao iniciar a API.

- Perfil: http://localhost:3000
- Vagas: http://localhost:3000/jobs
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health
- Readiness: http://localhost:8000/api/v1/ready

### Testes

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

### Privacidade

**Somente para execução local.** Este MVP ainda não possui autenticação, separação entre usuários ou controles de acesso adequados a uma implantação pública. Não exponha a API nem o banco à internet. Não use credenciais de exemplo em produção. O `.env` está no `.gitignore`.

A importação de vagas usa APIs externas públicas e ocorre somente quando você clica em **Importar vagas**. Não há scraping ou candidaturas automáticas.

### Próximos passos

Autenticação, parsing estruturado do currículo, compatibilidade entre perfil e vagas, revisão humana e acompanhamento das candidaturas.
