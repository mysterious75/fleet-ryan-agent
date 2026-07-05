# Fleet-Ryan — Autonomous AI Agent for Fleet Management

> Built on OpenClaw | Designed for Orbital Installation Technologies

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Agent-red.svg)](https://github.com/openclaw/openclaw)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)

---

## What Is This?

An **autonomous fleet management agent** that runs 24/7 using OpenClaw's heartbeat pattern. It monitors fleet vehicles, detects anomalies, takes safe actions, and escalates to humans when needed.

**Built for:** Ryan Scharnowske, COO — Orbital Installation Technologies, LLC

**Key Capabilities:**
- 24/7 continuous monitoring via heartbeat pattern
- Real-time vehicle tracking (location, speed, fuel, faults)
- Compliance monitoring (HOS, DVIR, IFTA)
- Predictive maintenance alerts
- Fuel anomaly detection (theft, leaks)
- Human-in-the-loop escalation with Telegram approval buttons
- Full audit trail (FMCSA compliant)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLEET-RYAN SYSTEM                           │
│                                                                  │
│  ┌──────────────────────┐      ┌────────────────────────────┐   │
│  │   OPENCLAW GATEWAY   │◄────►│     PYTHON BACKEND          │   │
│  │   (Node.js daemon)   │ API  │     FastAPI + Celery        │   │
│  │   - Heartbeat engine │      │   - 26 REST endpoints       │   │
│  │   - Agent runtime    │      │   - Webhook receiver        │   │
│  │   - Channel mgmt     │      │   - 6 background tasks      │   │
│  └──────────┬───────────┘      │   - Audit logging           │   │
│             │                  └──────────┬─────────────────┘   │
│             │                             │                      │
│  ┌──────────▼─────────────────────────────▼──────────────────┐  │
│  │              FLEET AGENT WORKSPACE                          │  │
│  │   SOUL.md | AGENTS.md | HEARTBEAT.md | MEMORY.md           │  │
│  │   4 Skills: monitor | compliance | maintenance | escalation │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   DATA LAYER                                              │   │
│  │   PostgreSQL (5 tables) | Redis (cache + queue)           │   │
│  │   Mock Data (52 vehicles, 20 drivers, 15 fault codes)     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   FLEET PLATFORMS                                         │   │
│  │   Samsara (primary) | Motive | Geotab | Fleetio           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │   HUMAN INTERFACE                                         │   │
│  │   Telegram Bot (alerts + approvals) | Web Dashboard       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/mysterious75/fleet-ryan-agent.git
cd fleet-ryan-agent

# Copy environment template
cp .env.example .env
# Edit .env with your API keys (optional — mock data works without keys)

# Start all services
docker-compose up -d

# Access the API
open http://localhost:8000/docs
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/mysterious75/fleet-ryan-agent.git
cd fleet-ryan-agent

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000

# In another terminal — start OpenClaw agent
openclaw gateway
```

### Option 3: Quick Test (No Dependencies)

```bash
cd fleet-ryan-agent/backend
pip install fastapi uvicorn pydantic pydantic-settings httpx sqlalchemy aiosqlite
uvicorn app.main:app --port 8765
# Open http://localhost:8765/docs
```

---

## API Endpoints (26 Total)

### Fleet Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/fleet/vehicles` | List all vehicles |
| `GET` | `/api/v1/fleet/vehicles/{id}` | Vehicle details |
| `GET` | `/api/v1/fleet/vehicles/{id}/stats` | Real-time stats |
| `GET` | `/api/v1/fleet/vehicles/{id}/faults` | Vehicle fault codes |
| `GET` | `/api/v1/fleet/overview` | Fleet-wide overview |
| `GET` | `/api/v1/fleet/search?q=` | Search vehicles |

### Compliance
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/compliance/hos` | Hours of Service status |
| `GET` | `/api/v1/compliance/hos/violations` | HOS violations |
| `GET` | `/api/v1/compliance/dvir` | DVIR status |
| `GET` | `/api/v1/compliance/ifta` | IFTA status |
| `GET` | `/api/v1/compliance/summary` | Compliance summary |

### Maintenance
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/maintenance/schedule` | Maintenance schedule |
| `GET` | `/api/v1/maintenance/faults` | Fleet fault codes |
| `GET` | `/api/v1/maintenance/faults/patterns` | Fault patterns |
| `GET` | `/api/v1/maintenance/costs` | Maintenance costs |
| `POST` | `/api/v1/maintenance/schedule/{id}` | Schedule maintenance |

### Escalation (HITL)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/escalation/active` | Pending escalations |
| `POST` | `/api/v1/escalation/create` | Create escalation |
| `POST` | `/api/v1/escalation/{id}/approve` | Approve escalation |
| `POST` | `/api/v1/escalation/{id}/reject` | Reject escalation |

### Webhooks
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/webhooks/samsara` | Samsara events |
| `POST` | `/api/v1/webhooks/motive` | Motive events |
| `POST` | `/api/v1/webhooks/fleetio` | Fleetio events |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health/` | Health check |
| `GET` | `/health/ready` | Readiness check |

---

## Database Schema (5 Tables)

| Table | Fields | Purpose |
|-------|--------|---------|
| `vehicles` | 23 | Fleet vehicle data (location, fuel, speed, odometer) |
| `drivers` | 16 | Driver info + HOS status |
| `fault_codes` | 11 | Diagnostic trouble codes (P-codes, C-codes) |
| `audit_log` | 13 | Full action audit trail |
| `escalations` | 19 | Human approval requests |

---

## Background Tasks (6 Celery Tasks)

| Task | Schedule | Purpose |
|------|----------|---------|
| `check_fault_codes` | Every 30 min | Poll for new diagnostic trouble codes |
| `check_compliance` | Every 1 hour | HOS violation check |
| `check_fuel_anomalies` | Every 2 hours | Fuel theft/leak detection |
| `fleet_health_snapshot` | Every 6 hours | Fleet-wide status snapshot |
| `daily_summary` | 8:00 AM daily | Daily report to Telegram |
| `memory_cleanup` | Monday 2:00 AM | Archive old memory files |

---

## Mock Data System

Works without real API keys — perfect for demo:

| Data | Count | Details |
|------|-------|---------|
| Vehicles | 52 | Makes, models, locations, fuel, speed |
| Drivers | 20 | Names, HOS status, vehicle assignments |
| Fault Codes | 15 | P0340, P0300, P0700, etc. with severity |
| Compliance | 20 drivers | DVIR, HOS, IFTA status |

When Samsara API token is set, the system automatically switches to real data.

---

## OpenClaw Agent Workspace

### Core Files
| File | Purpose |
|------|---------|
| `SOUL.md` | Agent persona — FleetCommander |
| `AGENTS.md` | Operating manual + guardrails |
| `HEARTBEAT.md` | Monitoring tasks (5 intervals) |
| `MEMORY.md` | Long-term fleet knowledge |
| `USER.md` | Client context (Ryan Scharnowske) |
| `TOOLS.md` | Fleet API tool documentation |
| `IDENTITY.md` | Agent identity card |

### Fleet Skills
| Skill | Purpose |
|-------|---------|
| `fleet-monitor` | Vehicle tracking, location, status |
| `fleet-compliance` | HOS, DVIR, IFTA monitoring |
| `fleet-maintenance` | Fault codes, PM scheduling |
| `fleet-escalation` | HITL approval workflow |

### Configuration
| File | Purpose |
|------|---------|
| `data/fleet-config.yaml` | API config, thresholds, alert channels |
| `data/escalation-rules.yaml` | 19 severity rules, 3-tier guardrails |

---

## Guardrails (3-Tier Permission System)

| Tier | Actions | Example |
|------|---------|---------|
| **Auto-Action** | Read-only queries, notifications | Check vehicle status, send alerts |
| **Require Approval** | Cost/risk operations | Schedule maintenance, modify routes |
| **Forbidden** | Never allowed | Modify ELD data, approve payments, disable safety |

---

## Telegram Bot Setup

### 1. Create Bot
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`, follow prompts
3. Save the bot token

### 2. Get Chat ID
1. Send any message to your bot
2. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find your chat ID in the response

### 3. Configure
```bash
# In .env file
TELEGRAM_BOT_TOKEN=your_bot_token_here
FLEET_MANAGER_CHAT_ID=your_chat_id_here
```

### 4. Bot Commands
```
/status    — Quick fleet status
/vehicles  — List active vehicles
/alerts    — View active alerts
/approve   — Approve pending request
/help      — Show available commands
```

---

## Project Structure

```
fleet-ryan-agent/
├── README.md                           # This file
├── .env.example                        # Environment template
├── .gitignore                          # Git ignore rules
├── docker-compose.yml                  # Docker orchestration (5 services)
├── LICENSE                             # MIT License
│
├── agent-workspace/                    # OpenClaw agent
│   ├── SOUL.md                         # Agent persona
│   ├── AGENTS.md                       # Operating manual
│   ├── HEARTBEAT.md                    # Monitoring tasks
│   ├── IDENTITY.md                     # Agent identity
│   ├── USER.md                         # User context
│   ├── TOOLS.md                        # Tool documentation
│   ├── MEMORY.md                       # Long-term memory
│   ├── memory/                         # Daily memory logs
│   │   ├── 2026-07-05.md              # Today's log
│   │   ├── README.md                   # Memory system docs
│   │   ├── weekly/                     # Weekly summaries
│   │   ├── monthly/                    # Monthly summaries
│   │   └── archive/                    # Old files
│   ├── skills/                         # Fleet skills
│   │   ├── fleet-monitor/SKILL.md
│   │   ├── fleet-compliance/SKILL.md
│   │   ├── fleet-maintenance/SKILL.md
│   │   └── fleet-escalation/SKILL.md
│   └── data/                           # Configuration
│       ├── fleet-config.yaml
│       └── escalation-rules.yaml
│
├── backend/                            # Python backend
│   ├── Dockerfile                      # Backend container
│   ├── requirements.txt                # Python dependencies
│   └── app/
│       ├── main.py                     # FastAPI entry point
│       ├── api/                        # API routes (6 files)
│       │   ├── fleet.py
│       │   ├── compliance.py
│       │   ├── maintenance.py
│       │   ├── escalation.py
│       │   ├── webhooks.py
│       │   └── health.py
│       ├── core/                       # Core modules
│       │   ├── config.py
│       │   ├── database.py
│       │   └── redis.py
│       ├── models/                     # Pydantic schemas
│       │   └── schemas.py
│       ├── services/                   # Business logic
│       │   ├── samsara.py
│       │   ├── fleetio.py
│       │   ├── telegram.py
│       │   └── mock_data.py
│       └── tasks/                      # Background jobs
│           ├── celery_app.py
│           ├── fleet_monitoring.py
│           ├── fleet_events.py
│           ├── reports.py
│           └── memory.py
│
├── scripts/                            # Automation
│   ├── setup.sh                        # One-click setup
│   ├── create_telegram_bot.sh          # Bot setup guide
│   └── memory_manager.py              # Memory management
│
└── docs/                               # Documentation
    ├── ARCHITECTURE.md                 # Technical architecture
    ├── RESEARCH.md                     # Client research
    ├── IMPROVEMENTS.md                 # Feature roadmap
    └── COMPLETE_PROJECT_GUIDE.md       # Everything in one doc
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent Runtime | OpenClaw (Node.js) | Heartbeat pattern, omnichannel |
| Backend API | FastAPI (Python 3.11+) | Async REST API, OpenAPI docs |
| Background Jobs | Celery + Redis | Task queue, retry, scheduling |
| Database | PostgreSQL | Persistent storage, JSON support |
| Cache | Redis | Caching, rate limiting, task queue |
| Fleet APIs | Samsara, Motive, Fleetio | Vehicle data, compliance |
| Messaging | Telegram | Alerts, approval buttons |
| Deployment | Docker Compose | Containerized, reproducible |
| Monitoring | Grafana Cloud + Sentry | Metrics, error tracking |

---

## Docker Services

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| PostgreSQL | fleet-ryan-db | 5432 | Database |
| Redis | fleet-ryan-redis | 6379 | Cache + queue |
| Backend API | fleet-ryan-backend | 8000 | REST API |
| Celery Worker | fleet-ryan-celery-worker | — | Background tasks |
| Celery Beat | fleet-ryan-celery-beat | — | Task scheduler |
| OpenClaw | fleet-ryan-openclaw | 18789 | Agent gateway |

---

## Cost Breakdown

### Monthly Infrastructure
| Scenario | Monthly | Yearly |
|----------|---------|--------|
| Minimum (Hetzner) | $51/mo | $612/yr |
| Standard (DigitalOcean) | $84/mo | $1,008/yr |
| Full (AWS) | $150/mo | $1,800/yr |

### Development (360 hours)
| Phase | Hours | Rate | Cost |
|-------|-------|------|------|
| MVP | 60 | $65 | $3,900 |
| Foundation | 60 | $65 | $3,900 |
| Hardening | 80 | $70 | $5,600 |
| Deployment | 80 | $70 | $5,600 |
| Scale | 80 | $65 | $5,200 |
| **Total** | **360** | **~$67** | **$24,200** |

See `docs/COMPLETE_PROJECT_GUIDE.md` for full cost breakdown.

---

## Production Roadmap

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| **Phase 1** | Now | Working demo with mock data |
| **Phase 2** | Week 1-2 | MVP with real Samsara data |
| **Phase 3** | Week 3-4 | Production foundation (auth, CI/CD) |
| **Phase 4** | Week 5-8 | Hardening (tests, security, dashboard) |
| **Phase 5** | Week 9-12 | Deployment (AWS, monitoring, SLA) |
| **Phase 6** | Week 13-16 | Scale (multi-tenant, optimization) |

See `docs/COMPLETE_PROJECT_GUIDE.md` for detailed roadmap.

---

## Testing

### Quick API Test
```bash
cd backend
pip install fastapi uvicorn pydantic pydantic-settings httpx sqlalchemy aiosqlite
uvicorn app.main:app --port 8765

# In another terminal
curl http://localhost:8765/api/v1/fleet/overview
curl http://localhost:8765/api/v1/fleet/vehicles
curl http://localhost:8765/api/v1/compliance/hos
curl http://localhost:8765/api/v1/maintenance/faults
```

### Swagger UI
Open `http://localhost:8765/docs` in browser for interactive API documentation.

---

## Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file — project overview |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical architecture deep dive |
| [RESEARCH.md](docs/RESEARCH.md) | Client research (Ryan, Orbital, fleet AI) |
| [IMPROVEMENTS.md](docs/IMPROVEMENTS.md) | Feature roadmap (20 improvements) |
| [COMPLETE_PROJECT_GUIDE.md](docs/COMPLETE_PROJECT_GUIDE.md) | Everything in one doc (costs, timeline, deployment) |

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## Built For

**Ryan Scharnowske** — COO, Orbital Installation Technologies, LLC

Orbital is a nationwide fleet technology installation company with 20+ years experience, 80+ regional hubs, and 1M+ completed installations. This agent represents their evolution from "we install the hardware" to "our AI manages your fleet."
