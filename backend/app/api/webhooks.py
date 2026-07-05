"""
Webhook receiver endpoints for fleet platform events.
"""

from fastapi import APIRouter, HTTPException, Request, Header
from typing import Optional
from datetime import datetime
import structlog
import hashlib
import hmac

from app.core.config import settings
# Import celery task lazily to avoid import errors when celery is not installed
def _get_process_fleet_event():
    try:
        from app.tasks.fleet_events import process_fleet_event
        return process_fleet_event
    except ImportError:
        return None

logger = structlog.get_logger()
router = APIRouter()


@router.post("/samsara")
async def samsara_webhook(
    request: Request,
    x_samsara_signature: Optional[str] = Header(None),
):
    """Receive Samsara webhook events."""
    body = await request.body()

    # Verify webhook signature
    if settings.SAMSARA_API_TOKEN:
        expected_sig = hmac.new(
            settings.SAMSARA_API_TOKEN.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(x_samsara_signature or "", expected_sig):
            raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = await request.json()
        logger.info("Samsara webhook received", event_type=data.get("eventType"))

        # Process event asynchronously (if celery is available)
        process_fn = _get_process_fleet_event()
        if process_fn:
            process_fn.delay(
                platform="samsara",
                event_type=data.get("eventType"),
                payload=data,
            )
        else:
            logger.info("Celery not available — event logged only")

        return {"status": "accepted"}
    except Exception as e:
        logger.error("Failed to process Samsara webhook", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process webhook")


@router.post("/motive")
async def motive_webhook(request: Request):
    """Receive Motive (KeepTruckin') webhook events."""
    try:
        data = await request.json()
        logger.info("Motive webhook received", event_type=data.get("event_type"))

        # Process event asynchronously (if celery is available)
        process_fn = _get_process_fleet_event()
        if process_fn:
            process_fn.delay(
                platform="motive",
                event_type=data.get("event_type"),
                payload=data,
            )
        else:
            logger.info("Celery not available — event logged only")

        return {"status": "accepted"}
    except Exception as e:
        logger.error("Failed to process Motive webhook", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process webhook")


@router.post("/fleetio")
async def fleetio_webhook(request: Request):
    """Receive Fleetio webhook events."""
    try:
        data = await request.json()
        logger.info("Fleetio webhook received", event_type=data.get("event_type"))

        # Process event asynchronously (if celery is available)
        process_fn = _get_process_fleet_event()
        if process_fn:
            process_fn.delay(
                platform="fleetio",
                event_type=data.get("event_type"),
                payload=data,
            )
        else:
            logger.info("Celery not available — event logged only")

        return {"status": "accepted"}
    except Exception as e:
        logger.error("Failed to process Fleetio webhook", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process webhook")
