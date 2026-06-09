from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription_record import SubscriptionRecord
from app.schemas.subscription import SubscriptionRead, SubscriptionSeed

router = APIRouter()


def _get_record(db: Session) -> SubscriptionRecord | None:
    return db.query(SubscriptionRecord).order_by(SubscriptionRecord.id.desc()).first()


@router.get("", response_model=SubscriptionRead)
def get_subscription(db: Session = Depends(get_db)) -> SubscriptionRead:
    record = _get_record(db)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscription found")
    return SubscriptionRead.model_validate(record)


@router.post("/cancel", response_model=SubscriptionRead)
def cancel_subscription(db: Session = Depends(get_db)) -> SubscriptionRead:
    record = _get_record(db)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscription found")
    record.status = "canceled"
    db.commit()
    db.refresh(record)
    return SubscriptionRead.model_validate(record)


@router.post("/_seed", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
def seed_subscription(payload: SubscriptionSeed, db: Session = Depends(get_db)) -> SubscriptionRead:
    """Test-only endpoint to create a subscription record."""
    record = SubscriptionRecord(
        plan=payload.plan,
        status=payload.status,
        trial_ends_at=payload.trial_ends_at,
        current_period_end=payload.current_period_end,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return SubscriptionRead.model_validate(record)
