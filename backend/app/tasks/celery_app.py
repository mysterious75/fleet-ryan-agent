"""
Celery application configuration for background tasks.
Optional — works without Celery/Redis installed.
"""

import structlog

logger = structlog.get_logger()

# Try to import celery — it's optional
try:
    from celery import Celery
    from celery.schedules import crontab
    from app.core.config import settings

    # Create Celery app
    celery_app = Celery(
        "fleet-ryan",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
    )

    # Celery configuration
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="America/Indiana/Indianapolis",
        enable_utc=True,
        task_track_started=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        result_expires=3600,  # 1 hour
    )

    # Periodic tasks (beat schedule)
    celery_app.conf.beat_schedule = {
        # Fleet monitoring tasks
        "check-fault-codes": {
            "task": "app.tasks.fleet_monitoring.check_fault_codes",
            "schedule": 1800.0,  # Every 30 minutes
        },
        "check-compliance": {
            "task": "app.tasks.fleet_monitoring.check_compliance",
            "schedule": 3600.0,  # Every 1 hour
        },
        "check-fuel-anomalies": {
            "task": "app.tasks.fleet_monitoring.check_fuel_anomalies",
            "schedule": 7200.0,  # Every 2 hours
        },
        "fleet-health-snapshot": {
            "task": "app.tasks.fleet_monitoring.fleet_health_snapshot",
            "schedule": 21600.0,  # Every 6 hours
        },
        # Daily reports
        "daily-summary": {
            "task": "app.tasks.reports.daily_summary",
            "schedule": crontab(hour=8, minute=0),  # 8:00 AM daily
        },
        # Weekly memory cleanup
        "memory-cleanup": {
            "task": "app.tasks.memory.cleanup_memory",
            "schedule": crontab(hour=2, minute=0, day_of_week=1),  # Monday 2:00 AM
        },
        # Monthly summary
        "monthly-summary": {
            "task": "app.tasks.memory.monthly_summary",
            "schedule": crontab(hour=3, minute=0, day_of_month=1),  # 1st of month 3:00 AM
        },
    }

    # Auto-discover tasks
    celery_app.autodiscover_tasks(["app.tasks"])

    HAS_CELERY = True
    logger.info("Celery configured successfully")

except ImportError:
    HAS_CELERY = False
    celery_app = None
    logger.info("Celery not installed — background tasks disabled")
