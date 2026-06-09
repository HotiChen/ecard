from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.metric_record import MetricRecord
from app.schemas.metric import MetricCreate, MetricRead

router = APIRouter()


@router.get("/metrics", response_model=list[MetricRead])
def list_metrics(
    post_id: Optional[int] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[MetricRead]:
    q = db.query(MetricRecord)
    if post_id is not None:
        q = q.filter(MetricRecord.post_id == post_id)
    if platform is not None:
        q = q.filter(MetricRecord.platform == platform)
    return [MetricRead.model_validate(r) for r in q.all()]


@router.post("/metrics", response_model=MetricRead, status_code=status.HTTP_201_CREATED)
def record_metric(payload: MetricCreate, db: Session = Depends(get_db)) -> MetricRead:
    record = MetricRecord(
        post_id=payload.post_id,
        platform=payload.platform.value,
        likes=payload.likes,
        comments=payload.comments,
        replies=payload.replies,
        reposts=payload.reposts,
        views=payload.views,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return MetricRead.model_validate(record)
