"""
Human-in-the-loop escalation API routes.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import structlog
import uuid

from app.core.database import AuditLog, Escalation, async_session
from app.services.telegram import TelegramService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/active")
async def get_active_escalations():
    """Get all pending escalations."""
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Escalation)
            .where(Escalation.status == "pending")
            .order_by(Escalation.timestamp.desc())
        )
        escalations = result.scalars().all()

    return {
        "escalations": [
            {
                "escalation_id": e.escalation_id,
                "timestamp": e.timestamp.isoformat(),
                "vehicle_id": e.vehicle_id,
                "severity": e.severity,
                "issue_type": e.issue_type,
                "description": e.description,
                "status": e.status,
                "recommended_action": e.recommended_action,
                "cost_estimate": e.cost_estimate,
            }
            for e in escalations
        ],
        "total": len(escalations),
    }


@router.post("/create")
async def create_escalation(
    vehicle_id: str,
    severity: str,
    issue_type: str,
    description: str,
    details: Optional[dict] = None,
    recommended_action: Optional[str] = None,
    cost_estimate: Optional[float] = None,
):
    """Create a new escalation request."""
    escalation_id = f"esc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{vehicle_id}"

    # Create escalation record
    async with async_session() as session:
        escalation = Escalation(
            escalation_id=escalation_id,
            vehicle_id=vehicle_id,
            severity=severity,
            issue_type=issue_type,
            description=description,
            details=details,
            recommended_action=recommended_action,
            cost_estimate=cost_estimate,
            status="pending",
            channel="telegram",
        )
        session.add(escalation)
        await session.commit()

    # Send to human via Telegram
    telegram = TelegramService()
    await telegram.send_escalation(
        escalation_id=escalation_id,
        vehicle_id=vehicle_id,
        severity=severity,
        description=description,
        recommended_action=recommended_action,
        cost_estimate=cost_estimate,
    )

    logger.info(
        "Escalation created",
        escalation_id=escalation_id,
        vehicle_id=vehicle_id,
        severity=severity,
    )

    return {
        "escalation_id": escalation_id,
        "status": "pending",
        "channel": "telegram",
    }


@router.post("/{escalation_id}/approve")
async def approve_escalation(
    escalation_id: str,
    responder: str = Query(..., description="Who approved"),
    notes: Optional[str] = Query(None, description="Approval notes"),
):
    """Approve an escalation."""
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Escalation).where(Escalation.escalation_id == escalation_id)
        )
        escalation = result.scalar_one_or_none()

        if not escalation:
            raise HTTPException(status_code=404, detail="Escalation not found")

        escalation.status = "approved"
        escalation.responded_at = datetime.utcnow()
        escalation.response_by = responder
        escalation.response_notes = notes
        await session.commit()

    # Log to audit trail
    await _log_audit(
        action_type="escalation_approved",
        severity=escalation.severity,
        vehicle_id=escalation.vehicle_id,
        description=f"Escalation {escalation_id} approved by {responder}",
        human_response="approved",
        human_responder=responder,
    )

    logger.info("Escalation approved", escalation_id=escalation_id, responder=responder)

    return {
        "escalation_id": escalation_id,
        "status": "approved",
        "responder": responder,
    }


@router.post("/{escalation_id}/reject")
async def reject_escalation(
    escalation_id: str,
    responder: str = Query(..., description="Who rejected"),
    reason: Optional[str] = Query(None, description="Rejection reason"),
):
    """Reject an escalation."""
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(Escalation).where(Escalation.escalation_id == escalation_id)
        )
        escalation = result.scalar_one_or_none()

        if not escalation:
            raise HTTPException(status_code=404, detail="Escalation not found")

        escalation.status = "rejected"
        escalation.responded_at = datetime.utcnow()
        escalation.response_by = responder
        escalation.response_notes = reason
        await session.commit()

    # Log to audit trail
    await _log_audit(
        action_type="escalation_rejected",
        severity=escalation.severity,
        vehicle_id=escalation.vehicle_id,
        description=f"Escalation {escalation_id} rejected by {responder}: {reason}",
        human_response="rejected",
        human_responder=responder,
    )

    logger.info("Escalation rejected", escalation_id=escalation_id, responder=responder)

    return {
        "escalation_id": escalation_id,
        "status": "rejected",
        "responder": responder,
    }


async def _log_audit(
    action_type: str,
    severity: str,
    vehicle_id: str,
    description: str,
    human_response: Optional[str] = None,
    human_responder: Optional[str] = None,
):
    """Log an action to the audit trail."""
    async with async_session() as session:
        audit = AuditLog(
            action_type=action_type,
            severity=severity,
            vehicle_id=vehicle_id,
            description=description,
            agent_decision="escalated",
            human_response=human_response,
            human_responder=human_responder,
        )
        session.add(audit)
        await session.commit()
