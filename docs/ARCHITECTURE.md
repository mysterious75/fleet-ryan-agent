# Fleet-Ryan Architecture Document

> Autonomous AI Agent for Fleet Management — Built on OpenClaw

---

## 1. System Overview

Fleet-Ryan is an autonomous fleet management agent that combines OpenClaw's always-on agent runtime with a Python backend for fleet API integration, background monitoring, and human-in-the-loop escalation.

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **OpenClaw as agent runtime** | Native heartbeat cycle, omnichannel support, claw-pattern agent design |
| **FastAPI backend** | Async Python, Pydantic validation, OpenAPI docs, production-ready |
| **Celery + Redis** | Background job scheduling, retry logic, task queue management |
| **PostgreSQL** | Persistent storage for fleet state, audit logs, escalations |
| **Telegram as primary channel** | Quick alerts, approval buttons, mobile-friendly |

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FLEET-RYAN SYSTEM                             │
│                                                                      │
│  ┌─────────────────────────┐       ┌────────────────────────────┐   │
│  │    OPENCLAW GATEWAY     │◄─────►│     PYTHON BACKEND          │   │
│  │    (Node.js daemon)     │  API  │     FastAPI + Celery        │   │
│  │                         │       │                              │   │
│  │  ┌───────────────────┐  │       │  ┌────────────────────────┐ │   │
│  │  │ Agent Runtime     │  │       │  │ REST API Endpoints     │ │   │
│  │  │ - SOUL.md         │  │       │  │ - /api/v1/fleet/*      │ │   │
│  │  │ - AGENTS.md       │  │       │  │ - /api/v1/compliance/* │ │   │
│  │  │ - HEARTBEAT.md    │  │       │  │ - /api/v1/maintenance/*│ │   │
│  │  │ - Skills          │  │       │  │ - /api/v1/escalation/* │ │   │
│  │  └───────────────────┘  │       │  │ - /api/v1/webhooks/*   │ │   │
│  │                         │       │  └────────────────────────┘ │   │
│  │  ┌───────────────────┐  │       │                              │   │
│  │  │ Heartbeat Engine  │  │       │  ┌────────────────────────┐ │   │
│  │  │ - 30-min cycle    │  │       │  │ Celery Workers         │ │   │
│  │  │ - Task scheduler  │  │       │  │ - Fault code checker   │ │   │
│  │  │ - Memory mgmt     │  │       │  │ - Compliance monitor   │ │   │
│  │  └───────────────────┘  │       │  │ - Fuel anomaly detect  │ │   │
│  │                         │       │  │ - Daily report gen     │ │   │
│  │  ┌───────────────────┐  │       │  └────────────────────────┘ │   │
│  │  │ Channel Manager   │  │       │                              │   │
│  │  │ - Telegram        │  │       │  ┌────────────────────────┐ │   │
│  │  │ - WhatsApp        │  │       │  │ Services               │ │   │
│  │  │ - Web Dashboard   │  │       │  │ - SamsaraService       │ │   │
│  │  └───────────────────┘  │       │  │ - MotiveService        │ │   │
│  └─────────────────────────┘       │  │ - FleetioService       │ │   │
│                                     │  │ - TelegramService      │ │   │
│                                     │  └────────────────────────┘ │   │
│                                     └────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐│
│  │                        DATA LAYER                                 ││
│  │                                                                    ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐││
│  │  │ PostgreSQL   │  │ Redis        │  │ Fleet Platform APIs      │││
│  │  │ - Vehicles   │  │ - Cache      │  │ - Samsara REST API       │││
│  │  │ - Drivers    │  │ - Rate limit │  │ - Motive REST API        │││
│  │  │ - Faults     │  │ - Task queue │  │ - Fleetio REST API       │││
│  │  │ - Audit log  │  │ - Sessions   │  │ - Webhooks (inbound)     │││
│  │  │ - Escalations│  │              │  │                          │││
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘││
│  └──────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐│
│  │                        HUMAN LAYER                                ││
│  │                                                                    ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐││
│  │  │ Telegram Bot │  │ Web Dashboard│  │ Email Reports            │││
│  │  │ - Alerts     │  │ - Fleet view │  │ - Daily summary          │││
│  │  │ - Approvals  │  │ - Reports    │  │ - Weekly report          │││
│  │  │ - Commands   │  │ - Settings   │  │ - Compliance reports     │││
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘││
│  └──────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow

### 3.1 Fleet Monitoring (Heartbeat Cycle)

```
Every 30 minutes:
    │
    ▼
OpenClaw Heartbeat Engine triggers
    │
    ▼
Agent reads HEARTBEAT.md tasks
    │
    ▼
Agent calls fleet-query skill
    │
    ▼
Skill calls FastAPI backend (/api/v1/fleet/*)
    │
    ▼
Backend calls Samsara API
    │
    ▼
Response processed by agent
    │
    ├── No issues → HEARTBEAT_OK
    │
    └── Issues found:
        │
        ├── Classify severity
        │
        ├── Critical → Immediate Telegram alert
        ├── High → Telegram with approval buttons
        ├── Medium → Log for daily report
        └── Low → Log only
```

### 3.2 Webhook Event Flow

```
Fleet Platform (Samsara/Motive)
    │
    ▼
Webhook POST to /api/v1/webhooks/samsara
    │
    ▼
FastAPI validates signature
    │
    ▼
Celery task enqueued
    │
    ▼
Worker processes event:
    │
    ├── Engine fault → Store in DB → Alert if critical
    ├── Geofence event → Log → Alert if configured
    ├── DVIR submission → Update status
    ├── HOS violation → Immediate alert
    └── Other → Log to audit trail
```

### 3.3 Human Escalation Flow

```
Agent detects issue requiring approval
    │
    ▼
Agent calls escalation skill
    │
    ▼
Backend creates escalation record in DB
    │
    ▼
TelegramService sends message with inline buttons:
    [✅ Approve] [❌ Reject] [⏰ Defer] [📞 Call]
    │
    ▼
Fleet manager taps button
    │
    ▼
Telegram callback → Backend updates escalation status
    │
    ▼
Agent executes approved action (or logs rejection)
    │
    ▼
Audit trail updated
```

---

## 4. Component Details

### 4.1 OpenClaw Agent

**Purpose:** Always-on autonomous agent that monitors fleet operations.

**Key Files:**
- `SOUL.md` — Agent persona (FleetCommander)
- `AGENTS.md` — Operating procedures and guardrails
- `HEARTBEAT.md` — Periodic monitoring tasks
- `MEMORY.md` — Long-term fleet knowledge
- `skills/` — Fleet-specific skill definitions

**Heartbeat Tasks:**
| Task | Interval | Purpose |
|------|----------|---------|
| Fault code check | 30 min | Detect new DTCs |
| Compliance monitor | 1 hour | HOS, DVIR status |
| Fuel anomaly | 2 hours | Theft/leak detection |
| Health snapshot | 6 hours | Fleet-wide status |
| Daily summary | 24 hours (8am) | Comprehensive report |

### 4.2 FastAPI Backend

**Purpose:** REST API for fleet data, webhook processing, and escalation management.

**Endpoints:**
| Route | Methods | Purpose |
|-------|---------|---------|
| `/api/v1/fleet/*` | GET | Vehicle queries, stats, search |
| `/api/v1/compliance/*` | GET | HOS, DVIR, IFTA status |
| `/api/v1/maintenance/*` | GET, POST | Fault codes, scheduling |
| `/api/v1/escalation/*` | GET, POST | HITL approval workflow |
| `/api/v1/webhooks/*` | POST | Fleet platform events |
| `/health/*` | GET | Health checks |

### 4.3 Celery Workers

**Purpose:** Background task processing for monitoring and reporting.

**Tasks:**
| Task | Schedule | Purpose |
|------|----------|---------|
| `check_fault_codes` | 30 min | Poll for new DTCs |
| `check_compliance` | 1 hour | HOS violation check |
| `check_fuel_anomalies` | 2 hours | Fuel theft detection |
| `fleet_health_snapshot` | 6 hours | Status snapshot |
| `daily_summary` | 8:00 AM | Daily report |
| `process_fleet_event` | On webhook | Event processing |

### 4.4 Telegram Bot

**Purpose:** Human interface for alerts, approvals, and commands.

**Features:**
- Real-time alerts with severity indicators
- Inline approval/reject buttons
- Fleet status queries
- Daily summary delivery
- Escalation management

---

## 5. Database Schema

### Core Tables

```sql
-- Vehicles
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    latitude FLOAT,
    longitude FLOAT,
    speed FLOAT,
    fuel_level FLOAT,
    odometer FLOAT,
    -- ... more fields
);

-- Fault Codes
CREATE TABLE fault_codes (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    fault_code VARCHAR(20) NOT NULL,
    severity VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    occurrence_count INTEGER DEFAULT 1,
    -- ... more fields
);

-- Audit Log
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    action_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20),
    vehicle_id VARCHAR(50),
    description TEXT,
    details JSONB,
    agent_decision VARCHAR(50),
    human_response VARCHAR(50),
    -- ... more fields
);

-- Escalations
CREATE TABLE escalations (
    id SERIAL PRIMARY KEY,
    escalation_id VARCHAR(100) UNIQUE NOT NULL,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    description TEXT,
    recommended_action TEXT,
    cost_estimate FLOAT,
    -- ... more fields
);
```

---

## 6. Security Design

### Authentication
- API key authentication for backend endpoints
- Telegram bot token for channel security
- Samsara/Motive API tokens stored in environment variables

### Authorization
- Auto-actions: Read-only queries, notifications
- Approval-required: Maintenance, routes, compliance reports
- Forbidden: ELD modification, payment approval, safety system override

### Audit Trail
- Every action logged with timestamp, reason, outcome
- Human responses tracked (who approved/rejected, when)
- Full compliance history for regulatory requirements

---

## 7. Deployment

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --port 8000

# Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# Celery Beat
celery -A app.tasks.celery_app beat --loglevel=info

# OpenClaw
openclaw gateway
```

---

## 8. Future Enhancements

### Phase 2: Multi-Platform Integration
- Motive API integration
- Geotab SDK integration
- GPS Insight webhooks

### Phase 3: Advanced Analytics
- Predictive maintenance ML models
- Route optimization algorithms
- Fuel efficiency analytics
- Driver behavior scoring

### Phase 4: Web Dashboard
- Real-time fleet map
- Interactive reports
- Configuration UI
- Multi-fleet support

### Phase 5: Enterprise Features
- Role-based access control
- Multi-tenant architecture
- SSO integration
- Compliance reporting automation
