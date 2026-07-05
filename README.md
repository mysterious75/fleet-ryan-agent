# Fleet-Ryan — Autonomous AI Agent for Fleet Management

> Built on OpenClaw | Designed for Orbital Installation Technologies

---

## What Is This?

An **autonomous fleet management agent** that runs 24/7 using OpenClaw's heartbeat pattern. It monitors fleet operations, detects anomalies, takes safe actions, and escalates to humans when needed.

**Built for:** Ryan Scharnowske, COO — Orbital Installation Technologies, LLC

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FLEET-RYAN SYSTEM                         │
│                                                              │
│  ┌──────────────────────┐    ┌──────────────────────────┐   │
│  │   OPENCLAW GATEWAY   │◄──►│   PYTHON BACKEND          │   │
│  │   (Node.js daemon)   │    │   FastAPI + Celery        │   │
│  │   - Heartbeat engine │    │   - REST API endpoints    │   │
│  │   - Agent runtime    │    │   - Webhook receiver      │   │
│  │   - Channel mgmt     │    │   - Background jobs       │   │
│  └──────────┬───────────┘    │   - Audit logging         │   │
│             │                └──────────┬───────────────┘   │
│             │                           │                    │
│  ┌──────────▼───────────────────────────▼──────────────┐    │
│  │              FLEET AGENT WORKSPACE                    │    │
│  │   SOUL.md | AGENTS.md | HEARTBEAT.md | MEMORY.md     │    │
│  │   skills/fleet-monitor | fleet-compliance | etc.      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              CHANNELS                                  │    │
│  │   Telegram Bot  |  WhatsApp  |  Web Dashboard         │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              FLEET PLATFORM APIs                       │    │
│  │   Samsara  |  Motive  |  Geotab  |  Fleetio           │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/fleet-ryan-agent.git
cd fleet-ryan-agent
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start with Docker
```bash
docker-compose up -d
```

### 3. Or start manually
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# OpenClaw agent (separate terminal)
openclaw gateway
```

---

## Project Structure

```
fleet-ryan-agent/
├── agent-workspace/          # OpenClaw agent workspace
│   ├── SOUL.md               # Agent persona
│   ├── AGENTS.md             # Operating instructions
│   ├── HEARTBEAT.md          # Monitoring tasks
│   ├── MEMORY.md             # Long-term memory
│   ├── TOOLS.md              # Tool usage guide
│   ├── IDENTITY.md           # Agent identity
│   ├── USER.md               # User context
│   ├── skills/               # Fleet-specific skills
│   │   ├── fleet-monitor/SKILL.md
│   │   ├── fleet-compliance/SKILL.md
│   │   ├── fleet-maintenance/SKILL.md
│   │   └── fleet-escalation/SKILL.md
│   └── data/                 # Fleet config & rules
│       ├── fleet-config.yaml
│       └── escalation-rules.yaml
├── backend/                  # Python FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI app entry
│   │   ├── api/              # API routes
│   │   ├── core/             # Config, security
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   ├── tasks/            # Celery background tasks
│   │   └── utils/            # Helpers
│   ├── tests/
│   └── requirements.txt
├── docker/                   # Docker configs
├── mcp-servers/              # Fleet platform MCP servers
│   ├── samsara/
│   ├── motive/
│   └── fleetio/
├── scripts/                  # Setup & utility scripts
├── docs/                     # Documentation
└── docker-compose.yml
```

---

## Features

### Phase 1: Core Agent (MVP) ✅
- [x] OpenClaw agent with fleet persona
- [x] Heartbeat monitoring (compliance, faults, fuel)
- [x] Telegram channel for human interaction
- [x] Basic fleet queries

### Phase 2: Fleet API Integration
- [ ] Samsara API integration
- [ ] Vehicle locations, fault codes, HOS status
- [ ] Webhook receiver for real-time events
- [ ] Human escalation workflow

### Phase 3: Intelligent Monitoring
- [ ] Condition-based maintenance alerts
- [ ] Compliance monitoring (HOS, DVIR, IFTA)
- [ ] Fuel anomaly detection
- [ ] Severity-based escalation rules

### Phase 4: Autonomous Actions
- [ ] Auto-schedule maintenance
- [ ] Auto-generate compliance reports
- [ ] Route optimization suggestions
- [ ] Multi-system orchestration

### Phase 5: Production Hardening
- [ ] Full audit trail
- [ ] Role-based permissions
- [ ] Web dashboard
- [ ] Multi-fleet support

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Runtime | OpenClaw (Node.js) |
| Backend API | FastAPI + Python |
| Queue System | Celery + Redis |
| Database | PostgreSQL |
| Fleet APIs | Samsara, Motive, Geotab, Fleetio |
| Deployment | Docker Compose |
| Human Interface | Telegram + Web Dashboard |

---

## License

Private — Orbital Installation Technologies, LLC
