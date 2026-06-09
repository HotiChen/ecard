from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.schedule_entry import ScheduleEntry


def get_due_schedules(db: Session, now: datetime | None = None) -> list[ScheduleEntry]:
    """Return schedule entries that are past their scheduled_at and not yet canceled or executed."""
    if now is None:
        now = datetime.now(timezone.utc)
    return (
        db.query(ScheduleEntry)
        .filter(
            ScheduleEntry.scheduled_at <= now,
            ScheduleEntry.is_canceled.is_(False),
            ScheduleEntry.executed_at.is_(None),
        )
        .order_by(ScheduleEntry.scheduled_at)
        .all()
    )


def mark_schedule_executed(db: Session, schedule_id: int, now: datetime | None = None) -> ScheduleEntry:
    """Stamp executed_at on the given schedule entry. Raises ValueError if not found."""
    if now is None:
        now = datetime.now(timezone.utc)
    entry = db.get(ScheduleEntry, schedule_id)
    if entry is None:
        raise ValueError(f"Schedule {schedule_id} not found")
    entry.executed_at = now
    db.commit()
    db.refresh(entry)
    return entry
