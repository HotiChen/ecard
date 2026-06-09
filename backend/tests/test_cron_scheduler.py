"""
TDD tests for Cron Job scheduling logic.
get_due_schedules() queries DB for posts ready to execute.
mark_schedule_executed() stamps executed_at.
Uses SQLite in-memory + StaticPool — no Celery/Redis needed.
"""
from datetime import datetime, timezone, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.schedule_entry import ScheduleEntry
from app.services.cron_scheduler import get_due_schedules, mark_schedule_executed

_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_Session = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)

NOW = datetime(2026, 6, 9, 12, 0, 0, tzinfo=timezone.utc)
PAST = NOW - timedelta(hours=1)
FUTURE = NOW + timedelta(hours=1)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(_engine, tables=[ScheduleEntry.__table__])
    yield
    Base.metadata.drop_all(_engine, tables=[ScheduleEntry.__table__])


@pytest.fixture
def db():
    session = _Session()
    try:
        yield session
    finally:
        session.close()


def _make_entry(db, scheduled_at, is_canceled=False, executed_at=None):
    entry = ScheduleEntry(
        content="test",
        platforms=["threads"],
        scheduled_at=scheduled_at,
        is_canceled=is_canceled,
        executed_at=executed_at,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def test_due_returns_past_entry(db):
    entry = _make_entry(db, scheduled_at=PAST)
    due = get_due_schedules(db, now=NOW)
    assert len(due) == 1
    assert due[0].id == entry.id


def test_due_excludes_future_entry(db):
    _make_entry(db, scheduled_at=FUTURE)
    assert get_due_schedules(db, now=NOW) == []


def test_due_excludes_canceled_entry(db):
    _make_entry(db, scheduled_at=PAST, is_canceled=True)
    assert get_due_schedules(db, now=NOW) == []


def test_due_excludes_already_executed(db):
    _make_entry(db, scheduled_at=PAST, executed_at=PAST - timedelta(minutes=1))
    assert get_due_schedules(db, now=NOW) == []


def test_due_returns_multiple_past_entries(db):
    _make_entry(db, scheduled_at=PAST)
    _make_entry(db, scheduled_at=PAST - timedelta(hours=2))
    assert len(get_due_schedules(db, now=NOW)) == 2


def test_mark_executed_sets_timestamp(db):
    entry = _make_entry(db, scheduled_at=PAST)
    mark_schedule_executed(db, entry.id, now=NOW)
    db.refresh(entry)
    # SQLite stores datetimes without tz info; compare naive values
    assert entry.executed_at.replace(tzinfo=None) == NOW.replace(tzinfo=None)


def test_mark_executed_unknown_id_raises(db):
    with pytest.raises(ValueError, match="not found"):
        mark_schedule_executed(db, 9999, now=NOW)


def test_due_returns_empty_when_no_entries(db):
    assert get_due_schedules(db, now=NOW) == []
