"""貼文內容文字特徵分析（W6 AI 分析引擎前置）。

extract_features 從貼文文字提取可量化特徵，供 Claude 分析或本地統計使用。
純 regex／字串操作，不呼叫任何外部服務。
"""

import re
from dataclasses import dataclass, field

_RE_HASHTAG = re.compile(r"#([\w一-鿿぀-ヿ]+)", re.UNICODE)
_RE_MENTION = re.compile(r"@([\w]+)", re.UNICODE)
_RE_URL = re.compile(r"https?://\S+", re.UNICODE)
_RE_QUESTION = re.compile(r"[?？]")
_RE_EXCLAMATION = re.compile(r"[!！]")


@dataclass
class ContentFeatures:
    """從貼文文字提取出的結構化特徵。"""

    char_count: int
    line_count: int
    hashtag_count: int
    hashtags: list[str] = field(default_factory=list)
    mention_count: int = 0
    mentions: list[str] = field(default_factory=list)
    url_count: int = 0
    has_question: bool = False
    has_exclamation: bool = False


def extract_features(content: str) -> ContentFeatures:
    """從貼文內容提取文字特徵，用於 AI 分析與統計報告。"""
    if not content:
        return ContentFeatures(
            char_count=0,
            line_count=0,
            hashtag_count=0,
        )

    hashtags = _RE_HASHTAG.findall(content)
    mentions = _RE_MENTION.findall(content)
    urls = _RE_URL.findall(content)

    return ContentFeatures(
        char_count=len(content),
        line_count=content.count("\n") + 1,
        hashtag_count=len(hashtags),
        hashtags=hashtags,
        mention_count=len(mentions),
        mentions=mentions,
        url_count=len(urls),
        has_question=bool(_RE_QUESTION.search(content)),
        has_exclamation=bool(_RE_EXCLAMATION.search(content)),
    )
