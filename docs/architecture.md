# Arquitetura inicial

Monólito modular: Next.js (UI) → FastAPI (REST) → PostgreSQL (pgvector).

- Backend: módulos de domínio, migrations versionadas e endpoints versionados.
- Frontend: Next.js App Router, Tailwind CSS, TypeScript.
- Desenvolvimento: Docker Compose com rede interna para API/banco.
- Segurança: portas expostas apenas em 127.0.0.1; credenciais de exemplo somente para ambiente local.
- Semana 2: autenticação, perfil profissional e upload seguro de currículo.
- Sem envio automático: a aprovação humana será obrigatória antes de qualquer candidatura.
