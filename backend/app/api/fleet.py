"""
Fleet management API routes.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime
import structlog

from app.services.samsara import SamsaraService
from app.models.schemas import (
    VehicleResponse,
    VehicleListResponse,
    VehicleStatsResponse,
    FleetOverviewResponse,
)

logger = structlog.get_logger()
router = APIRouter()


@router.get("/vehicles", response_model=VehicleListResponse)
async def list_vehicles(
    group_id: Optional[str] = Query(None, description="Filter by vehicle group"),
    status: Optional[str] = Query(None, description="Filter by status (active, inactive, maintenance)"),
):
    """List all fleet vehicles with optional filters."""
    try:
        samsara = SamsaraService()
        vehicles = await samsara.get_vehicles(group_id=group_id, status=status)
        return VehicleListResponse(
            vehicles=vehicles,
            total=len(vehicles),
            timestamp=datetime.utcnow(),
        )
    except Exception as e:
        logger.error("Failed to list vehicles", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch vehicles")


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: str):
    """Get details for a specific vehicle."""
    try:
        samsara = SamsaraService()
        vehicle = await samsara.get_vehicle(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found")
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get vehicle", vehicle_id=vehicle_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch vehicle")


@router.get("/vehicles/{vehicle_id}/stats", response_model=VehicleStatsResponse)
async def get_vehicle_stats(vehicle_id: str):
    """Get real-time stats for a vehicle (location, speed, fuel, etc.)."""
    try:
        samsara = SamsaraService()
        stats = await samsara.get_vehicle_stats(vehicle_id)
        if not stats:
            raise HTTPException(status_code=404, detail=f"Stats not found for vehicle {vehicle_id}")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get vehicle stats", vehicle_id=vehicle_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch vehicle stats")


@router.get("/overview", response_model=FleetOverviewResponse)
async def fleet_overview():
    """Get fleet-wide overview and statistics."""
    try:
        samsara = SamsaraService()
        overview = await samsara.get_fleet_overview()
        return overview
    except Exception as e:
        logger.error("Failed to get fleet overview", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch fleet overview")


@router.get("/vehicles/{vehicle_id}/faults")
async def get_vehicle_faults(vehicle_id: str):
    """Get active fault codes for a vehicle."""
    try:
        samsara = SamsaraService()
        faults = await samsara.get_vehicle_faults(vehicle_id)
        return {
            "vehicle_id": vehicle_id,
            "faults": faults,
            "total": len(faults),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get vehicle faults", vehicle_id=vehicle_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch fault codes")


@router.get("/search")
async def search_vehicles(
    q: str = Query(..., description="Search query (vehicle name, ID, location)"),
):
    """Search vehicles by name, ID, or location."""
    try:
        samsara = SamsaraService()
        results = await samsara.search_vehicles(q)
        return {
            "query": q,
            "results": results,
            "total": len(results),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to search vehicles", query=q, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search vehicles")
