"""
Compliance monitoring API routes.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import structlog

from app.services.samsara import SamsaraService
from app.models.schemas import HOSStatusResponse, DVIRStatusResponse

logger = structlog.get_logger()
router = APIRouter()


@router.get("/hos")
async def get_hos_status(
    driver_id: Optional[str] = Query(None, description="Filter by driver ID"),
    near_limit: bool = Query(False, description="Only show drivers near HOS limit"),
):
    """Get Hours of Service status for drivers."""
    try:
        samsara = SamsaraService()
        hos_data = await samsara.get_hos_status(driver_id=driver_id, near_limit=near_limit)
        return {
            "drivers": hos_data,
            "total": len(hos_data),
            "near_limit_count": sum(1 for d in hos_data if d.get("near_limit")),
            "violations_count": sum(1 for d in hos_data if d.get("in_violation")),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get HOS status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch HOS status")


@router.get("/hos/violations")
async def get_hos_violations():
    """Get all current HOS violations."""
    try:
        samsara = SamsaraService()
        violations = await samsara.get_hos_violations()
        return {
            "violations": violations,
            "total": len(violations),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get HOS violations", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch HOS violations")


@router.get("/dvir")
async def get_dvir_status(
    status: Optional[str] = Query(None, description="Filter by status (submitted, pending, overdue)"),
):
    """Get DVIR (Driver Vehicle Inspection Report) status."""
    try:
        samsara = SamsaraService()
        dvir_data = await samsara.get_dvir_status(status=status)
        return {
            "dvirs": dvir_data,
            "total": len(dvir_data),
            "submitted": sum(1 for d in dvir_data if d.get("status") == "submitted"),
            "pending": sum(1 for d in dvir_data if d.get("status") == "pending"),
            "overdue": sum(1 for d in dvir_data if d.get("status") == "overdue"),
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get DVIR status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch DVIR status")


@router.get("/ifta")
async def get_ifta_status(
    quarter: Optional[str] = Query(None, description="Quarter (e.g., 2026-Q2)"),
):
    """Get IFTA (International Fuel Tax Agreement) status."""
    try:
        samsara = SamsaraService()
        ifta_data = await samsara.get_ifta_status(quarter=quarter)
        return {
            "ifta": ifta_data,
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get IFTA status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch IFTA status")


@router.get("/summary")
async def compliance_summary():
    """Get overall compliance summary."""
    try:
        samsara = SamsaraService()
        summary = await samsara.get_compliance_summary()
        return {
            "summary": summary,
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error("Failed to get compliance summary", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch compliance summary")
