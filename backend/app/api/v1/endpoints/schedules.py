from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.schedule_entry import ScheduleEntry
from app.schemas.schedule import ScheduleCreate, ScheduleRead

router = APIRouter()


@router.post("", response_model=ScheduleRead, status_code=status.HTTP_201_CREATED)
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)) -> ScheduleRead:
    entry = ScheduleEntry(
        content=payload.content,
        platforms=payload.platforms,
        scheduled_at=payload.scheduled_at,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return ScheduleRead.model_validate(entry)


@router.get("", response_model=list[ScheduleRead])
def list_schedules(db: Session = Depends(get_db)) -> list[ScheduleRead]:
    entries = db.query(ScheduleEntry).order_by(ScheduleEntry.scheduled_at).all()
    return [ScheduleRead.model_validate(e) for e in entries]


@router.post("/{schedule_id}/cancel", response_model=ScheduleRead)
def cancel_schedule(schedule_id: int, db: Session = Depends(get_db)) -> ScheduleRead:
    entry = db.get(ScheduleEntry, schedule_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    entry.is_canceled = True
    db.commit()
    db.refresh(entry)
    return ScheduleRead.model_validate(entry)
