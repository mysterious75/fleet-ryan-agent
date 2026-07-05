# TOOLS.md — FleetCommander Tool Notes

## Fleet APIs

### Samsara API (Primary)
- Base URL: https://api.samsara.com
- Auth: Bearer token (stored in .env)
- Key endpoints:
  - `/v1/fleet/vehicles` — Vehicle list & status
  - `/v1/fleet/vehicles/stats` — Real-time vehicle stats
  - `/v1/fleet/drivers` — Driver list
  - `/v1/fleet/maintenance` — Maintenance data
  - `/v1/fleet/dispatching` — Dispatch & routing
- Rate limit: 5 requests/second (300/minute)
- Webhooks available for real-time events

### Motive API (Secondary)
- Base URL: https://api.gomotive.com/v1
- Auth: API key (stored in .env)
- Key endpoints:
  - `/vehicles` — Vehicle list
  - `/drivers` — Driver list
  - `/hos_logs` — Hours of Service
  - `/dvir_reports` — Driver Vehicle Inspection Reports
  - `/dispatch` — Dispatch operations

### Fleetio API (Maintenance)
- Base URL: https://secure.fleetio.com/api/v1
- Auth: API token + Account token
- Key endpoints:
  - `/vehicles` — Vehicle list
  - `/work_orders` — Work orders
  - `/service_entries` — Service history
  - `/fuel_entries` — Fuel transactions

## Communication

### Telegram Bot
- Bot token: stored in TELEGRAM_BOT_TOKEN env var
- Fleet manager chat ID: stored in FLEET_MANAGER_CHAT_ID env var
- Use for: alerts, approval requests, daily summaries
- Alert format: emoji + severity + vehicle ID + issue + action

### Email (Daily Reports)
- Use for: detailed daily/weekly reports
- Send via: SMTP or email API
- Recipients: [Client Email]

## Data Storage

### PostgreSQL
- Connection: stored in DATABASE_URL env var
- Tables: vehicles, drivers, fault_codes, fuel_transactions, audit_log, escalations

### Redis
- Connection: stored in REDIS_URL env var
- Use for: Celery task queue, caching fleet data, rate limiting

## Local Notes
- Fleet config: agent-workspace/data/fleet-config.yaml
- Escalation rules: agent-workspace/data/escalation-rules.yaml
- Memory files: agent-workspace/memory/
- Audit logs: PostgreSQL audit_log table + memory files
