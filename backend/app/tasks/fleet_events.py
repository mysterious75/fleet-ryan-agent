"""
Fleet event processing tasks (webhook events).
"""

import structlog
from datetime import datetime
from app.tasks.celery_app import celery_app
from app.services.telegram import TelegramService
from app.core.database import async_session, FaultCode, AuditLog

logger = structlog.get_logger()


@celery_app.task(name="app.tasks.fleet_events.process_fleet_event")
def process_fleet_event(platform: str, event_type: str, payload: dict):
    """Process a fleet platform webhook event."""
    import asyncio
    asyncio.run(_process_fleet_event(platform, event_type, payload))


async def _process_fleet_event(platform: str, event_type: str, payload: dict):
    """Async implementation of fleet event processing."""
    logger.info(
        "Processing fleet event",
        platform=platform,
        event_type=event_type,
    )

    try:
        if platform == "samsara":
            await _process_samsara_event(event_type, payload)
        elif platform == "motive":
            await _process_motive_event(event_type, payload)
        elif platform == "fleetio":
            await _process_fleetio_event(event_type, payload)
        else:
            logger.warning("Unknown platform", platform=platform)

        await _log_audit(
            action_type="webhook_processed",
            description=f"Processed {platform} event: {event_type}",
            details={"platform": platform, "event_type": event_type},
        )

    except Exception as e:
        logger.error(
            "Failed to process fleet event",
            platform=platform,
            event_type=event_type,
            error=str(e),
        )


async def _process_samsara_event(event_type: str, payload: dict):
    """Process Samsara webhook events."""
    telegram = TelegramService()

    if event_type == "AlertIncident":
        # Safety alert (crash, harsh driving, etc.)
        alert = payload.get("alertIncident", {})
        severity = alert.get("severity", "medium")
        vehicle_id = alert.get("vehicleId", "unknown")

        await telegram.send_alert(
            severity=severity,
            vehicle_id=vehicle_id,
            issue=f"Samsara Alert: {alert.get('type', 'Unknown')}",
            details=alert.get("description", ""),
            location=alert.get("location", ""),
        )

    elif event_type == "EngineFaultOn":
        # Engine fault detected
        fault = payload.get("engineFault", {})
        vehicle_id = fault.get("vehicleId", "unknown")

        # Store fault
        async with async_session() as session:
            new_fault = FaultCode(
                vehicle_id=vehicle_id,
                fault_code=fault.get("code", "unknown"),
                description=fault.get("description", ""),
                severity=fault.get("severity", "warning"),
                system=fault.get("system", "engine"),
                status="active",
            )
            session.add(new_fault)
            await session.commit()

        if fault.get("severity") == "critical":
            await telegram.send_alert(
                severity="critical",
                vehicle_id=vehicle_id,
                issue=f"Engine fault: {fault.get('code')} - {fault.get('description', '')}",
            )

    elif event_type == "DvirSubmitted":
        # DVIR submitted
        dvir = payload.get("dvir", {})
        logger.info("DVIR submitted", vehicle_id=dvir.get("vehicleId"))

    elif event_type == "GeofenceEntry" or event_type == "GeofenceExit":
        # Geofence event
        geofence = payload.get("geofence", {})
        logger.info(
            "Geofence event",
            event_type=event_type,
            vehicle_id=geofence.get("vehicleId"),
            geofence=geofence.get("name"),
        )

    else:
        logger.info("Unhandled Samsara event", event_type=event_type)


async def _process_motive_event(event_type: str, payload: dict):
    """Process Motive webhook events."""
    logger.info("Processing Motive event", event_type=event_type)
    # TODO: Implement Motive event processing


async def _process_fleetio_event(event_type: str, payload: dict):
    """Process Fleetio webhook events."""
    logger.info("Processing Fleetio event", event_type=event_type)
    # TODO: Implement Fleetio event processing


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
