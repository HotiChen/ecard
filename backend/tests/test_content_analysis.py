"""貼文內容文字特徵分析單元測試（W6）。

驗證 extract_features 從貼文文字中正確提取各種特徵，純字串處理，零外部依賴。
"""

import pytest

from app.services.content_analysis import ContentFeatures, extract_features


# ── 基本統計 ──────────────────────────────────────────────────────────────────


def test_empty_string_returns_zero_counts():
    f = extract_features("")
    assert f.char_count == 0
    assert f.hashtag_count == 0
    assert f.mention_count == 0
    assert f.url_count == 0
    assert f.line_count == 0


def test_char_count_matches_length():
    content = "攝影師的一天"
    assert extract_features(content).char_count == len(content)


def test_line_count_single_line():
    assert extract_features("hello world").line_count == 1


def test_line_count_multiple_lines():
    assert extract_features("line1\nline2\nline3").line_count == 3


def test_line_count_empty_string_is_zero():
    assert extract_features("").line_count == 0


# ── Hashtag ───────────────────────────────────────────────────────────────────


def test_hashtag_count_none():
    assert extract_features("沒有 hashtag 的文章").hashtag_count == 0


def test_hashtag_count_correct():
    f = extract_features("美好的一天 #攝影 #台灣 #travel")
    assert f.hashtag_count == 3


def test_hashtags_extracted_correctly():
    f = extract_features("#攝影 #台灣")
    assert set(f.hashtags) == {"攝影", "台灣"}


def test_hashtag_mixed_languages():
    f = extract_features("#photo #攝影師")
    assert f.hashtag_count == 2
    assert "photo" in f.hashtags
    assert "攝影師" in f.hashtags


# ── Mention ───────────────────────────────────────────────────────────────────


def test_mention_count_none():
    assert extract_features("沒有 mention 的文章").mention_count == 0


def test_mention_count_correct():
    f = extract_features("感謝 @alice 和 @bob 的協助")
    assert f.mention_count == 2


def test_mentions_extracted_correctly():
    f = extract_features("@alice @bob")
    assert set(f.mentions) == {"alice", "bob"}


# ── URL ───────────────────────────────────────────────────────────────────────


def test_url_count_none():
    assert extract_features("純文字，沒有連結").url_count == 0


def test_url_count_http():
    f = extract_features("看這裡 https://example.com 和 http://foo.bar/path")
    assert f.url_count == 2


# ── 語氣偵測 ─────────────────────────────────────────────────────────────────


def test_has_question_true():
    assert extract_features("你喜歡攝影嗎？").has_question is True


def test_has_question_false():
    assert extract_features("我喜歡攝影。").has_question is False


def test_has_exclamation_true():
    assert extract_features("太棒了！").has_exclamation is True


def test_has_exclamation_false():
    assert extract_features("普通的一天。").has_exclamation is False


# ── 回傳型別 ──────────────────────────────────────────────────────────────────


def test_returns_content_features_instance():
    assert isinstance(extract_features("test"), ContentFeatures)
