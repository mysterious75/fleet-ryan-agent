# Fleet Compliance Skill

> Monitor Hours of Service (HOS), DVIR status, IFTA reporting, and CSA scores.

## What This Skill Does

Tracks regulatory compliance across the fleet, monitors HOS limits, DVIR submissions, and generates compliance reports.

## Commands

### HOS Monitoring
```
"Any HOS violations today?"
"Which drivers are near their 11-hour limit?"
"Show me drivers who need a break soon"
```

### DVIR Status
```
"Any DVIRs not submitted today?"
"Show incomplete DVIRs"
"Which vehicles failed inspection?"
```

### IFTA Reporting
```
"What's our IFTA status this quarter?"
"Show mileage by state for last month"
"Any IFTA anomalies?"
```

### CSA Scores
```
"What's our CSA score?"
"Show recent violations"
"Any unsafe driving alerts?"
```

## Regulatory Context

### HOS Rules (US)
- **11-Hour Driving Limit:** Max 11 hours driving after 10 consecutive hours off duty
- **14-Hour Window:** Cannot drive beyond 14th consecutive hour after coming on duty
- **30-Minute Break:** Must take 30-minute break after 8 cumulative hours driving
- **60/70-Hour Limit:** Cannot drive after 60/70 hours on duty in 7/8 consecutive days

### DVIR Requirements
- Pre-trip and post-trip inspections required
- Must be submitted before next dispatch
- Defects must be corrected before next trip

### IFTA (International Fuel Tax Agreement)
- Quarterly fuel tax reporting
- Mileage tracking by state/jurisdiction
- Fuel purchase documentation required

## API Integration

### Samsara Endpoints
- `GET /v1/fleet/drivers/{id}/hos` — Driver HOS status
- `GET /v1/fleet/drivers/{id}/hos_logs` — HOS log history
- `GET /v1/fleet/drivers` — Driver list with HOS summary
- `GET /v1/compliance/dvir` — DVIR reports

### Motive Endpoints
- `GET /drivers/{id}/hos_logs` — HOS logs
- `GET /drivers/{id}/daily_logs` — Daily log summaries
- `GET /inspection_reports` — DVIR reports

## Output Format

### HOS Alert
```
⚠️ HOS WARNING: Driver Mike Johnson (Truck #842)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Driving Time: 10h 15m (limit: 11h)
On-Duty Window: 13h 30m (limit: 14h)
Break Required: Yes (30 min after 8h driving)
Status: ⚠️ Approaching limit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommendation: Plan rest stop within 45 minutes
```

### DVIR Summary
```
📋 DVIR Status — July 5, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submitted Today: 38
Pending: 8
Overdue: 2
Failed (Defects): 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 2 vehicles with overdue DVIRs — cannot dispatch until resolved
```

## Escalation Rules
- HOS violation in progress → CRITICAL → Immediate alert
- DVIR overdue > 2 hours → HIGH → Alert within 30 min
- IFTA anomaly → MEDIUM → Include in daily report
- CSA score decrease → MEDIUM → Weekly review
