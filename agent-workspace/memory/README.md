# FleetCommander Memory System

## How Memory Works

### Daily Memory Files (`memory/YYYY-MM-DD.md`)
- One file per day
- Raw logs of everything that happened
- Created automatically at start of each day
- Contains: alerts, actions, escalations, fleet status, lessons learned

### Long-Term Memory (`MEMORY.md`)
- Curated knowledge that persists across days
- Updated periodically from daily files
- Contains: fleet patterns, driver patterns, cost tracking, key contacts

### Memory Retention Policy
- **Daily files:** Keep for 30 days (configurable)
- **Weekly summary:** Generated every Monday, kept for 90 days
- **Monthly summary:** Generated 1st of month, kept for 1 year
- **MEMORY.md:** Permanent (curated, not raw logs)

## Memory Cleanup Schedule

### Weekly Cleanup (Every Monday at 02:00)
1. Archive daily files older than 7 days to `memory/archive/weekly/`
2. Generate weekly summary in `memory/weekly/YYYY-WXX.md`
3. Update MEMORY.md with important patterns from the week
4. Delete raw daily files older than 30 days

### Monthly Cleanup (1st of month at 02:00)
1. Archive weekly summaries older than 90 days to `memory/archive/monthly/`
2. Generate monthly summary in `memory/monthly/YYYY-MM.md`
3. Update MEMORY.md with monthly trends
4. Delete weekly summaries older than 90 days

## What Gets Logged

### Every Day
- All alerts sent (with severity and vehicle ID)
- All actions taken (with reason)
- All escalations (with outcome)
- Fleet status snapshots
- Anomalies detected
- API errors or issues
- Lessons learned

### Weekly Summary
- Total incidents by severity
- Top vehicles by fault count
- Fuel efficiency trends
- Maintenance cost summary
- Compliance score
- Key patterns identified

### Monthly Summary
- Fleet health trends
- Cost analysis (fuel, maintenance, downtime)
- Driver performance trends
- Compliance audit
- Recommendations for next month
