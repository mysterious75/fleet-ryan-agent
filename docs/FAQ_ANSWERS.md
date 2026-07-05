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

### Q: AI kahan hai? Kya model use hoga?

**Short Answer:** OpenClaw agent ka "brain" ek LLM (Large Language Model) hota hai. Bina LLM ke agent sirf ek script hai — intelligent decisions nahi le sakta.

**Detailed Answer:**

OpenClaw ek **agent framework** hai — ye khud AI nahi hai. Ye ek "container" hai jo ek AI model ko fleet management ka kaam deta hai. Jaise ek employee ka desk hota hai, waise OpenClaw AI model ka "desk" hai.

### LLM Options (Kya use karna chahiye):

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

### Recommended Setup for Ryan:

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

### Q: OpenClaw mein security risk hai? Kya sandbox ya Kali mein chalana chahiye?

**Short Answer:** Haan, security risk hai — lekin proper configuration se manageable hai. Kali zaroorat nahi hai, lekin Docker isolation zaroori hai.

### Security Risks in OpenClaw:

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|------------|
| **Prompt Injection** | High | User fleet data mein malicious instructions daal sakta hai | Input sanitization, guardrails |
| **API Key Exposure** | Critical | Agent API keys access kar sakta hai | Environment variables, never in code |
| **File System Access** | High | Agent files read/write kar sakta hai | Docker sandboxing, workspace isolation |
| **Network Access** | Medium | Agent external APIs call kar sakta hai | Firewall rules, allowlist |
| **Data Leakage** | High | Agent sensitive data leak kar sakta hai | Guardrails, audit logging |
| **Command Injection** | Critical | Agent shell commands execute kar sakta hai | Disable exec, use safe tools only |

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

### Kali Linux? Kya Zaroorat Hai?

**Nahi, Kali zaroorat nahi hai.** Kali penetration testing ke liye hai — fleet management ke liye nahi. Proper security ke liye:

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

### Q: Samsara ka free data hai? Bina law issue ke?

**Short Answer:** Haan, Samsara ka **developer sandbox** free hai. Real fleet data nahi milega, lekin test data milega jo demo ke liye kaafi hai.

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
| Scraping Samsara website | ❌ No | Violates ToS |
| Using leaked API keys | ❌ No | Illegal access |

---

## 4. [Client]'s Setup

### Q: [Client] kya use krega? Windows PC, Linux, ya online server?

**Short Answer:** [Client] ko **kuch nahi karna** — sab server pe hoga. [Client] sirf browser ya Telegram use karega.

### What [Client] Needs:

| Item | What | Why |
|------|------|-----|
| **Computer** | Any (Windows/Mac/Linux) | Sirf browser ke liye |
| **Browser** | Chrome/Firefox/Safari | Dashboard access |
| **Telegram** | Mobile app | Alerts + approvals |
| **Internet** | Normal broadband | Dashboard + Telegram |
| **Nothing else** | — | Sab server pe hoga |

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
  → Telegram pe daily summary aata hai (8 AM)
  → "52 active vehicles, 3 faults, 2 pending approvals"

During Day:
  → Telegram pe alerts aate hain (real-time)
  → "🚨 Truck #842 — Engine fault P0340"
  → [Client] taps [✅ Approve] or [❌ Reject]

Evening:
  → Telegram pe evening summary
  → Browser pe dashboard dekh sakta hai (optional)
```

### [Client] Ko Kya Sikhna Padega:

| Skill | Difficulty | Time |
|-------|-----------|------|
| Telegram use karna | Very Easy | 5 minutes |
| Browser mein dashboard dekhna | Very Easy | 2 minutes |
| Approve/Reject buttons tap karna | Very Easy | 1 minute |
| Kuch nahi — agent sab khud karta hai | — | — |

---

## 5. App vs Website

### Q: [Client] ko app chahiye ya website?

**Short Answer:** **Dono** — Website (dashboard) + Telegram Bot (mobile). App banane ki zaroorat nahi hai abhi.

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

### Q: Har 5 second pe real-time tracking ho sakta hai?

**Short Answer:** Haan, possible hai — lekin Samsara API ke limits hain. Best approach: **webhooks (instant) + polling (every 30 seconds)**.

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

### Q: Call ka option hai? Truck mein mic aur speaker chahiye?

**Short Answer:** Haan, call ka option hai — lekin truck mein hardware chahiye. Samsara/AI dashcam mein built-in hota hai.

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
    url="http://server/twiml/connect"  # Connect to Ryan
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

### Q: Dashcam se connect kaise hoga? Live footage kaise aayegi?

**Short Answer:** Samsara AI dashcam mein built-in API hai. Live stream aur recorded clips dono access kar sakte hain.

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

### Q: Kaun sa database lagega? Kyun aur kaise?

**Short Answer:** **3 databases** — PostgreSQL (main), Redis (cache), SQLite (testing). Har ek ka alag kaam hai.

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

### Q: AI seekhega kaise? Database mein kya save hoga?

**Short Answer:** AI **MEMORY.md** aur **daily memory files** mein seekhta hai. Patterns yaad rakhta hai, mistakes repeat nahi karta.

### How AI Learns:

```
Day 1: Truck #842 mein P0340 fault aaya
    │
    ▼
