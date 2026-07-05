# Fleet-[Client] — Complete Project Guide

> EVERYTHING you need to know — Architecture, Costs, Timeline, Requirements, Deployment

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Architecture Deep Dive](#2-architecture-deep-dive)
3. [What We Built](#3-what-we-built)
4. [Production Roadmap](#4-production-roadmap)
5. [Technical Requirements](#5-technical-requirements)
6. [Risk Assessment](#6-risk-assessment)
7. [Pricing Strategy](#7-pricing-strategy)
8. [Deployment Checklist](#8-deployment-checklist)
9. [Maintenance Plan](#9-maintenance-plan)

---

## 1. PROJECT OVERVIEW

### What Is This?

An **autonomous AI fleet management agent** that:
- Runs 24/7 using OpenClaw's heartbeat pattern
- Monitors fleet vehicles (location, fuel, faults, compliance)
- Detects anomalies (fuel theft, HOS violations, engine faults)
- Takes safe actions (notifications, reports)
- Escalates to humans for expensive/risky decisions
- Logs everything with full audit trail

### Who Is It For?

[Client Name], COO of Fleet Installation Company
- 20+ year old fleet hardware installation company
- 80+ regional hubs, 1M+ installs completed
- Wants to evolve from "we install hardware" to "our AI manages your fleet"

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Agent Runtime | OpenClaw (Node.js) | Heartbeat pattern, omnichannel, claw-pattern |
| Backend API | FastAPI (Python) | Async, Pydantic, OpenAPI docs |
| Background Jobs | Celery + Redis | Task queue, retry, scheduling |
| Database | PostgreSQL | Persistent storage, JSON support |
| Fleet API | Samsara (primary) | REST API, webhooks, market leader |
| Messaging | Telegram | Alerts, approval buttons, mobile-friendly |
| Deployment | Docker Compose | Containerized, reproducible |

---

## 2. ARCHITECTURE DEEP DIVE

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FLEET-RYAN SYSTEM                             │
│                                                                      │
│  ┌─────────────────────────┐       ┌────────────────────────────┐   │
│  │    OPENCLAW GATEWAY     │◄─────►│     PYTHON BACKEND          │   │
│  │    (Node.js daemon)     │  API  │     FastAPI + Celery        │   │
│  │                         │       │                              │   │
│  │  ┌───────────────────┐  │       │  ┌────────────────────────┐ │   │
│  │  │ Agent Runtime     │  │       │  │ REST API (26 endpoints)│ │   │
│  │  │ - SOUL.md         │  │       │  │ - /api/v1/fleet/*      │ │   │
│  │  │ - AGENTS.md       │  │       │  │ - /api/v1/compliance/* │ │   │
│  │  │ - HEARTBEAT.md    │  │       │  │ - /api/v1/maintenance/*│ │   │
│  │  │ - 4 Skills        │  │       │  │ - /api/v1/escalation/* │ │   │
│  │  └───────────────────┘  │       │  │ - /api/v1/webhooks/*   │ │   │
│  │                         │       │  └────────────────────────┘ │   │
│  │  ┌───────────────────┐  │       │                              │   │
│  │  │ Heartbeat Engine  │  │       │  ┌────────────────────────┐ │   │
│  │  │ - 30 min cycle    │  │       │  │ Celery Workers         │ │   │
│  │  │ - 5 task types    │  │       │  │ - Fault checker (30m)  │ │   │
│  │  │ - Memory mgmt     │  │       │  │ - Compliance (1hr)     │ │   │
│  │  └───────────────────┘  │       │  │ - Fuel anomaly (2hr)   │ │   │
│  │                         │       │  │ - Health snapshot (6hr) │ │   │
│  │  ┌───────────────────┐  │       │  │ - Daily summary (24hr) │ │   │
│  │  │ Channel Manager   │  │       │  │ - Memory cleanup (wk)  │ │   │
│  │  │ - Telegram        │  │       │  └────────────────────────┘ │   │
│  │  │ - WhatsApp        │  │       │                              │   │
│  │  └───────────────────┘  │       │  ┌────────────────────────┐ │   │
│  └─────────────────────────┘       │  │ Services               │ │   │
│                                     │  │ - Samsara API client   │ │   │
│                                     │  │ - Fleetio API client   │ │   │
│                                     │  │ - Telegram bot service │ │   │
│                                     │  │ - Mock data (demo)     │ │   │
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
│  │  │ - Alerts     │  │ - Fleet map  │  │ - Daily summary          │││
│  │  │ - Approvals  │  │ - Reports    │  │ - Weekly report          │││
│  │  │ - Commands   │  │ - Settings   │  │ - Compliance reports     │││
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘││
│  └──────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Fleet Platform (Samsara)                    Telegram (Ryan)
       │                                          ▲
       ▼                                          │
  Webhook POST ──► FastAPI ──► Celery Worker ──► Alert/Escalation
       │                │           │
       ▼                ▼           ▼
  Signature Check   Store in DB   Classify Severity
       │                │           │
       ▼                ▼           ▼
  Accept/Reject     Audit Log    Auto-Act or HITL
```

### Agent Workspace Structure

```
agent-workspace/
├── SOUL.md              # Agent persona (FleetCommander)
├── AGENTS.md            # Operating manual (guardrails, workflows)
├── HEARTBEAT.md         # Monitoring tasks (5 intervals)
├── IDENTITY.md          # Agent identity card
├── USER.md              # [Client]'s profile & preferences
├── TOOLS.md             # Fleet API tool documentation
├── MEMORY.md            # Long-term fleet knowledge
├── memory/              # Daily memory logs
│   ├── 2026-07-05.md   # Today's log
│   ├── weekly/          # Weekly summaries
│   ├── monthly/         # Monthly summaries
│   └── archive/         # Old files
├── skills/              # Fleet-specific skills
│   ├── fleet-monitor/   # Vehicle tracking
│   ├── fleet-compliance/# HOS, DVIR, IFTA
│   ├── fleet-maintenance/# Fault codes, PM scheduling
│   └── fleet-escalation/# HITL approval workflow
└── data/                # Configuration
    ├── fleet-config.yaml    # API config, thresholds
    └── escalation-rules.yaml# Severity rules, guardrails
```

---

## 3. WHAT WE BUILT

### File Inventory (48 source files)

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| **Agent Workspace** | 12 | ~1,500 | OpenClaw agent config |
| **Python Backend** | 15 | ~2,000 | FastAPI + Celery |
| **Docker** | 3 | ~200 | Deployment |
| **Scripts** | 2 | ~200 | Setup automation |
| **Documentation** | 5 | ~2,500 | Architecture, FAQ, roadmap |
| **Config** | 4 | ~300 | Environment, gitignore |
| **Total** | **48** | **~6,200** | **Complete system** |

### API Endpoints (26 total)

```
GET  /                                    → Root info
GET  /health/                             → Health check
GET  /health/ready                        → Readiness check
GET  /api/v1/fleet/vehicles               → List all vehicles
GET  /api/v1/fleet/vehicles/{id}          → Vehicle details
GET  /api/v1/fleet/vehicles/{id}/stats    → Real-time stats
GET  /api/v1/fleet/vehicles/{id}/faults   → Vehicle fault codes
GET  /api/v1/fleet/overview               → Fleet-wide overview
GET  /api/v1/fleet/search?q=              → Search vehicles
GET  /api/v1/compliance/hos               → HOS status
GET  /api/v1/compliance/hos/violations    → HOS violations
GET  /api/v1/compliance/dvir              → DVIR status
GET  /api/v1/compliance/ifta              → IFTA status
GET  /api/v1/compliance/summary           → Compliance summary
GET  /api/v1/maintenance/schedule         → Maintenance schedule
GET  /api/v1/maintenance/faults           → Fleet fault codes
GET  /api/v1/maintenance/faults/patterns  → Fault patterns
GET  /api/v1/maintenance/costs            → Maintenance costs
POST /api/v1/maintenance/schedule/{id}    → Schedule maintenance
GET  /api/v1/escalation/active            → Pending escalations
POST /api/v1/escalation/create            → Create escalation
POST /api/v1/escalation/{id}/approve      → Approve escalation
POST /api/v1/escalation/{id}/reject       → Reject escalation
POST /api/v1/webhooks/samsara             → Samsara webhook
POST /api/v1/webhooks/motive              → Motive webhook
POST /api/v1/webhooks/fleetio             → Fleetio webhook
```

### Database Tables (6 tables, 94 fields)

| Table | Fields | Purpose |
|-------|--------|---------|
| `vehicles` | 23 | Fleet vehicle data |
| `drivers` | 16 | Driver info + HOS status |
| `fault_codes` | 11 | Diagnostic trouble codes |
| `fuel_transactions` | 12 | Fuel purchase tracking & anomaly detection |
| `audit_log` | 13 | Full action audit trail |
| `escalations` | 19 | Human approval requests |

### Background Tasks (6 Celery tasks)

| Task | Schedule | Purpose |
|------|----------|---------|
| `check_fault_codes` | Every 30 min | Poll for new DTCs |
| `check_compliance` | Every 1 hour | HOS violation check |
| `check_fuel_anomalies` | Every 2 hours | Fuel theft detection |
| `fleet_health_snapshot` | Every 6 hours | Status snapshot |
| `daily_summary` | 8:00 AM daily | Daily report |
| `memory_cleanup` | Monday 2:00 AM | Archive old files |

### Mock Data (Demo-Ready)

| Data | Count | Realistic? |
|------|-------|-----------|
| Vehicles | 52 | ✅ Makes, models, locations |
| Drivers | 20 | ✅ Names, HOS status |
| Fault Codes | 15 | ✅ P0340, P0300, etc. |
| Compliance | 20 drivers | ✅ DVIR, HOS, IFTA |

---

## 4. PRODUCTION ROADMAP

### Phase 1: Working Demo (NOW — 1-2 days)

- [x] OpenClaw agent with FleetCommander persona
- [x] FastAPI backend (26 endpoints)
- [x] Mock data system (52 vehicles, 20 drivers)
- [x] Telegram bot integration
- [x] Database models (5 tables)
- [x] Celery background tasks
- [x] HITL escalation workflow
- [x] Audit trail
- [x] Architecture documentation
- [x] Research documentation

**Status:** ✅ READY FOR DEMO

### Phase 2: MVP (Week 1-2)

- [ ] Telegram bot commands (/status, /vehicles, /approve)
- [ ] Real Samsara API integration (needs API key)
- [ ] Basic automated tests (pytest)
- [ ] Error handling improvements
- [ ] Logging improvements (structured logs)
- [ ] [Client] demo preparation

### Phase 3: Production Foundation (Week 3-4)

- [ ] Authentication (API keys, JWT tokens)
- [ ] Rate limiting (per-client)
- [ ] Database migrations (Alembic)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Docker production build
- [ ] Logging aggregation
- [ ] Basic monitoring (health checks)

### Phase 4: Hardening (Week 5-8)

- [ ] Automated test suite (80%+ coverage)
- [ ] Load testing (100+ concurrent requests)
- [ ] Security audit (OWASP top 10)
- [ ] Backup/restore procedures
- [ ] Failover handling
- [ ] Multi-fleet support
- [ ] Web dashboard (basic)

### Phase 5: Deployment (Week 9-12)

- [ ] AWS/DigitalOcean deployment
- [ ] SSL/TLS setup
- [ ] Domain + DNS
- [ ] Monitoring stack (Prometheus + Grafana)
- [ ] Alerting (PagerDuty/OpsGenie)
- [ ] On-call rotation setup
- [ ] SLA definition
- [ ] Client onboarding flow

### Phase 6: Scale & Optimize (Week 13-16)

- [ ] Performance optimization
- [ ] Database indexing
- [ ] Caching layer (Redis)
- [ ] CDN for dashboard
- [ ] Multi-region support
- [ ] Advanced analytics
- [ ] API rate limiting per tenant

### Timeline Summary

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| Phase 2 | Week 1-2 | MVP with real data |
| Phase 3 | Week 3-4 | Production foundation |
| Phase 4 | Week 5-8 | Hardening + testing |
| Phase 5 | Week 9-12 | Deployment + monitoring |
| Phase 6 | Week 13-16 | Scale + optimize |
| **Total** | **16 weeks** | **Full production system** |

---

## 5. TECHNICAL REQUIREMENTS

### Server Requirements

| Resource | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| **CPU** | 2 vCPU | 4 vCPU | OpenClaw + FastAPI + Celery |
| **RAM** | 4GB | 8GB | Node.js + Python + PostgreSQL |
| **Storage** | 50GB SSD | 160GB NVMe | Database + logs + backups |
| **Network** | 100 Mbps | 1 Gbps | Webhook traffic |
| **OS** | Ubuntu 22.04 | Ubuntu 24.04 | LTS recommended |

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| **Node.js** | 22+ (recommended 24) | OpenClaw runtime |
| **Python** | 3.11+ | FastAPI backend |
| **PostgreSQL** | 15+ | Database |
| **Redis** | 7+ | Cache + task queue |
| **Docker** | 24+ | Containerization |
| **Docker Compose** | 2.20+ | Multi-container orchestration |

### Fleet API Requirements

| API | Auth Method | Rate Limits | Notes |
|-----|-------------|-------------|-------|
| **Samsara** | Bearer token | 5 req/sec (300/min) | Primary platform |
| **Motive** | API key | Varies | Secondary platform |
| **Fleetio** | Token + Account | 100 req/min | Maintenance focus |
| **Google Maps** | API key | 50 req/sec | Geocoding |

### Telegram Requirements

| Requirement | Details |
|-------------|---------|
| **Bot Token** | Get from @BotFather on Telegram |
| **Chat ID** | [Client]'s Telegram user ID |
| **Privacy Mode** | Disable for group chats |
| **Commands** | /status, /vehicles, /approve, /help |

---

## 6. RISK ASSESSMENT

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **[Client] picks another freelancer** | Medium | High | Apply ASAP, show working prototype |
| **Samsara API changes** | Low | High | Abstract API layer, use versioning |
| **Server downtime** | Low | Medium | Health checks, auto-restart, backups |
| **Security breach** | Low | Critical | Security audit, guardrails, encryption |
| **Cost overrun** | Medium | Medium | Fixed-price phases, clear scope |
| **Scope creep** | High | Medium | Phase-based delivery, change orders |
| **Dependency breaking** | Low | Medium | Pin versions, test before updates |
| **Data loss** | Low | Critical | Daily backups, tested restore |
| **Performance issues** | Medium | Medium | Load testing, caching, indexing |
| **Compliance failure** | Low | High | Legal review, FMCSA research |

---

## 7. PRICING STRATEGY

### For [Client] (Client)

| Phase | Deliverable | Hours | Rate | Cost |
|-------|-------------|-------|------|------|
| **Phase 1** | Working demo | 0 | $0 | $0 (already done) |
| **Phase 2** | MVP with real data | Week 1-2 |
| **Phase 3** | Production foundation | Week 3-4 |
| **Phase 4** | Hardening + testing | Week 5-8 |
| **Phase 5** | Deployment + monitoring | Week 9-12 |
| **Phase 6** | Scale + optimize | Week 13-16 |
| **Total** | Full production system | 16 weeks |

### Monthly Recurring (After Launch)

| Service | Cost | Who Pays |
|---------|------|----------|
| Server hosting | [Client] |
| Fleet API (Samsara) | $0 (API) | [Client] (hardware subscription) |
| Monitoring tools | $0-10 | You (included) |
| Support & maintenance | $500-1000/mo | [Client] (optional retainer) |

### Retainer Option

| Tier | Hours/month | Rate | Monthly | Includes |
|------|-------------|------|---------|----------|
| **Basic** | 5 hrs | $75 | $375 | Bug fixes, minor updates |
| **Standard** | 10 hrs | $70 | $700 | Bug fixes, monitoring, minor features |
| **Premium** | 20 hrs | $65 | $1,300 | Full support, new features, on-call |

---

## 8. DEPLOYMENT CHECKLIST

### Pre-Deployment

- [ ] Get Samsara API token from Ryan
- [ ] Create Telegram bot via @BotFather
- [ ] Get [Client]'s Telegram chat ID
- [ ] Choose hosting provider (Hetzner recommended)
- [ ] Register domain name
- [ ] Set up GitHub repository (private)

### Server Setup

- [ ] Provision VPS (4 vCPU, 8GB RAM)
- [ ] Install Docker + Docker Compose
- [ ] Configure firewall (ports 80, 443, 18789)
- [ ] Set up SSH key authentication
- [ ] Install fail2ban
- [ ] Configure automatic security updates

### Application Deployment

- [ ] Clone repository to server
- [ ] Configure .env file with real API keys
- [ ] Run database migrations
- [ ] Start Docker Compose services
- [ ] Verify all services are running
- [ ] Test API endpoints
- [ ] Test Telegram bot

### SSL & Domain

- [ ] Point domain to server IP
- [ ] Install Certbot for Let's Encrypt
- [ ] Generate SSL certificate
- [ ] Configure Nginx reverse proxy
- [ ] Test HTTPS access

### Monitoring

- [ ] Set up UptimeRobot (free)
- [ ] Set up Sentry (free tier)
- [ ] Set up Grafana Cloud (free tier)
- [ ] Configure alert channels (email, Telegram)
- [ ] Test alert delivery

### Backup

- [ ] Configure daily database backups
- [ ] Set up backup storage (Hetzner Storage Box)
- [ ] Test restore procedure
- [ ] Document restore steps

### Security

- [ ] Change all default passwords
- [ ] Rotate API keys
- [ ] Enable 2FA on all accounts
- [ ] Review firewall rules
- [ ] Run security scan

---

## 9. MAINTENANCE PLAN

### Daily (Automated)

- Database backup
- Health check monitoring
- Error tracking review
- Log rotation

### Weekly (Manual)

- Review error reports
- Check disk usage
- Review security alerts
- Update dependencies (if needed)

### Monthly (Manual)

- Security patch review
- Performance review
- Cost review
- Client check-in

### Quarterly (Manual)

- Security audit
- Disaster recovery test
- Dependency major updates
- Client satisfaction review

---

## APPENDIX A: TECHNOLOGY DECISIONS

| Decision | Options | Chosen | Why |
|----------|---------|--------|-----|
| Agent runtime | OpenClaw, Hermes, Custom | OpenClaw | [Client] specifically asked for it |
| Backend | FastAPI, Django, Flask | FastAPI | Async, Pydantic, OpenAPI |
| Database | PostgreSQL, MySQL, MongoDB | PostgreSQL | JSON support, audit trails |
| Cache/Queue | Redis, RabbitMQ, SQS | Redis | Simple, fast, Celery native |
| Fleet API | Samsara, Motive, Geotab | Samsara | Market leader, best API |
| Messaging | Telegram, WhatsApp, Slack | Telegram | Free, inline buttons |
| Deployment | Docker, K8s, Serverless | Docker Compose | Simple, reproducible |
| Monitoring | Prometheus, Datadog, Grafana | Grafana Cloud | Free tier, powerful |
| Error tracking | Sentry, Bugsnag, Rollbar | Sentry | Free tier, great DX |
| CI/CD | GitHub Actions, GitLab CI | GitHub Actions | Free, integrated |

## APPENDIX B: FILE STRUCTURE

```
fleet-ryan-agent/
├── README.md                           # Project overview
├── .env.example                        # Environment template
├── .gitignore                          # Git ignore rules
├── docker-compose.yml                  # Docker orchestration
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
│   │   ├── fleet-monitor/SKILL.md      # Vehicle tracking
│   │   ├── fleet-compliance/SKILL.md   # HOS, DVIR, IFTA
│   │   ├── fleet-maintenance/SKILL.md  # Fault codes, PM
│   │   └── fleet-escalation/SKILL.md   # HITL workflow
│   └── data/                           # Configuration
│       ├── fleet-config.yaml           # Fleet API config
│       └── escalation-rules.yaml       # Severity rules
│
├── backend/                            # Python backend
│   ├── Dockerfile                      # Backend container
│   ├── requirements.txt                # Python dependencies
│   └── app/
│       ├── main.py                     # FastAPI entry
│       ├── api/                        # API routes
│       │   ├── fleet.py                # Vehicle endpoints
│       │   ├── compliance.py           # Compliance endpoints
│       │   ├── maintenance.py          # Maintenance endpoints
│       │   ├── escalation.py           # HITL endpoints
│       │   ├── webhooks.py             # Webhook receivers
│       │   └── health.py               # Health checks
│       ├── core/                       # Core modules
│       │   ├── config.py               # Settings
│       │   ├── database.py             # SQLAlchemy models
│       │   └── redis.py                # Redis client
│       ├── models/                     # Pydantic schemas
│       │   └── schemas.py              # API schemas
│       ├── services/                   # Business logic
│       │   ├── samsara.py              # Samsara API client
│       │   ├── fleetio.py              # Fleetio API client
│       │   ├── telegram.py             # Telegram bot
│       │   └── mock_data.py            # Demo data
│       └── tasks/                      # Background jobs
│           ├── celery_app.py           # Celery config
│           ├── fleet_monitoring.py     # Monitoring tasks
│           ├── fleet_events.py         # Event processing
│           ├── reports.py              # Report generation
│           └── memory.py               # Memory cleanup
│
├── scripts/                            # Automation
│   ├── setup.sh                        # One-click setup
│   ├── create_telegram_bot.sh          # Bot setup guide
│   └── memory_manager.py               # Memory management
│
└── docs/                               # Documentation
    ├── ARCHITECTURE.md                 # Technical architecture
    ├── IMPROVEMENTS.md                 # Feature roadmap
    ├── FAQ_ANSWERS.md                  # Frequently asked questions
    └── COMPLETE_PROJECT_GUIDE.md       # This file
```
