# JobMatch AI

Agente semiautomático para descoberta de vagas, análise de compatibilidade e currículos personalizados.

## Semana 2 — perfil profissional e leitura de PDF

A aplicação agora permite cadastrar um perfil profissional e extrair texto de um currículo em PDF para revisão manual. Consulte [a documentação da Semana 2](docs/week-2.md).

### Executar

Requisitos: Docker Desktop + Docker Compose.

```powershell
Copy-Item .env.example .env
docker compose -f infra/docker-compose.yml up --build -d
```

Se já criou o `.env` na Semana 1, não precisa recriá-lo. A migration da Semana 2 roda automaticamente ao iniciar a API.

- Interface: http://localhost:3000
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

### Estrutura

- `apps/api`: FastAPI, SQLAlchemy, Alembic e testes
- `apps/web`: Next.js, TypeScript e Tailwind
- `infra`: Docker Compose com PostgreSQL/pgvector
- `docs`: arquitetura e documentação das entregas
- `.github/workflows`: CI

### Privacidade

**Somente para execução local.** Este MVP ainda não possui autenticação, separação entre usuários ou controles de acesso adequados a uma implantação pública. Dados do perfil ficam no PostgreSQL local sem criptografia de aplicação. O PDF enviado é processado em memória e não é persistido. Não exponha a API nem o banco à internet e não use credenciais de exemplo em produção. O `.env` está no `.gitignore`.

### Próximos passos

Autenticação, perfil por usuário, parsing estruturado, OCR opcional, busca de vagas e pontuação de compatibilidade com aprovação humana.
