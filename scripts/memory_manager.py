#!/usr/bin/env python3
"""
FleetCommander Memory Manager
Manages memory files — cleanup, archival, summaries.
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path


class MemoryManager:
    """Manages FleetCommander's memory system."""

    def __init__(self, memory_dir: str = "agent-workspace/memory"):
        self.memory_dir = Path(memory_dir)
        self.archive_dir = self.memory_dir / "archive"
        self.weekly_dir = self.memory_dir / "weekly"
        self.monthly_dir = self.memory_dir / "monthly"

        # Create directories
        for d in [self.archive_dir, self.weekly_dir, self.monthly_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def get_daily_files(self, days: int = 30) -> list:
        """Get daily memory files from the last N days."""
        files = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            filename = date.strftime("%Y-%m-%d") + ".md"
            filepath = self.memory_dir / filename
            if filepath.exists():
                files.append({
                    "date": date,
                    "path": filepath,
                    "size": filepath.stat().st_size,
                })
        return files

    def cleanup_old_daily_files(self, keep_days: int = 7):
        """Archive daily files older than keep_days."""
        cutoff = datetime.now() - timedelta(days=keep_days)
        archived = 0

        for filepath in self.memory_dir.glob("????-??-??.md"):
            try:
                date_str = filepath.stem  # e.g., "2026-07-05"
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                if file_date < cutoff:
                    # Move to archive
                    archive_path = self.archive_dir / filepath.name
                    shutil.move(str(filepath), str(archive_path))
                    archived += 1
                    print(f"  Archived: {filepath.name}")
            except ValueError:
                continue

        return archived

    def generate_weekly_summary(self) -> str:
        """Generate a weekly summary from daily files."""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())

        # Read daily files from this week
        daily_contents = []
        for i in range(7):
            date = week_start + timedelta(days=i)
            filepath = self.memory_dir / f"{date.strftime('%Y-%m-%d')}.md"
            if filepath.exists():
                daily_contents.append({
                    "date": date,
                    "content": filepath.read_text(),
                })

        if not daily_contents:
            return "No daily memory files found for this week."

        # Generate summary
        week_num = today.isocalendar()[1]
        year = today.year

        summary = f"""# Weekly Fleet Summary — {year} Week {week_num}

## Period: {week_start.strftime('%B %d')} - {today.strftime('%B %d, %Y')}

## Key Events
- Days with memory: {len(daily_contents)}
- Generated: {today.strftime('%Y-%m-%d %H:%M')}

## Daily Breakdown
"""

        for entry in daily_contents:
            summary += f"\n### {entry['date'].strftime('%A, %B %d')}\n"
            # Extract key info from daily file
            content = entry['content']
            if 'CRITICAL' in content:
                summary += "- ⚠️ Had critical incidents\n"
            if 'escalation' in content.lower():
                summary += "- 📋 Escalations occurred\n"
            if 'HEARTBEAT_OK' in content:
                summary += "- ✅ Normal operation\n"

        summary += """
## Recommendations
- Review any critical incidents
- Check pending escalations
- Update MEMORY.md with patterns

## Next Week Focus
- Monitor recurring issues
- Track maintenance schedule
- Review fuel efficiency
"""

        # Save weekly summary
        summary_path = self.weekly_dir / f"{year}-W{week_num:02d}.md"
        summary_path.write_text(summary)

        return summary

    def generate_monthly_summary(self) -> str:
        """Generate a monthly summary."""
        today = datetime.now()
        month_start = today.replace(day=1)

        # Read all daily files from this month
        daily_files = []
        for filepath in sorted(self.memory_dir.glob("????-??-??.md")):
            try:
                date = datetime.strptime(filepath.stem, "%Y-%m-%d")
                if date >= month_start:
                    daily_files.append({
                        "date": date,
                        "content": filepath.read_text(),
                    })
            except ValueError:
                continue

        summary = f"""# Monthly Fleet Summary — {today.strftime('%B %Y')}

## Period: {month_start.strftime('%B %d')} - {today.strftime('%B %d, %Y')}

## Statistics
- Days tracked: {len(daily_files)}
- Generated: {today.strftime('%Y-%m-%d %H:%M')}

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

        # Save monthly summary
        summary_path = self.monthly_dir / f"{today.strftime('%Y-%m')}.md"
        summary_path.write_text(summary)

        return summary

    def update_long_term_memory(self):
        """Update MEMORY.md with recent patterns."""
        memory_path = self.memory_dir.parent / "MEMORY.md"
        if not memory_path.exists():
            return

        # Read recent daily files
        recent_files = self.get_daily_files(days=7)

        # Extract patterns (simplified)
        patterns = []
        for f in recent_files:
            content = f['path'].read_text()
            if 'P0340' in content:
                patterns.append("Recurring P0340 fault detected")
            if 'fuel theft' in content.lower():
                patterns.append("Fuel anomaly detected")
            if 'HOS violation' in content:
                patterns.append("HOS compliance issue")

        if patterns:
            # Append to MEMORY.md
            with open(memory_path, 'a') as f:
                f.write(f"\n## Weekly Update — {datetime.now().strftime('%Y-%m-%d')}\n")
                for p in set(patterns):
                    f.write(f"- {p}\n")

    def run_weekly_cleanup(self):
        """Run full weekly cleanup."""
        print("=== FleetCommander Weekly Memory Cleanup ===")
        print()

        # 1. Archive old daily files
        print("1. Archiving old daily files...")
        archived = self.cleanup_old_daily_files(keep_days=7)
        print(f"   Archived {archived} files")

        # 2. Generate weekly summary
        print("\n2. Generating weekly summary...")
        summary = self.generate_weekly_summary()
        print("   Weekly summary generated")

        # 3. Update long-term memory
        print("\n3. Updating long-term memory...")
        self.update_long_term_memory()
        print("   MEMORY.md updated")

        # 4. Stats
        print("\n4. Memory stats:")
        daily_count = len(list(self.memory_dir.glob("????-??-??.md")))
        weekly_count = len(list(self.weekly_dir.glob("*.md")))
        monthly_count = len(list(self.monthly_dir.glob("*.md")))
        archive_count = len(list(self.archive_dir.glob("*.md")))
        print(f"   Daily files: {daily_count}")
        print(f"   Weekly summaries: {weekly_count}")
        print(f"   Monthly summaries: {monthly_count}")
        print(f"   Archived files: {archive_count}")

        print("\n=== Cleanup Complete ===")


if __name__ == "__main__":
    import sys

    manager = MemoryManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "weekly":
            manager.run_weekly_cleanup()
        elif command == "monthly":
            manager.generate_monthly_summary()
            print("Monthly summary generated")
        elif command == "stats":
            files = manager.get_daily_files(days=30)
            print(f"Daily files (last 30 days): {len(files)}")
            for f in files:
                print(f"  {f['date'].strftime('%Y-%m-%d')} ({f['size']} bytes)")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python memory_manager.py [weekly|monthly|stats]")
    else:
        manager.run_weekly_cleanup()
