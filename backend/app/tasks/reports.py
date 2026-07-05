"""
Report generation tasks.
"""

import structlog
from datetime import datetime, timedelta
from app.tasks.celery_app import celery_app
from app.services.samsara import SamsaraService
from app.services.telegram import TelegramService
from app.core.database import async_session, AuditLog, Escalation

logger = structlog.get_logger()


@celery_app.task(name="app.tasks.reports.daily_summary")
def daily_summary():
    """Generate and send daily fleet summary."""
    import asyncio
    asyncio.run(_daily_summary())


async def _daily_summary():
    """Async implementation of daily summary."""
    samsara = SamsaraService()
    telegram = TelegramService()

    try:
        # Gather fleet data
        overview = await samsara.get_fleet_overview()
        hos_data = await samsara.get_hos_status()
        faults = await samsara.get_fleet_faults(status="active")

        # Get pending escalations
        async with async_session() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(Escalation).where(Escalation.status == "pending")
            )
            pending_escalations = result.scalars().all()

        # Build summary
        summary = {
            "total_vehicles": overview.get("total_vehicles", 0),
            "active_vehicles": overview.get("active_vehicles", 0),
            "total_miles": overview.get("total_miles_today", 0),
            "total_fuel": overview.get("total_fuel_today", 0),
            "critical_incidents": sum(1 for f in faults if f.get("severity") == "critical"),
            "high_incidents": sum(1 for f in faults if f.get("severity") == "warning"),
            "medium_incidents": 0,
            "pending_approvals": len(pending_escalations),
            "overdue_maintenance": overview.get("overdue_maintenance", 0),
            "recommendations": [],
        }

        # Add recommendations
        if summary["critical_incidents"] > 0:
            summary["recommendations"].append(
                f"Address {summary['critical_incidents']} critical fault codes immediately"
            )
        if summary["pending_approvals"] > 0:
            summary["recommendations"].append(
                f"Review {summary['pending_approvals']} pending approval requests"
            )
        if summary["overdue_maintenance"] > 0:
            summary["recommendations"].append(
                f"Schedule {summary['overdue_maintenance']} overdue maintenance items"
            )

        # Send summary
        await telegram.send_daily_summary(summary)

        logger.info("Daily summary sent", summary=summary)

        await _log_audit(
            action_type="daily_summary",
            description="Daily fleet summary generated and sent",
            details=summary,
        )

    except Exception as e:
        logger.error("Failed to generate daily summary", error=str(e))


async def _log_audit(action_type: str, description: str, details: dict = None):
    """Log to audit trail."""
    async with async_session() as session:
        audit = AuditLog(
            action_type=action_type,
            description=description,
            details=details,
        )
        session.add(audit)
        await session.commit()
