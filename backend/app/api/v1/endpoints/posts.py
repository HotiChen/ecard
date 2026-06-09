from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.post_record import PostRecord
from app.schemas.post_record import PostRecordCreate, PostRecordRead, ProofResponse
from app.services.backup import build_proof

router = APIRouter()


@router.post("", response_model=ProofResponse, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostRecordCreate, db: Session = Depends(get_db)) -> ProofResponse:
    proof = build_proof(
        payload.content,
        metadata={"platforms": payload.platforms},
    )
    record = PostRecord(
        content=payload.content,
        platforms=payload.platforms,
        sha256=proof.sha256,
        proof_timestamp=proof.proof_timestamp,
    )
    db.add(record)
    db.commit()
    return ProofResponse(sha256=proof.sha256, proof_timestamp=proof.proof_timestamp)


@router.get("", response_model=list[PostRecordRead])
def list_posts(db: Session = Depends(get_db)) -> list[PostRecordRead]:
    records = db.query(PostRecord).order_by(PostRecord.id.desc()).all()
    return [PostRecordRead.model_validate(r) for r in records]
