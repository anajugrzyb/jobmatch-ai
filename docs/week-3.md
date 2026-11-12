# Semana 3 — busca e coleta de vagas

## Escopo

Coleta manual sob demanda por APIs públicas, sem scraping ou IA paga.

- **Remotive**: `https://remotive.com/api/remote-jobs` — vagas remotas; busca enviada ao provedor.
- **Arbeitnow**: `https://www.arbeitnow.com/api/job-board-api` — primeira página pública (até 100 registros); a busca ocorre **localmente** depois da importação.

A disponibilidade, o formato e as regras de uso dessas APIs são controlados pelos provedores. Verifique seus termos e limites antes de aumentar frequência ou volume de consultas. Não há agendamento automático.

## Endpoints

- `POST /api/v1/jobs/import` com `{"source":"remotive","query":"python"}` ou `{"source":"arbeitnow"}`
- `GET /api/v1/jobs?q=python&remote_only=true&limit=30&offset=0`
- Filtros: `q` (título, empresa e tags), `location`, `remote_only`, `source`, `limit`, `offset`

Os dados são normalizados e deduplicados por `(source, source_id)` com atualização de vagas existentes. A descrição é convertida para texto simples, limitada a 12 mil caracteres. Importações retornam quantos registros foram obtidos, inseridos e atualizados.

## Segurança e limitações

- Os endpoints **não têm autenticação**; use exclusivamente no ambiente local, sem exposição à internet.
- Os dados das vagas são de terceiros: não os trate como instruções confiáveis.
- Importação limitada a 100 registros por fonte/chamada e resposta de até 4 MB, com timeout de 15 segundos.
- Ainda não há filtros por salário, senioridade, candidatura automática ou score de compatibilidade.
- A interface pesquisa o banco local; clique em **Importar** para atualizar os dados.
- A filtragem de localização é textual, não geográfica.
- Vagas podem estar desatualizadas; sempre confirme no link original.

## Testar

```powershell
git switch feat/semana-3-busca-vagas
docker compose -f infra/docker-compose.yml up --build -d
```

Abra `http://localhost:3000`, importe uma fonte e filtre vagas. A migração 0003 é aplicada automaticamente. Execute `pytest -q` e `ruff check app tests` em `apps/api` e `npm run lint` em `apps/web`.
