# Semana 2 — perfil e leitura de currículo

## Funcionalidades

- `GET /api/v1/profile`: consultar perfil local (inicialmente `null`).
- `PUT /api/v1/profile`: criar ou atualizar o perfil local.
- `POST /api/v1/resume/extract`: receber PDF de até 5 MB / 20 páginas e extrair texto.
- Interface em `http://localhost:3000`: editar perfil, extrair texto e revisar antes de salvar.

O PDF **não é armazenado**; apenas seu texto é devolvido para revisão. Nenhuma informação extraída é salva automaticamente. PDF digitalizado sem camada de texto requer OCR (não implementado).

## Aviso de privacidade

Este MVP é **exclusivamente local e de usuário único**, sem login, isolamento de contas, proteção contra CSRF, limites de requisições ou auditoria. Não exponha portas, banco ou API à internet e não faça deploy público com dados pessoais. Os campos do perfil são armazenados em texto simples no PostgreSQL local. Não envie currículos sensíveis até implementar autenticação e controles de acesso.

## Testes

```bash
cd apps/api
pip install -e '.[dev]'
ruff check app tests
pytest -q
```

## Próximos passos

- Autenticação, contas individuais e autorização por recurso.
- Validação e normalização de habilidades e experiências.
- OCR opcional para PDFs digitalizados.
- Versionamento do perfil e exclusão/exportação dos dados.
