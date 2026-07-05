# Fleet Maintenance Skill

> Predictive and preventive maintenance management for fleet vehicles.

## What This Skill Does

Tracks maintenance needs, predicts failures from fault code patterns, schedules service, and manages work orders.

## Commands

### Maintenance Status
```
"Which vehicles need oil change?"
"Show me maintenance due this week"
"What's the maintenance backlog?"
```

### Fault Code Analysis
```
"Any engine fault patterns across fleet?"
"What does fault code P0340 mean?"
"Show vehicles with recurring faults"
```

### Scheduling
```
"Schedule maintenance for Truck #842"
"When is the next PM due for Vehicle #567?"
"Show me available service slots"
```

### Cost Tracking
```
"What's our maintenance spend this month?"
"Average cost per vehicle?"
"Show me most expensive repairs"
```

## Common Fault Codes

### Engine (P-codes)
| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| P0300 | Random/Multiple Cylinder Misfire | High | Schedule service |
| P0340 | Camshaft Position Sensor | Critical | Immediate service |
| P0401 | EGR Flow Insufficient | Medium | Schedule service |
| P0420 | Catalyst System Efficiency | Low | Monitor |
| P0500 | Vehicle Speed Sensor | High | Schedule service |

### Transmission (P-codes)
| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| P0700 | Transmission Control System | Critical | Immediate service |
| P0715 | Input/Turbine Speed Sensor | High | Schedule service |
| P0730 | Incorrect Gear Ratio | Critical | Immediate service |

### Brakes (C-codes)
| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| C0035 | Left Front Wheel Speed Sensor | High | Schedule service |
| C0040 | Right Front Wheel Speed Sensor | High | Schedule service |
| C0050 | Rear Wheel Speed Sensor | High | Schedule service |

## Maintenance Intervals

### Preventive Maintenance (PM) Schedule
| Service | Interval | Mileage |
|---------|----------|---------|
| Oil Change | 6 months | 25,000 mi |
| Tire Rotation | 6 months | 25,000 mi |
| Brake Inspection | 12 months | 50,000 mi |
| Transmission Service | 24 months | 100,000 mi |
| Coolant Flush | 24 months | 100,000 mi |
| DPF Cleaning | 12 months | 50,000 mi |

## API Integration

### Samsara Endpoints
- `GET /v1/faults` — Fault code data
- `GET /v1/maintenance` — Maintenance schedules
- `POST /v1/maintenance/schedule` — Schedule maintenance

### Fleetio Endpoints
- `GET /work_orders` — Work order list
- `POST /work_orders` — Create work order
- `GET /service_entries` — Service history
- `GET /parts` — Parts inventory

## Output Format

### Maintenance Alert
```
🔧 MAINTENANCE REQUIRED: Truck #842
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Issue: Fault code P0340 (Camshaft Position Sensor)
Mileage: 125,430 mi
Last Service: 118,200 mi (7,230 mi ago)
Severity: 🔴 Critical
Estimated Cost: $350-500
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended: Schedule immediate service
Nearest Service: Love's Travel Stop, I-65 Exit 103
Approve maintenance? [Yes] [No] [Schedule Later]
```

### Weekly Maintenance Report
```
📋 Maintenance Report — Week of July 1-7, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: 12 work orders
In Progress: 3
Scheduled: 8
Overdue: 1 (Truck #567 — oil change 500mi overdue)

Total Cost: $4,280
Average per Vehicle: $82.31

Top Issues:
1. Brake adjustments (4 vehicles)
2. Oil changes (3 vehicles)
3. Tire replacements (2 vehicles)

Upcoming Next Week:
- 5 vehicles due for PM
- 2 vehicles with active fault codes
```

## Predictive Maintenance Logic

### Pattern Detection
- Same fault code 3+ times in 30 days → Recommend component replacement
- Increasing fault frequency → Escalate severity
- Mileage approaching PM threshold → Schedule proactively
- Engine hours vs. mileage mismatch → Investigate usage patterns

### Cost Optimization
- Group maintenance by location when possible
- Track parts inventory for common repairs
- Identify vehicles with highest maintenance costs (replacement candidates)
