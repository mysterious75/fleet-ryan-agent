# Fleet-[Client] — Frequently Asked Questions (FAQ)

> Every question answered — AI, Security, Samsara, Databases, Real-time Tracking, Dashcam, and more

---

## TABLE OF CONTENTS

1. [AI & Models](#1-ai--models)
2. [Security & Sandboxing](#2-security--sandboxing)
3. [Samsara Free Data](#3-samsara-free-data)
4. [[Client]'s Setup](#4-ryans-setup)
5. [App vs Website](#5-app-vs-website)
6. [Real-time Tracking](#6-real-time-tracking)
7. [Call & Communication](#7-call--communication)
8. [Dashcam Integration](#8-dashcam-integration)
9. [Database Architecture](#9-database-architecture)
10. [AI Learning](#10-ai-learning)
11. [Technical Glossary](#11-technical-glossary)

---

## 1. AI & Models

### Q: Where is the AI? What model will be used?

**Short Answer:** The OpenClaw agent's "brain" is an LLM (Large Language Model). Without an LLM, the agent is just a script — it cannot make intelligent decisions.

**Detailed Answer:**

OpenClaw is an **agent framework** — it is not AI itself. It is a "container" that gives an AI model the task of fleet management. Think of it as the AI model's "desk" where it works.

### LLM Options (What to use):

| Model | Provider | Cost | Quality | Speed | Best For |
|-------|----------|------|---------|-------|----------|
| **GPT-4o** | OpenAI | $5-15/1M tokens | ⭐⭐⭐⭐⭐ | Fast | Best quality, production-ready |
| **GPT-4o-mini** | OpenAI | $0.15-0.60/1M tokens | ⭐⭐⭐⭐ | Very Fast | Budget-friendly, good quality |
| **Claude 3.5 Sonnet** | Anthropic | $3-15/1M tokens | ⭐⭐⭐⭐⭐ | Fast | Best reasoning, safety-focused |
| **Claude 3 Haiku** | Anthropic | $0.25-1.25/1M tokens | ⭐⭐⭐ | Very Fast | Budget, fast responses |
| **Gemini Pro** | Google | $1.25-5/1M tokens | ⭐⭐⭐⭐ | Fast | Good balance |
| **Llama 3.1 70B** | Meta (self-hosted) | $0 (hardware cost) | ⭐⭐⭐⭐ | Medium | Free, needs GPU |
| **Mistral 7B** | Mistral (self-hosted) | $0 (hardware cost) | ⭐⭐⭐ | Fast | Free, runs on CPU |
| **Ollama** | Local | $0 | ⭐⭐⭐ | Medium | Free, runs locally |

### Recommended Setup for [Client]:

**Option A: OpenAI GPT-4o-mini (Best for start)**
- Cost: ~$10-30/month for fleet monitoring
- Quality: Very good for fleet queries
- Setup: Just add API key to .env

**Option B: Anthropic Claude 3.5 Sonnet (Best quality)**
- Cost: ~$20-50/month
- Quality: Excellent reasoning, safety-focused
- Setup: Just add API key to .env

**Option C: Ollama + Llama 3.1 (Free, local)**
- Cost: $0 (needs decent server with 16GB+ RAM)
- Quality: Good enough for fleet queries
- Setup: Install Ollama, pull model, configure OpenClaw

### How to Configure:

```bash
# Option A: OpenAI
# In .env file:
OPENAI_API_KEY=sk-…your_key_here
OPENAI_MODEL=gpt-4o-mini

# Option B: Anthropic
ANTHROPIC_API_KEY=sk-ant-…your_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Option C: Ollama (local)
# Install Ollama first:
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:70b
# In .env:
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:70b
```

### API Key Costs (Monthly Estimate):

| Usage Level | Queries/Day | GPT-4o-mini | Claude Haiku | Ollama |
|-------------|-------------|-------------|--------------|--------|
| Light (testing) | 50 | ~$2/mo | ~$3/mo | $0 |
| Normal (single fleet) | 200 | ~$10/mo | ~$15/mo | $0 |
| Heavy (multi-fleet) | 1000+ | ~$50/mo | ~$75/mo | $0 |

---

## 2. Security & Sandboxing

### Q: Is there a security risk in OpenClaw? Should it run in a sandbox or Kali?

**Short Answer:** Yes, there is a security risk — but it is manageable with proper configuration. Kali is not needed, but Docker isolation is essential.

### Security Risks in OpenClaw:

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|------------|
| **Prompt Injection** | High | Malicious instructions can be injected via fleet data | Input sanitization, guardrails |
| **API Key Exposure** | Critical | Agent could access API keys | Environment variables, never in code |
| **File System Access** | High | Agent can read/write files | Docker sandboxing, workspace isolation |
| **Network Access** | Medium | Agent can call external APIs | Firewall rules, allowlist |
| **Data Leakage** | High | Agent could leak sensitive data | Guardrails, audit logging |
| **Command Injection** | Critical | Agent could execute shell commands | Disable exec, use safe tools only |

### Recommended Security Setup:

**Level 1: Docker Isolation (Minimum)**
```yaml
# docker-compose.yml
services:
  openclaw:
    image: node:22-alpine
    volumes:
      - ./agent-workspace:/app/workspace:ro  # Read-only workspace
    read_only: true  # Container is read-only
    security_opt:
      - no-new-privileges:true  # No privilege escalation
    cap_drop:
      - ALL  # Drop all capabilities
    cap_add:
      - NET_BIND_SERVICE  # Only bind to ports
```

**Level 2: Network Isolation (Recommended)**
```yaml
services:
  openclaw:
    networks:
      - internal  # Can only access internal network
    dns:
      - 8.8.8.8  # Only known DNS servers

networks:
  internal:
    internal: true  # No external access
```

**Level 3: Full Sandbox (Maximum Security)**
```bash
# Use gVisor or Firecracker for kernel-level isolation
# Or run in a dedicated VM on Hetzner/DigitalOcean
```

### Kali Linux? Why Would You Need It?

**No, Kali is not needed.** Kali is for penetration testing — not fleet management. For proper security:

1. **Docker** — Container isolation
2. **Firewall** — Only required ports open (80, 443, 18789)
3. **Fail2ban** — Brute force protection
4. **SSH Keys** — No password authentication
5. **Regular Updates** — Security patches
6. **Environment Variables** — No hardcoded secrets
7. **Audit Logging** — Every action tracked

### Security Checklist:

- [ ] Run OpenClaw in Docker container
- [ ] Use read-only filesystem for container
- [ ] Drop all Linux capabilities
- [ ] Use internal Docker network
- [ ] Store API keys in environment variables
- [ ] Enable audit logging
- [ ] Set up firewall (only ports 80, 443, 18789)
- [ ] Install fail2ban
- [ ] Use SSH keys (no passwords)
- [ ] Regular security updates
- [ ] Weekly security scan

---

## 3. Samsara Free Data

### Q: Is Samsara data free? Without legal issues?

**Short Answer:** Yes, Samsara's **developer sandbox** is free. You won't get real fleet data, but you get test data which is sufficient for demos.

### Samsara Free Options:

| Option | Cost | Data Type | Legal? | Use Case |
|--------|------|-----------|--------|----------|
| **Developer Sandbox** | Free | Test/mock data | ✅ Yes | Development, testing |
| **API with Subscription** | Free (API) | Real fleet data | ✅ Yes | Production (client pays for hardware) |
| **Sample Data** | Free | Static JSON | ✅ Yes | Demo, prototyping |
| **Mock Data (Our System)** | Free | Realistic fake data | ✅ Yes | Demo without Samsara account |

### How to Get Samsara Developer Access:

1. Go to: https://developers.samsara.com
2. Click "Get Started" or "Sign Up"
3. Create free developer account
4. Get API token from dashboard
5. Use sandbox endpoints (test data)

### Samsara API Endpoints (Free Sandbox):

```
GET /v1/fleet/vehicles          → List vehicles (test data)
GET /v1/fleet/vehicles/stats    → Vehicle stats (test data)
GET /v1/fleet/drivers           → Driver list (test data)
GET /v1/fleet/drivers/{id}/hos  → HOS status (test data)
GET /v1/faults                  → Fault codes (test data)
POST /v1/fleet/vehicles         → Create test vehicle
```

### Our Mock Data System (Best for Demo):

We already built a **mock data system** that generates realistic fleet data:
- 52 vehicles with real locations
- 20 drivers with HOS status
- 15 fault codes (P0340, P0300, etc.)
- Fuel levels, speed, odometer

**This works WITHOUT any Samsara account.** Perfect for demo.

### Legal Status:

| Action | Legal? | Notes |
|--------|--------|-------|
| Using Samsara developer sandbox | ✅ Yes | Free, designed for development |
| Using Samsara API with client's subscription | ✅ Yes | Client pays for hardware |
| Using mock/fake data | ✅ Yes | Our data, no legal issues |
| Scraping Samsara website | ❌ No | Violates Terms of Service |
| Using leaked API keys | ❌ No | Illegal access |

---

## 4. [Client]'s Setup

### Q: What will [Client] use? Windows, Linux, or online server?

**Short Answer:** [Client] **doesn't need to do anything** — everything runs on the server. [Client] only uses a browser or Telegram.

### What [Client] Needs:

| Item | What | Why |
|------|------|-----|
| **Computer** | Any (Windows/Mac/Linux) | Only for browser access |
| **Browser** | Chrome/Firefox/Safari | Dashboard access |
| **Telegram** | Mobile app | Alerts + approvals |
| **Internet** | Normal broadband | Dashboard + Telegram |
| **Nothing else** | — | Everything runs on server |

### Server Setup (You Handle This):

| Component | Where | [Client]'s Involvement |
|-----------|-------|-------------------|
| OpenClaw Gateway | Cloud server | None — you deploy |
| FastAPI Backend | Cloud server | None — you deploy |
| PostgreSQL Database | Cloud server | None — you deploy |
| Redis Cache | Cloud server | None — you deploy |
| Telegram Bot | Telegram servers | None — you create |
| Samsara API | Samsara servers | [Client] gives API key |

### [Client]'s Daily Workflow:

```
Morning:
  → Daily summary arrives on Telegram (8 AM)
  → "52 active vehicles, 3 faults, 2 pending approvals"

During Day:
  → Alerts arrive on Telegram (real-time)
  → "🚨 Truck #842 — Engine fault P0340"
  → [Client] taps [✅ Approve] or [❌ Reject]

Evening:
  → Evening summary on Telegram
  → Can view dashboard in browser (optional)
```

### What [Client] Needs to Learn:

| Skill | Difficulty | Time |
|-------|-----------|------|
| Using Telegram | Very Easy | 5 minutes |
| Viewing dashboard in browser | Very Easy | 2 minutes |
| Tapping Approve/Reject buttons | Very Easy | 1 minute |
| Nothing — agent does everything automatically | — | — |

---

## 5. App vs Website

### Q: Does [Client] need an app or a website?

**Short Answer:** **Both** — Website (dashboard) + Telegram Bot (mobile). No need to build a native app yet.

### Why Website + Telegram (Not Native App):

| Factor | Website + Telegram | Native App |
|--------|-------------------|------------|
| **Development Time** | 2-3 weeks | 2-3 months |
| **Maintenance** | Easy (server-side) | Complex (app updates) |
| **Platform** | All devices | iOS + Android separate |
| **Updates** | Instant | App store review |
| **[Client]'s Learning** | Zero (browser + Telegram) | Install app, learn UI |
| **Offline** | Limited | Better offline support |
| **Push Notifications** | Telegram handles it | Native push |

### What We Have:

1. **Web Dashboard** (http://server:8000)
   - Modern responsive UI
   - Works on desktop, tablet, mobile
   - Real-time fleet overview
   - Vehicle tracking, alerts, compliance
   - No installation needed

2. **Telegram Bot** (Mobile)
   - Instant alerts
   - Approve/reject buttons
   - Daily summaries
   - Works on any phone
   - No app installation (Telegram already installed)

### Future: Native App (Phase 5+)

If [Client] wants a native app later:
- **React Native** — Cross-platform (iOS + Android)
- **Cost:** $15,000-25,000
- **Timeline:** 2-3 months
- **Features:** Offline mode, push notifications, camera integration

---

## 6. Real-time Tracking

### Q: Can real-time tracking happen every 5 seconds?

**Short Answer:** Yes, it is possible — but Samsara API has limits. Best approach: **webhooks (instant) + polling (every 30 seconds)**.

### Real-time Tracking Options:

| Method | Frequency | Latency | API Calls | Cost |
|--------|-----------|---------|-----------|------|
| **Webhooks** | Instant | <1 sec | 0 (push) | Free |
| **Polling (5s)** | Every 5 sec | 5 sec | 12/min/vehicle | High |
| **Polling (30s)** | Every 30 sec | 30 sec | 2/min/vehicle | Medium |
| **Polling (5min)** | Every 5 min | 5 min | 0.2/min/vehicle | Low |

### Recommended Setup:

```
Primary:   Samsara Webhooks (instant alerts)
Secondary: Polling every 30 seconds (backup)
Dashboard: Auto-refresh every 30 seconds
```

### Webhook Flow (Instant):

```
Samsara detects event (speeding, fault, geofence)
    │
    ▼
Webhook POST to our server (< 1 second)
    │
    ▼
FastAPI receives event
    │
    ▼
Celery processes event
    │
    ▼
Telegram alert sent to [Client] (< 2 seconds total)
```

### Polling Flow (Backup):

```
Every 30 seconds:
    │
    ▼
Celery task runs
    │
    ▼
Fetch vehicle stats from Samsara API
    │
    ▼
Compare with previous data
    │
    ▼
If changed → Update database → Notify dashboard
```

### Samsara API Rate Limits:

| Tier | Requests/Second | Requests/Minute | Vehicles Supported |
|------|----------------|-----------------|-------------------|
| Free (sandbox) | 1 | 60 | ~10 |
| Standard | 5 | 300 | ~50 |
| Enterprise | 20 | 1200 | ~200+ |

### For 52 Vehicles with 5-Second Updates:

- API calls needed: 52 vehicles × 12/min = 624 calls/min
- Samsara standard tier: 300 calls/min
- **Solution:** Use webhooks (0 API calls) + polling every 30s (104 calls/min)

---

## 7. Call & Communication

### Q: Is there a call option? Does the truck need a mic and speaker?

**Short Answer:** Yes, call option exists — but the truck needs hardware. Samsara/AI dashcams have it built-in.

### Call Options:

| Method | Hardware Needed | Cost | Quality | Use Case |
|--------|----------------|------|---------|----------|
| **Samsara Dashcam** | Built-in mic + speaker | Included | Good | Primary |
| **Driver's Phone** | Driver ka phone | Free | Good | Backup |
| **CB Radio** | CB radio in truck | $100-300 | Fair | Legacy |
| **Dedicated Intercom** | Intercom system | $200-500 | Excellent | High-end |

### How Call Works in Our System:

```
[Client] taps [📞 Call Driver] in dashboard/Telegram
    │
    ▼
System finds driver's phone number
    │
    ▼
Option A: Twilio API initiates call (server-side)
Option B: Samsara dashcam intercom activation
Option C: WhatsApp/Telegram voice call
    │
    ▼
Driver answers (on phone or dashcam speaker)
    │
    ▼
[Client] speaks to driver
```

### Hardware in Truck:

| Component | Present? | Purpose |
|-----------|----------|---------|
| **GPS Tracker** | ✅ Already installed | Location tracking |
| **AI Dashcam** | ✅ Already installed | Video + audio |
| **Microphone** | ✅ Built into dashcam | Driver communication |
| **Speaker** | ✅ Built into dashcam | [Client]'s voice to driver |
| **ELD Device** | ✅ Already installed | Compliance logging |
| **OBD-II Port** | ✅ Already installed | Engine diagnostics |

### Call Integration Options:

**Option A: Twilio (Recommended)**
```python
# Server-side call initiation
from twilio.rest import Client

client = Client(account_sid, auth_token)
call = client.calls.create(
    to="+13175551234",  # Driver's phone
    from_="+13175559999",  # Fleet number
    url="http://server/twiml/connect"  # Connect to [Client]
)
```
- Cost: $0.01-0.05/minute
- Setup: Twilio account + phone number

**Option B: Samsara Dashcam Intercom**
- Built into Samsara AI dashcams
- Activate via Samsara API
- No additional hardware needed
- Cost: Included in Samsara subscription

**Option C: WhatsApp/Telegram Voice Call**
- Free
- Uses driver's phone
- Requires internet connection
- Quality depends on connection

---

## 8. Dashcam Integration

### Q: How will the dashcam connect? How will live footage be accessed?

**Short Answer:** Samsara AI dashcam has a built-in API. Both live stream and recorded clips can be accessed.

### Dashcam Integration Architecture:

```
Samsara AI Dashcam (in truck)
    │
    ├── Front Camera (road-facing)
    ├── Rear Camera (driver-facing)
    ├── GPS Module
    ├── Microphone + Speaker
    └── 4G/LTE Connection
         │
         ▼
    Samsara Cloud Server
         │
         ▼
    Samsara API
         │
         ├── GET /v1/fleet/cameras/{id}/stream → Live stream
         ├── GET /v1/fleet/cameras/{id}/clips → Recorded clips
         ├── POST /v1/fleet/cameras/{id}/snapshot → Take photo
         └── Webhook: CameraEvent → Motion/crash detected
         │
         ▼
    Our Fleet-[Client] Backend
         │
         ▼
    Dashboard (live feed) + Telegram (alert clips)
```

### What We Can Access:

| Feature | API Endpoint | Description |
|---------|-------------|-------------|
| **Live Stream** | `/cameras/{id}/stream` | Real-time video feed |
| **Snapshots** | `/cameras/{id}/snapshot` | Take photo anytime |
| **Recorded Clips** | `/cameras/{id}/clips` | Get recorded footage |
| **Events** | Webhook | Motion, crash, harsh driving |
| **Driver-facing** | `/cameras/{id}/rear` | Driver behavior video |

### Dashboard Integration:

```html
<!-- Live dashcam feed in dashboard -->
<div class="dashcam-feed">
    <video id="dashcamStream" autoplay muted>
        <source src="https://api.samsara.com/v1/fleet/cameras/TRUCK-001/stream" type="video/mp4">
    </video>
    <span class="live-badge">LIVE</span>
</div>
```

### Alert with Video Clip:

```
Samsara detects harsh braking
    │
    ▼
Webhook sends event + video clip URL
    │
    ▼
Our system processes event
    │
    ▼
Telegram alert with video thumbnail:
    "🚨 Truck #842 — Harsh braking detected"
    [📹 View Clip] [📞 Call Driver] [✅ Acknowledge]
```

### Dashcam Hardware Specs (Samsara AI Dashcam):

| Feature | Spec |
|---------|------|
| **Front Camera** | 1080p, 120° FOV |
| **Rear Camera** | 720p, 120° FOV |
| **Storage** | 64GB local + cloud |
| **Connectivity** | 4G LTE + WiFi |
| **GPS** | Built-in, 10Hz |
| **Microphone** | Built-in, noise-canceling |
| **Speaker** | Built-in, for driver communication |
| **AI Processing** | On-device (distraction, collision) |

---

## 9. Database Architecture

### Q: Which database will be used? Why and how?

**Short Answer:** **3 databases** — PostgreSQL (main), Redis (cache), SQLite (testing). Each has a different purpose.

### Database Architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  PostgreSQL (Main Database)                       │   │
│  │  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │ vehicles    │  │ drivers     │                │   │
│  │  │ (23 fields) │  │ (16 fields) │                │   │
│  │  └─────────────┘  └─────────────┘                │   │
│  │  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │ fault_codes │  │ audit_log   │                │   │
│  │  │ (11 fields) │  │ (13 fields) │                │   │
│  │  └─────────────┘  └─────────────┘                │   │
│  │  ┌─────────────┐                                 │   │
│  │  │ escalations │                                 │   │
│  │  │ (19 fields) │                                 │   │
│  │  └─────────────┘                                 │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Redis (Cache + Queue)                            │   │
│  │  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │ Cache       │  │ Task Queue  │                │   │
│  │  │ (5 min TTL) │  │ (Celery)    │                │   │
│  │  └─────────────┘  └─────────────┘                │   │
│  │  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │ Rate Limit  │  │ Sessions    │                │   │
│  │  │ (per client)│  │ (agent)     │                │   │
│  │  └─────────────┘  └─────────────┘                │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  SQLite (Testing Only)                            │   │
│  │  ┌─────────────┐                                 │   │
│  │  │ test.db     │  → Local development            │   │
│  │  │ (same schema)│  → No server needed            │   │
│  │  └─────────────┘                                 │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Why 3 Databases?

| Database | Purpose | Why This One | Alternative |
|----------|---------|-------------|-------------|
| **PostgreSQL** | Main data storage | JSON support, full-text search, audit trails, ACID compliant | MySQL (less features), MongoDB (no ACID) |
| **Redis** | Cache + task queue | In-memory (fast), pub/sub, TTL support | Memcached (no queue), RabbitMQ (no cache) |
| **SQLite** | Testing | Zero config, file-based, same SQL syntax | H2 (Java only), HSQLDB (Java only) |

### PostgreSQL Tables Deep Dive:

**vehicles table (23 fields):**
```sql
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) UNIQUE,     -- "TRUCK-001"
    name VARCHAR(100),                  -- "Truck #1"
    make VARCHAR(50),                   -- "Freightliner"
    model VARCHAR(50),                  -- "Cascadia"
    year INTEGER,                       -- 2022
    vin VARCHAR(17),                    -- "1HGCM82633A..."
    status VARCHAR(20),                 -- "active", "idle", "maintenance"
    latitude FLOAT,                     -- 39.7684
    longitude FLOAT,                    -- -86.1581
    address VARCHAR(200),               -- "Indianapolis, IN"
    speed FLOAT,                        -- 65.0
    fuel_level FLOAT,                   -- 72.0
    odometer FLOAT,                     -- 125430.0
    engine_hours FLOAT,                 -- 12500.0
    engine_status VARCHAR(20),          -- "running", "off"
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**audit_log table (13 fields):**
```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,                -- When it happened
    action_type VARCHAR(50),            -- "alert", "escalation", "query"
    severity VARCHAR(20),               -- "critical", "high", "medium", "low"
    vehicle_id VARCHAR(50),             -- Which vehicle
    driver_id VARCHAR(50),              -- Which driver
    description TEXT,                   -- What happened
    details JSON,                       -- Full context (JSON)
    agent_decision VARCHAR(50),         -- "auto_act", "escalated", "logged"
    human_response VARCHAR(50),         -- "approved", "rejected", "timeout"
    human_responder VARCHAR(100),       -- "[Client Name]"
    outcome VARCHAR(100),               -- "maintenance_scheduled"
    cost FLOAT                          -- 450.00
);
```

### Redis Usage:

| Key Pattern | TTL | Purpose |
|-------------|-----|---------|
| `vehicle:TRUCK-001` | 5 min | Cache vehicle data |
| `fleet:overview` | 1 min | Cache fleet overview |
| `rate:api:user123` | 1 min | Rate limiting |
| `celery:task:uuid` | 1 hour | Task results |
| `session:agent:main` | 24 hours | Agent session state |

### Why Not MongoDB?

| Factor | PostgreSQL | MongoDB |
|--------|-----------|---------|
| **ACID Compliance** | ✅ Full | ⚠️ Limited |
| **JSON Support** | ✅ JSONB (fast) | ✅ Native |
| **Full-text Search** | ✅ Built-in | ✅ Built-in |
| **Audit Trails** | ✅ Perfect | ⚠️ Manual |
| **Joins** | ✅ Native | ⚠️ Manual |
| **FMCSA Compliance** | ✅ Yes | ⚠️ Needs proof |
| **Maturity** | 30+ years | 15 years |

### Data Retention Policy:

| Data Type | Retention | Archive | Reason |
|-----------|-----------|---------|--------|
| Vehicle locations | 90 days | Compress | High volume |
| Fault codes | 1 year | Archive | Pattern analysis |
| Audit logs | 7 years | Archive | FMCSA requirement |
| Escalations | 2 years | Archive | Legal |
| Driver HOS | 6 months | Archive | FMCSA requirement |
| Fuel transactions | 1 year | Archive | IFTA requirement |

---

## 10. AI Learning

### Q: How will the AI learn? What will be saved in the database?

**Short Answer:** The AI learns through **MEMORY.md** and **daily memory files**. It remembers patterns and does not repeat mistakes.

### How AI Learns:

```
Day 1: Truck #842 has P0340 fault
    │
    ▼
AI sends alert → [Client] approves → Maintenance scheduled
    │
    ▼
AI writes to MEMORY.md:
    "Truck #842 has recurring P0340 fault (camshaft sensor)"
    "Last maintenance: July 5, 2026"
    "Cost: $450"
    │
    ▼
Day 15: P0340 appears again
    │
    ▼
AI remembers: "This happened before"
    │
    ▼
AI detects pattern:
    "Truck #842 has P0340 every 2 weeks — needs permanent fix"
    │
    ▼
AI tells [Client]:
    "⚠️ Truck #842 has recurring P0340 fault.
     Pattern: Every 2 weeks. Recommend: Full camshaft system check.
     Estimated cost: $1,200 (one-time) vs $450 every 2 weeks ($1,170/6 months)"
```

### What AI Stores in Memory:

**Short-term (daily files):**
```markdown
# memory/2026-07-05.md
- 09:00 — Fleet health check: 52 vehicles, 30 active
- 09:15 — Fault detected: P0340 on TRUCK-842
- 09:16 — Escalation sent to [Client]
- 09:18 — [Client] approved maintenance
- 09:20 — Maintenance scheduled for July 6
- 10:00 — Fuel anomaly: TRUCK-015 dropped 25% in 30 min
- 10:01 — Alert sent, investigating
```

**Long-term (MEMORY.md):**
```markdown
# Fleet Patterns
- Truck #842: Recurring P0340 fault (camshaft sensor)
  - Frequency: Every 2 weeks
  - Last: July 5, 2026
  - Recommendation: Full system check

- Truck #015: Fuel anomaly pattern
  - July 5: 25% drop in 30 min (possible theft)
  - Location: Chicago terminal
  - Action: Investigate fuel card transactions

- Driver Mike Johnson:
  - Consistently near HOS limit (10.5+ hrs)
  - Prefers night shifts
  - Routes: Indianapolis ↔ Chicago
```

### AI Learning Capabilities:

| What AI Learns | How | Example |
|---------------|-----|---------|
| **Fault patterns** | Tracks fault codes per vehicle | "Truck #842 has P0340 every 2 weeks" |
| **Driver behavior** | Tracks HOS, speeding, harsh events | "Mike J. always near HOS limit" |
| **Fuel patterns** | Tracks fuel consumption per route | "Indianapolis-Chicago route: 8.2 MPG avg" |
| **Maintenance costs** | Tracks cost per vehicle/type | "Truck #842 maintenance: $450/visit avg" |
| **Seasonal trends** | Tracks patterns over months | "Winter: 30% more battery faults" |
| **Route efficiency** | Tracks miles/time per route | "I-65 route 15% faster than I-70" |

### Database vs Memory:

| Data | Where Stored | Why |
|------|-------------|-----|
| **Vehicle locations** | PostgreSQL | High volume, need SQL queries |
| **Fault codes** | PostgreSQL | Need pattern analysis |
| **Audit logs** | PostgreSQL | Legal requirement (7 years) |
| **AI patterns** | MEMORY.md | Agent reads every session |
| **Daily context** | memory/YYYY-MM-DD.md | Agent reads today + yesterday |
| **Cached data** | Redis | Fast access, auto-expire |

---

## 11. Technical Glossary

| Word | Meaning |
|------|---------|
| **API** | Application Programming Interface — connection between two systems |
| **Backend** | Server-side code — not visible to the user, does the work |
| **Frontend** | User-facing website/app — what the user sees |
| **Webhook** | Server-to-server push notification — instant data when something happens |
| **LLM** | Large Language Model — AI brain (GPT, Claude, Llama) |
| **Heartbeat** | Periodic check — agent checks every X minutes |
| **HITL** | Human-in-the-Loop — AI asks human before acting |
| **Guardrails** | Safety rules — what AI can and cannot do |
| **Audit Trail** | Complete log — who did what and when |
| **Escalation** | Sending an issue to a human — when AI cannot handle it |
| **HOS** | Hours of Service — how many hours a driver has driven |
| **DVIR** | Driver Vehicle Inspection Report — pre/post trip check |
| **IFTA** | International Fuel Tax Agreement — fuel tax reporting |
| **DTC** | Diagnostic Trouble Code — vehicle error code |
| **ELD** | Electronic Logging Device — automatic driving hours log |
| **GPS** | Global Positioning System — location tracking |
| **OBD-II** | On-Board Diagnostics — vehicle diagnostic port |
| **Telematics** | Remote vehicle data collection |
| **CSA** | Compliance, Safety, Accountability — FMCSA safety score |
| **FMCSA** | Federal Motor Carrier Safety Administration — US trucking regulator |
| **Geofence** | Virtual boundary — triggers when vehicle enters/exits area |
| **Idling** | Engine on but vehicle not moving — wastes fuel |
| **Fault Code** | Vehicle error code — P0340, P0300, etc. |
| **Celery** | Python task queue — handles background jobs |
| **Redis** | In-memory database — fast cache and queue |
| **PostgreSQL** | Main database — permanent data storage |
| **Docker** | Containerization — run apps in isolated boxes |
| **Container** | Isolated environment — app runs in its own box |
| **VPS** | Virtual Private Server — online computer |
| **SSL/TLS** | Encryption — keeps data secure |
| **HTTPS** | Secure HTTP — encrypted web connection |
| **REST API** | Web API standard — GET, POST, PUT, DELETE |
| **JSON** | Data format — {"key": "value"} |
| **Schema** | Database structure — table blueprint |
| **Migration** | Database structure change — adding new columns |
| **ORM** | Object-Relational Mapping — Python talks to database |
| **Pydantic** | Python data validation — input checking |
| **FastAPI** | Python web framework — for building REST APIs |
| **Swagger** | API documentation — interactive API testing |
| **OpenAPI** | API specification standard |
| **CDN** | Content Delivery Network — fast file delivery |
| **DNS** | Domain Name System — website address system |
| **SSH** | Secure Shell — secure server login |
| **CI/CD** | Continuous Integration/Deployment — automatic code deployment |
| **Git** | Version control — code history and tracking |
| **GitHub** | Code hosting platform — store code online |
| **Repository (Repo)** | Project folder on GitHub |
| **Commit** | Save changes to Git |
| **Push** | Upload to GitHub |
| **Clone** | Download from GitHub |
| **Branch** | Parallel version of code |
| **Merge** | Combine branches |
| **Pull Request** | Request to merge code changes |
| **Environment Variables** | Secret config values — API keys, passwords |
| **.env** | Environment file — stores secrets |
| **.gitignore** | Files Git should ignore — secrets, temp files |
| **Mock Data** | Fake data for testing — demo without real API |
| **Sandbox** | Isolated testing environment |
| **Rate Limiting** | Limit API calls per time — prevent abuse |
| **Latency** | Delay — time taken for response |
| **Uptime** | Time server is running (e.g., 99.9%) |
| **Downtime** | Time server is down — maintenance or crash |
| **SLA** | Service Level Agreement — guaranteed uptime |
| **Backup** | Data copy — recover if data is lost |
| **Restore** | Recover from backup |
| **Firewall** | Network security — blocks unauthorized access |
| **Encryption** | Data coding — only authorized people can read |
| **Decryption** | Reverse encryption — decoding data |
| **Token** | Authentication key — for access |
| **JWT** | JSON Web Token — secure authentication |
| **OAuth** | Open Authorization — third-party login |
| **Polling** | Periodic checking — check every X seconds |
| **Streaming** | Real-time data flow — continuous data |
| **Dashboard** | Visual data display — charts, graphs, maps |
| **Widget** | Small UI component — button, card, chart |
| **Responsive** | Works on all screen sizes — desktop, tablet, mobile |
| **Viewport** | Screen size — varies by device |
| **CSS** | Styling language — website design |
| **HTML** | Structure language — website structure |
| **JavaScript** | Programming language — website behavior |
| **DOM** | Document Object Model — HTML tree structure |
| **Async** | Non-blocking — do multiple things simultaneously |
| **Await** | Wait for async result |
| **Callback** | Function called after task completes |
| **Promise** | Async result container — result arrives later |
| **Middleware** | Code that runs between request and response |
| **Endpoint** | API URL — where requests go |
| **Route** | URL pattern — which URL triggers which code |
| **Handler** | Function that processes a request |
| **Payload** | Data sent in request/response |
| **Header** | Request metadata — auth token, content type |
| **Body** | Request data — actual content |
| **Status Code** | HTTP response code — 200 = OK, 404 = Not Found, 500 = Error |
| **200 OK** | Success — request worked |
| **404 Not Found** | Resource not found |
| **500 Internal Server Error** | Server error |
| **401 Unauthorized** | Authentication required |
| **403 Forbidden** | Access denied |
| **429 Too Many Requests** | Rate limit exceeded |
