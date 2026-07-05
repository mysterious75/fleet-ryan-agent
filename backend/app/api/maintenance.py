"""
Maintenance management API routes.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import structlog

from app.services.samsara import SamsaraService
from app.services.fleetio import FleetioService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/schedule")
async def get_maintenance_schedule(
    vehicle_id: Optional[str] = Query(None, description="Filter by vehicle ID"),
    days: int = Query(7, description="Days ahead to look"),
):
    """Get upcoming maintenance schedule."""
    try:
        samsara = SamsaraService()
        schedule = await samsara.get_maintenance_schedule(
            vehicle_id=vehicle_id, days_ahead=days
        )
        return {
            "schedule": schedule,
            "total": len(schedule),
            "overdue": sum(1 for m in schedule if m.get("overdue")),
            "due_soon": sum(1 for m in schedule if m.get("due_soon")),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get maintenance schedule", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch maintenance schedule")


@router.get("/faults")
async def get_fault_codes(
    vehicle_id: Optional[str] = Query(None, description="Filter by vehicle ID"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: str = Query("active", description="Filter by status (active, resolved, all)"),
):
    """Get fleet-wide fault codes."""
    try:
        samsara = SamsaraService()
        faults = await samsara.get_fleet_faults(
            vehicle_id=vehicle_id, severity=severity, status=status
        )
        return {
            "faults": faults,
            "total": len(faults),
            "critical": sum(1 for f in faults if f.get("severity") == "critical"),
            "warning": sum(1 for f in faults if f.get("severity") == "warning"),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get fault codes", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch fault codes")


@router.get("/faults/patterns")
async def get_fault_patterns(
    days: int = Query(30, description="Days to analyze"),
):
    """Get fault code patterns and trends."""
    try:
        samsara = SamsaraService()
        patterns = await samsara.get_fault_patterns(days=days)
        return {
            "patterns": patterns,
            "total": len(patterns),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get fault patterns", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch fault patterns")


@router.post("/schedule/{vehicle_id}")
async def schedule_maintenance(
    vehicle_id: str,
    service_type: str = Query(..., description="Type of service"),
    notes: Optional[str] = Query(None, description="Additional notes"),
):
    """Schedule maintenance for a vehicle (requires approval)."""
    # This endpoint creates an escalation for human approval
    try:
        from app.api.escalation import create_escalation

        escalation = await create_escalation(
            vehicle_id=vehicle_id,
            severity="high",
            issue_type="maintenance_request",
            description=f"Maintenance requested: {service_type}",
            details={"service_type": service_type, "notes": notes},
            recommended_action=f"Schedule {service_type} for vehicle {vehicle_id}",
        )
        return {
            "message": "Maintenance request submitted for approval",
            "escalation_id": escalation["escalation_id"],
            "status": "pending_approval",
        }
    except Exception as e:
        logger.error("Failed to schedule maintenance", vehicle_id=vehicle_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to schedule maintenance")


@router.get("/costs")
async def get_maintenance_costs(
    vehicle_id: Optional[str] = Query(None, description="Filter by vehicle ID"),
    days: int = Query(30, description="Days to look back"),
):
    """Get maintenance cost data."""
    try:
        fleetio = FleetioService()
        costs = await fleetio.get_maintenance_costs(
            vehicle_id=vehicle_id, days=days
        )
        return {
            "entries": costs.get("entries", []),
            "total_cost": costs.get("total_cost", 0),
            "average_per_vehicle": costs.get("average_per_vehicle", 0),
            "vehicle_count": costs.get("vehicle_count", 0),
            "entry_count": costs.get("entry_count", 0),
            "period_days": costs.get("period_days", days),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get maintenance costs", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch maintenance costs")
