# Fleet Escalation Skill

> Human-in-the-loop (HITL) escalation system for fleet operations.

## What This Skill Does

Manages the escalation workflow when the agent needs human approval or when critical issues require immediate attention.

## Escalation Levels

### 🔴 CRITICAL — Immediate Human Alert
**Trigger:** Safety risk, legal compliance, financial impact > $1000
**Response:** Immediate Telegram alert + SMS if available
**Timeout:** 15 minutes, then re-escalate
**Examples:**
- Engine fault affecting drivability
- Crash detected
- HOS violation in progress
- Fuel theft confirmed
- Vehicle breakdown on highway

### 🟠 HIGH — Alert Within 30 Minutes
**Trigger:** Operational impact, compliance risk, financial impact $100-1000
**Response:** Telegram alert with approval buttons
**Timeout:** 1 hour, then include in next heartbeat
**Examples:**
- DVIR overdue
- Maintenance >500mi overdue
- Fuel anomaly (unconfirmed)
- Driver approaching HOS limit

### 🟡 MEDIUM — Next Heartbeat Report
**Trigger:** Minor issues, approaching thresholds
**Response:** Include in heartbeat report
**Timeout:** 24 hours
**Examples:**
- Mileage approaching PM threshold
- Minor fault code
- Idling >1 hour
- Route efficiency suggestion

### 🟢 LOW — Daily Summary
**Trigger:** Informational, optimization opportunities
**Response:** Include in daily summary
**Timeout:** None
**Examples:**
- Fuel efficiency trend
- Maintenance schedule reminder
- Compliance status update

## Escalation Workflow

```
Issue Detected
    │
    ▼
Classify Severity
    │
    ├── Critical ──► Immediate Telegram Alert
    │                    │
    │                    ▼
    │               Wait for Response (15 min)
    │                    │
    │                    ├── Approved → Execute + Log
    │                    ├── Rejected → Log + Note
    │                    └── Timeout → Re-escalate (SMS/Call)
    │
    ├── High ──────► Telegram Alert with Buttons
    │                    │
    │                    ▼
    │               Wait for Response (1 hour)
    │                    │
    │                    ├── Approved → Execute + Log
    │                    ├── Rejected → Log + Note
    │                    └── Timeout → Include in next heartbeat
    │
    ├── Medium ────► Include in Heartbeat Report
    │                    │
    │                    ▼
    │               Human reviews in daily flow
    │
    └── Low ───────► Include in Daily Summary
```

## Telegram Alert Format

### Critical Alert
```
🚨 CRITICAL FLEET ALERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vehicle: Truck #842
Issue: Engine fault P0340 (Camshaft Position Sensor)
Location: I-65 MM 203, Indianapolis, IN
Driver: Mike Johnson
Time: 2:30 PM EST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ IMMEDIATE ACTION REQUIRED

Options:
1. 🛑 Stop vehicle at next safe location
2. 🔧 Route to nearest service station
3. 📞 Contact driver directly

Which action? Reply with 1, 2, or 3
```

### Approval Request
```
🔧 MAINTENANCE APPROVAL REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vehicle: Truck #842
Issue: Oil change overdue (500mi)
Current Mileage: 125,430 mi
Last Service: 118,200 mi
Estimated Cost: TBD
Location: Indianapolis Terminal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Approve maintenance? [Yes] [No] [Schedule Later]
```

## Approval Button Configuration

### Telegram Inline Buttons
```json
{
  "inline_keyboard": [
    [
      {"text": "✅ Approve", "callback_data": "approve:{escalation_id}"},
      {"text": "❌ Reject", "callback_data": "reject:{escalation_id}"}
    ],
    [
      {"text": "⏰ Schedule Later", "callback_data": "defer:{escalation_id}"},
      {"text": "📞 Call Me", "callback_data": "call:{escalation_id}"}
    ]
  ]
}
```

## Escalation Rules Configuration

All escalation rules are defined in `data/escalation-rules.yaml`:

```yaml
rules:
  - name: "engine_fault_critical"
    condition: "fault_code.severity == 'critical' AND fault_code.system in ['engine', 'brake', 'transmission']"
    severity: "critical"
    action: "immediate_alert"
    timeout_minutes: 15

  - name: "hos_violation"
    condition: "driver.hos_remaining < 30"
    severity: "critical"
    action: "immediate_alert"
    timeout_minutes: 15

  - name: "dvir_overdue"
    condition: "vehicle.last_dvir_age > 2h"
    severity: "high"
    action: "alert_with_approval"
    timeout_minutes: 60
```

## Audit Trail

Every escalation is logged:
```json
{
  "escalation_id": "esc_20260705_143000_842",
  "timestamp": "2026-07-05T14:30:00Z",
  "vehicle_id": "842",
  "severity": "critical",
  "issue": "Engine fault P0340",
  "action_taken": "immediate_alert",
  "human_response": "approved",
  "human_response_time": "2026-07-05T14:32:00Z",
  "resolution": "Routed to Love's Travel Stop for service",
  "cost": null
}
```
