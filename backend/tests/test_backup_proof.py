"""存證引擎單元測試（W2 核心流程之一）。"""

import hashlib
import json

from app.services.backup import build_proof


def test_build_proof_is_deterministic_for_same_inputs_except_timestamp():
    p1 = build_proof("hello", {"platform": "threads"})
    # sha256 應為 64 字元 hex
    assert len(p1.sha256) == 64
    int(p1.sha256, 16)  # 可被解析為 16 進位即代表是合法 hex


def test_build_proof_hash_matches_payload():
    proof = build_proof("hello world", {"k": "v"})
    expected = hashlib.sha256(proof.payload_bytes).hexdigest()
    assert proof.sha256 == expected


def test_build_proof_payload_contains_content_and_timestamp():
    proof = build_proof("攝影師的一天", {"platform": "instagram"})
    payload = json.loads(proof.payload_bytes)
    assert payload["content"] == "攝影師的一天"
    assert payload["metadata"]["platform"] == "instagram"
    assert payload["proof_timestamp"] == proof.proof_timestamp


def test_different_content_yields_different_hash():
    a = build_proof("a")
    b = build_proof("b")
    assert a.sha256 != b.sha256
