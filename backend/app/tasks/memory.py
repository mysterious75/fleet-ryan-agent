"""
Memory management tasks — cleanup, archival, summaries.
"""

import structlog
from datetime import datetime, timedelta
from pathlib import Path
from app.tasks.celery_app import celery_app

logger = structlog.get_logger()

MEMORY_DIR = Path("/workspace/memory")
ARCHIVE_DIR = MEMORY_DIR / "archive"
WEEKLY_DIR = MEMORY_DIR / "weekly"
MONTHLY_DIR = MEMORY_DIR / "monthly"


@celery_app.task(name="app.tasks.memory.cleanup_memory")
def cleanup_memory():
    """Weekly memory cleanup — archive old files, generate summaries."""
    import asyncio
    asyncio.run(_cleanup_memory())


async def _cleanup_memory():
    """Async implementation of memory cleanup."""
    logger.info("Starting weekly memory cleanup")

    # Ensure directories exist
    for d in [ARCHIVE_DIR, WEEKLY_DIR, MONTHLY_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # 1. Archive daily files older than 7 days
    cutoff = datetime.now() - timedelta(days=7)
    archived = 0

    for filepath in MEMORY_DIR.glob("????-??-??.md"):
        try:
            date = datetime.strptime(filepath.stem, "%Y-%m-%d")
            if date < cutoff:
                archive_path = ARCHIVE_DIR / filepath.name
                filepath.rename(archive_path)
                archived += 1
        except ValueError:
            continue

    logger.info(f"Archived {archived} daily memory files")

    # 2. Generate weekly summary
    today = datetime.now()
    week_num = today.isocalendar()[1]
    year = today.year

    summary = f"""# Weekly Fleet Summary — {year} Week {week_num}
Generated: {today.strftime('%Y-%m-%d %H:%M')}

## Key Events
- Days tracked: 7
- Files archived: {archived}

## Fleet Health
- [To be populated with actual fleet data]

## Recommendations
- Review any critical incidents from this week
- Check pending escalations
- Update MEMORY.md with patterns
"""

    summary_path = WEEKLY_DIR / f"{year}-W{week_num:02d}.md"
    summary_path.write_text(summary)

    logger.info(f"Weekly summary generated: {summary_path.name}")


@celery_app.task(name="app.tasks.memory.monthly_summary")
def monthly_summary():
    """Monthly summary generation."""
    import asyncio
    asyncio.run(_monthly_summary())


async def _monthly_summary():
    """Async implementation of monthly summary."""
    logger.info("Generating monthly summary")

    today = datetime.now()
    month_start = today.replace(day=1)

    # Count daily files from this month
    daily_count = 0
    for filepath in MEMORY_DIR.glob("????-??-??.md"):
        try:
            date = datetime.strptime(filepath.stem, "%Y-%m-%d")
            if date >= month_start:
                daily_count += 1
        except ValueError:
            continue

    summary = f"""# Monthly Fleet Summary — {today.strftime('%B %Y')}
Generated: {today.strftime('%Y-%m-%d %H:%M')}

## Statistics
- Days tracked: {daily_count}
- Period: {month_start.strftime('%B %d')} - {today.strftime('%B %d')}

## Fleet Health
- [To be populated with actual fleet data]

## Cost Summary
- Maintenance: $[TBD]
- Fuel: $[TBD]
- Downtime: [TBD] hours

## Top Issues
- [To be populated]

## Recommendations
- [To be populated]
"""

    summary_path = MONTHLY_DIR / f"{today.strftime('%Y-%m')}.md"
    summary_path.write_text(summary)

    logger.info(f"Monthly summary generated: {summary_path.name}")
