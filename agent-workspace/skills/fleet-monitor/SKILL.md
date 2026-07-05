# Fleet Monitor Skill

> Monitor fleet vehicles, locations, and status in real-time.

## What This Skill Does

Queries fleet platform APIs to provide real-time visibility into vehicle locations, status, and health.

## Commands

### Vehicle Location
```
"Where is Truck #842?"
"Show all vehicles in Chicago terminal"
"Which vehicles are on I-65 right now?"
```

### Vehicle Status
```
"What's the status of Truck #842?"
"Show all vehicles with active fault codes"
"Which vehicles are idling right now?"
```

### Fleet Overview
```
"How many vehicles are active today?"
"Give me a fleet health snapshot"
"Show me vehicles that haven't reported in 2 hours"
```

## API Integration

### Samsara Endpoints Used
- `GET /v1/fleet/vehicles` — List all vehicles
- `GET /v1/fleet/vehicles/stats` — Real-time stats (location, speed, fuel)
- `GET /v1/fleet/vehicles/{id}` — Single vehicle details
- `GET /v1/fleet/vehicles/{id}/stats` — Single vehicle stats

### Response Format
```json
{
  "vehicle_id": "842",
  "name": "Truck #842",
  "location": {
    "latitude": 39.7684,
    "longitude": -86.1581,
    "address": "Indianapolis, IN"
  },
  "speed": 65,
  "fuel_level": 72,
  "engine_status": "running",
  "odometer": 125430,
  "last_updated": "2026-07-05T14:30:00Z"
}
```

## Output Format

### Single Vehicle
```
🚛 Truck #842
━━━━━━━━━━━━━━━━━━━━━━
📍 Location: I-65 MM 203, Indianapolis, IN
⛽ Fuel: 72%
🔧 Engine: Running
📊 Speed: 65 mph
📏 Odometer: 125,430 mi
🕐 Last Updated: 2:30 PM EST
```

### Fleet Overview
```
📊 Fleet Status — July 5, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Vehicles: 52
Active (Moving): 38
Idling: 6
Parked: 5
Offline: 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Active Fault Codes: 4 vehicles
Overdue Maintenance: 2 vehicles
```

## Error Handling
- API timeout → Retry 3x → Report error to human
- Vehicle not found → Suggest similar vehicle IDs
- Rate limit hit → Queue request → Process in order

## Configuration
- API credentials: environment variables
- Vehicle groups: `data/fleet-config.yaml`
- Update frequency: heartbeat cycle (30 min)
