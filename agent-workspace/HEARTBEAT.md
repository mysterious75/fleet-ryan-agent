# HEARTBEAT.md — FleetCommander Monitoring Tasks

# This file defines what FleetCommander checks during each heartbeat cycle.
# Keep tasks focused and actionable. If nothing needs attention, reply HEARTBEAT_OK.

## Every 30 Minutes — Fault Code Check
Check for new Diagnostic Trouble Codes (DTCs) across fleet:
- If severity = CRITICAL (engine, brake, transmission): IMMEDIATE ALERT
- If severity = WARNING: note in next report
- If pattern repeats 3+ times: suggest maintenance schedule
- Log all fault codes to daily memory

## Every 1 Hour — Compliance Monitor
Check all active vehicles for:
1. HOS violations (drivers near 11hr driving limit)
2. DVIRs not submitted today
3. IFTA mileage anomalies
4. Vehicles with pending maintenance beyond threshold
Report any violations with vehicle ID, driver, and severity.

## Every 2 Hours — Fuel Anomaly Detection
Cross-reference fuel card transactions with telematics data:
1. Fuel purchases without corresponding mileage
2. Sudden fuel level drops (possible theft)
3. Excessive idling (>2hrs/day) per vehicle
Report anomalies with confidence score.

## Every 6 Hours — Fleet Health Snapshot
Generate fleet health snapshot:
1. Total active vehicles vs. total fleet
2. Vehicles with active fault codes
3. Compliance status summary
4. Upcoming maintenance (next 7 days)
5. Fuel efficiency trends
Save to memory for daily report.

## Every 24 Hours (08:00 local) — Daily Summary
Generate and send daily fleet summary to fleet manager:
1. Total active vehicles
2. Miles driven (24hr)
3. Fuel consumed
4. Incidents today (faults, violations, alerts)
5. Pending approvals
6. Recommended actions for tomorrow
7. Cost summary (maintenance, fuel)

## On Startup
1. Verify all required files exist (SOUL.md, AGENTS.md, fleet-config.yaml)
2. Test fleet API connectivity
3. Log startup timestamp
4. Run initial fleet health check

## Rules
- If nothing needs attention after all due tasks, reply HEARTBEAT_OK
- Never skip Critical severity items
- Batch Medium/Low items into reports, don't send individually
- Max 1 alert per vehicle per hour (prevent alert fatigue)
