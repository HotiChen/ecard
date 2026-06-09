from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Plan(BaseModel):
    id: str
    name: str
    price_twd: int
    billing: str
    features: list[str]


_PLANS: list[Plan] = [
    Plan(
        id="free",
        name="免費試用",
        price_twd=0,
        billing="14 天免費",
        features=[
            "多平台發文（Threads / IG / X）",
            "SHA-256 備份存證",
            "基礎數據看板",
            "AI 留言情緒分析",
        ],
    ),
    Plan(
        id="basic",
        name="基礎版",
        price_twd=390,
        billing="每月",
        features=[
            "免費版全部功能",
            "排程發文",
            "每月 100 篇發文",
            "每週自動週報",
        ],
    ),
    Plan(
        id="pro",
        name="專業版",
        price_twd=990,
        billing="每月",
        features=[
            "基礎版全部功能",
            "無限發文",
            "AI 下一篇建議",
            "爆文特徵分析報告",
            "優先客服支援",
        ],
    ),
]


@router.get("", response_model=list[Plan])
def list_plans() -> list[Plan]:
    return _PLANS
