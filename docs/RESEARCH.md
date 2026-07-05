# Fleet-Ryan Research Document

> Deep research on Ryan Scharnowske, Orbital Installation Technologies, fleet management AI, and competitive landscape.

---

## 1. Ryan Scharnowske — Client Profile

### Background
- **Name:** Ryan Scharnowske
- **Role:** COO, Orbital Installation Technologies, LLC
- **Location:** 9750 E 150th St UNIT 1200, Noblesville, IN 46060, USA
- **Phone:** (317) 774-3668
- **Email:** ryan@orbitalinstalls.com
- **LinkedIn:** linkedin.com/in/ryan-scharnowske-6051412

### Upwork History
- **Member since:** July 2016
- **Total spent:** $551K+
- **Jobs posted:** 42
- **Hire rate:** 100%
- **Average rate paid:** $48.15/hr
- **Client name on Upwork:** "Ryan" (confirmed as Ryan Scharnowske)

### Past Upwork Hires
- WordPress development
- DevOps engineering
- QA testing
- T-shirt design
- PPC advertising (Choice Window Tint)
- Various technical roles

### Key Insight
Ryan is a **proven Upwork client** who has spent over $500K on freelancers. He has a 100% hire rate and pays well ($48/hr average). This is NOT a first-time client — he knows how to evaluate and work with freelancers.

---

## 2. Orbital Installation Technologies

### Company Profile
- **Founded:** 2006 (20+ years in business)
- **Type:** LLC
- **Core Business:** Nationwide fleet technology installation
- **Team:** W2 technicians (not subcontractors)
- **Coverage:** 80+ regional hubs across US
- **Installs completed:** 1M+

### Services
- GPS fleet tracking system installation
- In-vehicle cameras / dashcam installation
- AI camera systems
- Mobile WiFi systems
- RFID systems
- IoT device installation
- Telematics hardware

### Clients
- Fleet operators
- Telematics vendors
- Logistics companies
- Transportation companies

### Platform
- **TaskRaptor** — Own cloud-native platform for:
  - Scheduling
  - Quality assurance
  - Inventory management
  - Integrations

### Key Insight
Orbital is a **hardware installation services company**. They install fleet technology but don't manage fleets. Ryan wants to **move up the value chain** — from "we install the hardware" to "our AI manages your fleet."

---

## 3. Ryan's Blog — "Agentic AI Is Coming for Fleet Management"

### Published: June 24, 2026
### Author: Ryan Scharnowske
### Link: orbitalinstalls.com/blog/agentic-ai-is-coming-for-fleet-management-is-your-hardware-ready/

### Key Arguments

#### The Evolution of Fleet Telematics
1. **Traditional telematics** → Tells you what happened (vehicle location, speed history)
2. **Predictive telematics** → Forecasts what will happen (engine fault before warning light)
3. **Agentic AI** → Surfaces info AND acts on it (schedules maintenance, reroutes drivers, generates compliance docs)

#### The Hardware Layer Is Critical
- Every data point originates at a physical device
- If 15% of fleet has installation-related GPS drift → AI models learn wrong patterns
- Agentic systems amplify hardware quality issues: if AI acts without human review, hardware data quality = decision quality

#### 5 Questions Fleet Operators Should Ask
1. Is your installation partner device-certified on specific hardware?
2. Do you have photo-validated baseline for every vehicle?
3. Can they scale nationally without sacrificing consistency?
4. What happens when hardware fails after a year?
5. Who's actually doing the work (W2 vs subcontractors)?

#### Future Vision
- Vehicle-to-infrastructure communication
- Multi-sensor fusion (GPS + camera + engine + environmental)
- Edge AI running on-device inference

### Key Insight
Ryan has **deep domain expertise** in fleet hardware. He understands that AI is only as good as the data, and data is only as good as the hardware installation. This blog post is essentially his **product vision statement** for the AI fleet management service he wants to build.

---

## 4. Upwork Job Analysis

### Job Title
"Senior Python Developer Needed for Autonomous AI Agent / Claw-Style Workflow System"