AI ne alert bheja → [Client] ne approve kiya → Maintenance scheduled
    │
    ▼
AI ne MEMORY.md mein likha:
    "Truck #842 has recurring P0340 fault (camshaft sensor)"
    "Last maintenance: July 5, 2026"
    "Cost: $450"
    │
    ▼
Day 15: Phir se P0340 aaya
    │
    ▼
AI ne yaad kiya: "Ye pehle bhi hua tha"
    │
    ▼
AI ne pattern detect kiya:
    "Truck #842 has P0340 every 2 weeks — needs permanent fix"
    │
    ▼
AI ne [Client] ko bola:
    "⚠️ Truck #842 mein P0340 baar baar aa raha hai.
     Pattern: Har 2 weeks. Recommend: Full camshaft system check.
     Estimated cost: $1,200 (one-time) vs $450 every 2 weeks ($1,170/6 months)"
```

### What AI Stores in Memory:

**Short-term (daily files):**
```markdown
# memory/2026-07-05.md
- 09:00 — Fleet health check: 52 vehicles, 30 active
- 09:15 — Fault detected: P0340 on TRUCK-842
- 09:16 — Escalation sent to Ryan
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

### Sab Words Ka Meaning:

| Word | Meaning | Hindi/Urdu |
|------|---------|-----------|
| **API** | Application Programming Interface — Do systems ke beech ka connection | Do software ka baatcheet ka raasta |
| **Backend** | Server-side code — user ko nahi dikhta, kaam karta hai | Pardhe ke peeche ka kaam |
| **Frontend** | User-facing website/app — jo user dekhta hai | Jo screen pe dikhta hai |
| **Webhook** | Server se server push notification — jab kuch hota hai toh turant data aata hai | Jab kuch ho toh turant khabar aana |
| **LLM** | Large Language Model — AI brain (GPT, Claude, Llama) | AI ka dimaag |
| **Heartbeat** | Periodic check — agent har X minute pe check karta hai | Har thodi der mein check karna |
| **HITL** | Human-in-the-Loop — AI insaan se poochta hai karne se pehle | Insaan se ijazat lena |
| **Guardrails** | Safety rules — AI kya kar sakta hai, kya nahi | Suraksha niyam |
| **Audit Trail** | Complete log — kaun kab kya kiya | Poora hisaab |
| **Escalation** | Issue ko insaan tak pahunchana — jab AI khud nahi kar sakta | Insaan tak baat pahunchana |
| **HOS** | Hours of Service — kitne ghante driver ne gaadi chalayi | Driving ka samay |
| **DVIR** | Driver Vehicle Inspection Report — pre/post trip check | Gaadi ka check-up |
| **IFTA** | International Fuel Tax Agreement — fuel tax reporting | Fuel ka tax hisaab |
| **DTC** | Diagnostic Trouble Code — gaadi ka error code | Gaadi ki galti ka code |
| **ELD** | Electronic Logging Device — automatic driving hours log | Automatic driving record |
| **GPS** | Global Positioning System — location tracking | Location pata karna |
| **OBD-II** | On-Board Diagnostics — gaadi ka diagnostic port | Gaadi ka check-up port |
| **Telematics** | Remote vehicle data collection | Door se gaadi ka data lena |
| **CSA** | Compliance, Safety, Accountability — FMCSA safety score | Suraksha score |
| **FMCSA** | Federal Motor Carrier Safety Administration — US trucking regulator | US trucking ka niyamak |
| **Geofence** | Virtual boundary — jab gaadi area mein enter/exit kare | Virtual seema |
| **Idling** | Engine on but vehicle not moving — fuel waste | Engine chalana par gaadi na chalana |
| **Fault Code** | Vehicle error code — P0340, P0300, etc. | Gaadi ka error |
| **Celery** | Python task queue — background jobs | Background kaam ka queue |
| **Redis** | In-memory database — fast cache + queue | Tez temporary storage |
| **PostgreSQL** | Main database — permanent data storage | Permanent data ka ghar |
| **Docker** | Containerization — app ko isolated box mein chalana | App ko alag box mein rakhna |
| **Container** | Isolated environment — app apne box mein chalta hai | Alag box mein chalna |
| **VPS** | Virtual Private Server — online computer | Online computer |
| **SSL/TLS** | Encryption — data secure rehta hai | Data ki suraksha |
| **HTTPS** | Secure HTTP — encrypted web connection | Surakshit web connection |
| **REST API** | Web API standard — GET, POST, PUT, DELETE | Web ka baatcheet ka tareeka |
| **JSON** | Data format — {"key": "value"} | Data ka format |
| **Schema** | Database structure — table ka blueprint | Table ka naksha |
| **Migration** | Database structure change — naya column add karna | Table mein badlav |
| **ORM** | Object-Relational Mapping — Python se SQL | Python se database baat karna |
| **Pydantic** | Python data validation — input check karna | Data ki jaanch |
| **FastAPI** | Python web framework — REST API banane ke liye | Python ka web tool |
| **Swagger** | API documentation — interactive API testing | API ka manual |
| **OpenAPI** | API specification standard — Swagger ka standard | API ka standard |
| **CDN** | Content Delivery Network — fast file delivery | Tez file delivery |
| **DNS** | Domain Name System — website ka address system | Website ka pata system |
| **SSH** | Secure Shell — server pe login | Server pe surakshit login |
| **CI/CD** | Continuous Integration/Deployment — automatic code deploy | Automatic code daalna |
| **Git** | Version control — code ka hisaab | Code ka version hisaab |
| **GitHub** | Code hosting platform — code online rakhna | Code ka online ghar |
| **Repository (Repo)** | Project folder on GitHub | Project ka folder |
| **Commit** | Save changes to Git | Changes save karna |
| **Push** | Upload to GitHub | GitHub pe daalna |
| **Clone** | Download from GitHub | GitHub se lena |
| **Branch** | Parallel version of code | Code ki alag copy |
| **Merge** | Combine branches | Copies milana |
| **Pull Request** | Request to merge code | Code milane ki request |
| **Environment Variables** | Secret config values — API keys, passwords | Secret settings |
| **.env** | Environment file — secrets store karna | Secret file |
| **.gitignore** | Files Git should ignore — secrets, temp files | Git ko ignore karne wali files |
| **Mock Data** | Fake data for testing — bina real API ke demo | Nakli data testing ke liye |
| **Sandbox** | Isolated testing environment | Alag testing jagah |
| **Rate Limiting** | Limit API calls per time — abuse rokna | API calls ki seema |
| **Latency** | Delay — kitna time lagta hai response aane mein | Deri |
| **Uptime** | Time server is running — 99.9% = almost always on | Server chalne ka samay |
| **Downtime** | Time server is down — maintenance ya crash | Server band hone ka samay |
| **SLA** | Service Level Agreement — guaranteed uptime | Seva ki guarantee |
| **Backup** | Data copy — agar data loss ho toh recover karna | Data ki suraksha copy |
| **Restore** | Recover from backup | Backup se wapas lana |
| **Firewall** | Network security — unauthorized access rokna | Network ki suraksha |
| **Encryption** | Data coding — sirf authorized log padh sakte hain | Data ko coding karna |
| **Decryption** | Reverse encryption — coded data padhna | Coded data padhna |
| **Token** | Authentication key — access ke liye | Access ki chabhi |
| **JWT** | JSON Web Token — secure authentication | Surakshit authentication |
| **OAuth** | Open Authorization — third-party login | Doosre se login |
| **Webhook** | Server push notification (repeated for clarity) | Server se turant khabar |
| **Polling** | Periodic checking — har X second pe check karna | Baar baar check karna |
| **Streaming** | Real-time data flow — continuous data aata hai | Lagatar data aana |
| **Dashboard** | Visual data display — charts, graphs, maps | Data ka visual display |
| **Widget** | Small UI component — button, card, chart | Chhota UI hissa |
| **Responsive** | Works on all screen sizes — desktop, tablet, mobile | Har screen pe chalna |
| **Viewport** | Screen size — desktop = wide, mobile = narrow | Screen ka size |
| **CSS** | Styling language — website ka design | Website ka design |
| **HTML** | Structure language — website ka structure | Website ka structure |
| **JavaScript** | Programming language — website ka behavior | Website ka behavior |
| **DOM** | Document Object Model — HTML ka tree structure | HTML ka ped |
| **Async** | Non-blocking — ek kaam karte hue doosra bhi ho raha hai | Ek saath kaam karna |
| **Await** | Wait for async result — jab tak result na aaye wait karo | Result ka intezaar karna |
| **Callback** | Function called after task complete — jab kaam ho toh ye karo | Kaam ke baad ye karo |
| **Promise** | Async result container — result baad mein aayega | Result ka wada |
| **Middleware** | Code that runs between request and response | Request aur response ke beech ka code |
| **Endpoint** | API URL — jahan request jaati hai | API ka pata |
| **Route** | URL pattern — kaun sa URL kaun sa code chalata hai | URL ka pattern |
| **Handler** | Function that processes request — request ko handle karna | Request ko sambhalna |
| **Payload** | Data sent in request/response | Bheja gaya data |
| **Header** | Request metadata — auth token, content type | Request ki jaankaari |
| **Body** | Request data — actual content | Request ka data |
| **Status Code** | HTTP response code — 200 = OK, 404 = Not Found, 500 = Error | Response ka code |
| **200 OK** | Success — request kaam kar gayi | Safalta |
| **404 Not Found** | Resource nahi mila | Nahi mila |
| **500 Internal Server Error** | Server mein error | Server mein galti |
| **401 Unauthorized** | Authentication required | Login zaroori |
| **403 Forbidden** | Access denied | Anumati nahi |
| **429 Too Many Requests** | Rate limit exceeded | Bahut zyada requests |
