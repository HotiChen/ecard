from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.claude_client import get_claude_client
from app.services.sentiment import SentimentResult, analyze_comments
from app.services.weekly_report import WeeklyStats, WeeklyReport, generate_weekly_report
from app.services.next_post_suggestion import PostHistory, PostSuggestion, suggest_next_post

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class SentimentRequest(BaseModel):
    comments: list[str]


class SentimentResponse(BaseModel):
    comment: str
    label: str


class WeeklyReportResponse(BaseModel):
    summary: str


class SuggestionResponse(BaseModel):
    suggestion: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/sentiment", response_model=list[SentimentResponse])
async def sentiment(
    payload: SentimentRequest,
    claude: Any = Depends(get_claude_client),
) -> list[SentimentResponse]:
    results: list[SentimentResult] = await analyze_comments(payload.comments, client=claude)
    return [SentimentResponse(comment=r.comment, label=r.label.value) for r in results]


@router.post("/weekly-report", response_model=WeeklyReportResponse)
async def weekly_report(
    payload: WeeklyStats,
    claude: Any = Depends(get_claude_client),
) -> WeeklyReportResponse:
    report: WeeklyReport = await generate_weekly_report(payload, client=claude)
    return WeeklyReportResponse(summary=report.summary)


@router.post("/suggest", response_model=SuggestionResponse)
async def suggest(
    payload: PostHistory,
    claude: Any = Depends(get_claude_client),
) -> SuggestionResponse:
    result: PostSuggestion = await suggest_next_post(payload, client=claude)
    return SuggestionResponse(suggestion=result.suggestion)