### Posted: ~July 2-3, 2026

### What Ryan Wants
An **autonomous claw-style agent** that:
1. Monitors a process over time (not one-off tasks)
2. Notices when something changes (event-driven)
3. Knows what actions it is allowed to take (permission boundaries)
4. Can use APIs/tools safely (controlled tool execution)
5. Maintains state and context (persistent memory)
6. Logs what it did and why (full audit trail)
7. Escalates to human when confidence is low or approval required (HITL)
8. Can recover from failures or retry safely (resilience)

### What Ryan Does NOT Want
- Basic chatbots
- No-code AI tools
- Tutorial copiers
- People who can't explain architecture
- No Claw/OpenClaw experience
- Simple prompt chains
- Ignoring reliability, permissions, logging, failure handling

### Required Skills
- Strong Python development
- Real experience with autonomous AI agents
- **Claw / OpenClaw / NemoClaw-style agent experience — ABSOLUTELY REQUIRED**
- Agent loops, tools, state, memory, planning, monitoring, escalation, guardrails
- Production-grade AI workflows
- API integration, backend engineering
- Reliability, logging, permissions, audit trails, failure handling, HITL

### Helpful Skills
- LangGraph
- OpenAI / Anthropic APIs
- Multi-agent systems
- FastAPI, PostgreSQL
- AWS / cloud infrastructure
- Event-driven systems, background jobs, queues
- Permissioned tool execution, human approval workflows
- Security-conscious agent design

### Screening Process
- Live phone/video technical screening
- Must explain: what you built, agent architecture, state monitoring, tool triggering, failure handling, human escalation, unsafe action prevention

### Key Insight
Ryan is **very specific** about what he wants. He's not looking for a general Python developer — he wants someone with **real OpenClaw experience** who can build production-grade autonomous agents. The screening process shows he'll test your knowledge deeply.

---

## 5. Blog ↔ Job Connection

| Blog Concept | Job Requirement |
|---|---|
| "Fleets that self-optimize" | Agent that monitors processes over time |
| "Schedule maintenance automatically" | Agent that triggers actions via tools/APIs |
| "Reroute drivers mid-run" | Agent that notices changes and acts |
| "Generate compliance docs, flag for review" | Agent that logs what it did, escalates to human |
| "Without waiting for human at every step" | Agent with guardrails, knows allowed actions |
| "Data quality = decision quality" | Reliability, logging, audit trails |
| "Hardware layer" | API integration with fleet hardware systems |

**Conclusion:** The blog post is the **vision**, the Upwork job is the **execution plan**. Ryan wants to build the AI brain that connects to Orbital's existing fleet hardware installation business.

---

## 6. Fleet Management API Landscape

### Samsara (Priority 1)
- **Website:** samsara.com
- **API Docs:** developers.samsara.com
- **Market Position:** Leader in fleet telematics
- **API Features:**
  - REST API with OAuth 2.0
  - Webhooks for real-time events
  - Vehicle stats, locations, fault codes
  - HOS compliance, DVIR
  - Routing and dispatch
  - Fuel card integration
  - Kafka streaming for high-volume data
- **Webhook Events:**
  - AlertIncident (safety alerts)
  - EngineFaultOn/Off (DTC codes)
  - DvirSubmitted (inspection reports)
  - GeofenceEntry/Exit
  - SpeedingEventStarted/Ended
  - VehicleCreated/Updated
- **Rate Limits:** 5 requests/second (300/minute)

### Motive (KeepTruckin') (Priority 2)
- **Website:** gomotive.com
- **API Docs:** developer.gomotive.com
- **Market Position:** 120K+ fleets, strong compliance
- **API Features:**
  - REST API with API key auth
  - Users, vehicles, HOS logs
  - DVIR reports, IFTA reports
  - Fault codes, driver performance
  - Webhooks
- **Key Strength:** Compliance-focused (HOS, ELD, DVIR)

