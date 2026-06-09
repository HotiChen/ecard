from pydantic import BaseModel, Field


class PostRecordCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    platforms: list[str] = Field(..., min_length=1)


class PostRecordRead(BaseModel):
    id: int
    content: str
    platforms: list[str]
    sha256: str
    proof_timestamp: str

    model_config = {"from_attributes": True}


class ProofResponse(BaseModel):
    sha256: str
    proof_timestamp: str
