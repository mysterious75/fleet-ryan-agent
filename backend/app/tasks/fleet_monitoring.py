"""
Fleet monitoring background tasks.
"""

import structlog
from datetime import datetime
from app.tasks.celery_app import celery_app
from app.services.samsara import SamsaraService
from app.services.telegram import TelegramService
from sqlalchemy import select
from app.core.database import async_session, FaultCode, FuelTransaction, AuditLog

logger = structlog.get_logger()


@celery_app.task(name="app.tasks.fleet_monitoring.check_fault_codes")
def check_fault_codes():
    """Check for new fault codes across the fleet."""
    import asyncio
    asyncio.run(_check_fault_codes())


async def _check_fault_codes():
    """Async implementation of fault code checking."""
    samsara = SamsaraService()
    telegram = TelegramService()

    try:
        faults = await samsara.get_fleet_faults(status="active")
        logger.info("Fault code check completed", total_faults=len(faults))

        for fault in faults:
            severity = fault.get("severity", "info")
            vehicle_id = fault.get("vehicleId", "unknown")
            fault_code = fault.get("code", "unknown")

            # Store in database
            async with async_session() as session:
                existing = await session.execute(
                    select(FaultCode).where(
                        FaultCode.vehicle_id == vehicle_id,
                        FaultCode.fault_code == fault_code,
                        FaultCode.status == "active",
                    )
                )
                existing_fault = existing.scalar_one_or_none()

                if existing_fault:
                    existing_fault.last_seen = datetime.utcnow()
                    existing_fault.occurrence_count += 1
                else:
                    new_fault = FaultCode(
                        vehicle_id=vehicle_id,
                        fault_code=fault_code,
                        description=fault.get("description", ""),
                        severity=severity,
                        system=fault.get("system", "unknown"),
                        status="active",
                    )
                    session.add(new_fault)

                await session.commit()

            # Alert for critical faults
            if severity == "critical":
                await telegram.send_alert(
                    severity="critical",
                    vehicle_id=vehicle_id,
                    issue=f"Fault code {fault_code}: {fault.get('description', 'Unknown')}",
                    details=f"System: {fault.get('system', 'Unknown')}",
                )

        # Log to audit
        await _log_audit(
            action_type="fault_code_check",
            description=f"Checked {len(faults)} active fault codes",
            details={"total_faults": len(faults)},
        )

    except Exception as e:
        logger.error("Failed to check fault codes", error=str(e))


@celery_app.task(name="app.tasks.fleet_monitoring.check_compliance")
def check_compliance():
    """Check fleet compliance status (HOS, DVIR)."""
    import asyncio
    asyncio.run(_check_compliance())


async def _check_compliance():
    """Async implementation of compliance checking."""
    samsara = SamsaraService()
    telegram = TelegramService()

    try:
        # Check HOS status
        hos_data = await samsara.get_hos_status()

        violations = [d for d in hos_data if d.get("in_violation")]
        near_limit = [d for d in hos_data if d.get("near_limit") and not d.get("in_violation")]

        # Alert for violations
        for driver in violations:
            await telegram.send_compliance_alert(
                driver_name=driver.get("driver_name", "Unknown"),
                vehicle_id=driver.get("vehicle_id", "Unknown"),
                violation_type="HOS Violation",
                details=f"Driving time exceeded. Remaining: {driver.get('driving_minutes_remaining', 0):.0f} min",
            )

        # Alert for near-limit drivers
        for driver in near_limit:
            await telegram.send_alert(
                severity="high",
                vehicle_id=driver.get("vehicle_id", "Unknown"),
                issue=f"Driver {driver.get('driver_name')} approaching HOS limit",
                details=f"Driving time remaining: {driver.get('driving_minutes_remaining', 0):.0f} min",
            )

        logger.info(
            "Compliance check completed",
            total_drivers=len(hos_data),
            violations=len(violations),
            near_limit=len(near_limit),
        )

        await _log_audit(
            action_type="compliance_check",
            description=f"Compliance check: {len(violations)} violations, {len(near_limit)} near limit",
            details={
                "total_drivers": len(hos_data),
                "violations": len(violations),
                "near_limit": len(near_limit),
            },
        )

    except Exception as e:
        logger.error("Failed to check compliance", error=str(e))


@celery_app.task(name="app.tasks.fleet_monitoring.check_fuel_anomalies")
def check_fuel_anomalies():
    """Check for fuel anomalies (theft, leaks, excessive consumption)."""
    import asyncio
    asyncio.run(_check_fuel_anomalies())


async def _check_fuel_anomalies():
    """Async implementation of fuel anomaly detection."""
    # TODO: Implement fuel anomaly detection
    # This would cross-reference fuel card transactions with telematics data
    logger.info("Fuel anomaly check completed (not yet implemented)")


@celery_app.task(name="app.tasks.fleet_monitoring.fleet_health_snapshot")
def fleet_health_snapshot():
    """Generate a fleet health snapshot."""
    import asyncio
    asyncio.run(_fleet_health_snapshot())


async def _fleet_health_snapshot():
    """Async implementation of fleet health snapshot."""
    samsara = SamsaraService()

    try:
        overview = await samsara.get_fleet_overview()
        logger.info("Fleet health snapshot generated", overview=overview)

        await _log_audit(
            action_type="health_snapshot",
            description="Fleet health snapshot generated",
            details=overview,
        )

    except Exception as e:
        logger.error("Failed to generate fleet health snapshot", error=str(e))


async def _log_audit(
    action_type: str,
    description: str,
    details: dict = None,
):
    """Log an action to the audit trail."""
    async with async_session() as session:
        audit = AuditLog(
            action_type=action_type,
            description=description,
            details=details,
            agent_decision="auto_act",
        )
        session.add(audit)
        await session.commit()