### Geotab (Priority 3)
- **Website:** geotab.com
- **API Docs:** geotab.github.io/sdk
- **Market Position:** #1 globally by installed devices
- **API Features:**
  - MyGeotab SDK
  - Telematics data
  - Engine diagnostics
  - Custom data feeds

### Fleetio (Priority 4 — Maintenance)
- **Website:** fleetio.com
- **API Docs:** fleetio.com/api
- **Focus:** Maintenance management
- **API Features:**
  - Vehicles, work orders
  - Service entries, fuel entries
  - Parts inventory
  - Cost tracking

---

## 7. Competitive Landscape

### AI Fleet Management Players

| Company | Focus | Stage |
|---------|-------|-------|
| **Motive** | AI dashcam + fleet management | Established, $2.8B valuation |
| **Samsara** | IoT + fleet telematics | Public company (IOT) |
| **Geotab** | Data-driven fleet management | #1 by installed base |
| **Nauto** | AI driver safety | Series C |
| **Lytx** | Video telematics + AI | Established |
| **Azuga** | Fleet tracking + maintenance | Acquired by Bridgestone |

### Ryan's Differentiator
Orbital is NOT trying to compete with Samsara/Motive. Instead:
- Orbital **installs** the hardware (existing business)
- Orbital's AI **manages** the fleet using that hardware (new business)
- The AI layer sits **on top of** existing fleet platforms
- It's an **integration and intelligence layer**, not a replacement

---

## 8. OpenClaw Framework Analysis

### What Is OpenClaw?
- Open-source framework for running AI agents autonomously
- Think of it as the "operating system" for your AI workforce
- GitHub: github.com/openclaw/openclaw
- Built on Node.js

### Key Architecture Concepts

#### Gateway
- Single long-lived daemon
- Owns all messaging surfaces (Telegram, WhatsApp, Discord, etc.)
- Exposes WebSocket API for control
- Default port: 18789

#### Agent Workspace
- Plain text files define the agent
- SOUL.md — Personality and boundaries
- AGENTS.md — Operating procedures
- HEARTBEAT.md — Periodic tasks
- MEMORY.md — Long-term knowledge
- Skills/ — Skill definitions

#### Heartbeat Pattern
- Agent wakes up periodically (configurable interval)
- Reads HEARTBEAT.md for tasks
- Executes tasks (API calls, monitoring, etc.)
- Reports results or HEARTBEAT_OK if nothing notable
- Perfect for continuous fleet monitoring

#### Skills
- Modular capability definitions
- SKILL.md defines what the skill does
- Can include code, configs, prompts
- Workspace skills override bundled skills

#### Channels
- 20+ messaging channels supported
- Telegram (primary for fleet)
- WhatsApp, Discord, Slack, Signal, etc.
- Each channel has its own configuration

### Why OpenClaw for Fleet?
| Feature | Fleet Need | OpenClaw Solution |
|---------|-----------|-------------------|
| Always-on monitoring | 24/7 fleet watch | Heartbeat pattern |
| Multi-channel alerts | Telegram + email | 20+ channels |
| Persistent memory | Fleet knowledge | MEMORY.md + daily logs |
| Skill modularity | Fleet-specific tools | Skills system |
| Audit trail | Compliance logging | Agent logging |
| Human escalation | Approval workflows | HITL patterns |

---

## 9. Key Success Factors

### For Winning the Job
1. **Demonstrate real OpenClaw experience** — Not tutorials, real production use
2. **Show production thinking** — Error handling, logging, guardrails, HITL
3. **Connect to Ryan's vision** — Show you read his blog, understand his goals
4. **Deliver a working prototype** — Not just a proposal, actual code
5. **Price competitively** — $55-70/hr is the sweet spot

### For Project Success
1. **Start with Samsara** — Most likely platform Orbital uses
2. **Heartbeat-first design** — Continuous monitoring is the core value
3. **Strict guardrails** — Never auto-act on expensive/risky operations
4. **Full audit trail** — Every action logged with reason
5. **Telegram as primary channel** — Quick alerts, mobile-friendly approvals
