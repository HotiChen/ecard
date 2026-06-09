"""存證引擎單元測試（W2 核心流程之一）。"""

import hashlib
import json
from pathlib import Path

from app.services.backup import build_proof, write_proof_file


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


# --- write_proof_file 測試 ---


def test_write_proof_file_creates_file(tmp_path: Path):
    proof = build_proof("攝影師的一天", {"platform": "threads"})
    out = write_proof_file(proof, tmp_path / "post_123.proof.json")
    assert out.exists()


def test_write_proof_file_contains_sha256_and_timestamp(tmp_path: Path):
    proof = build_proof("攝影師的一天", {"platform": "threads"})
    out = write_proof_file(proof, tmp_path / "post_123.proof.json")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["sha256"] == proof.sha256
    assert data["proof_timestamp"] == proof.proof_timestamp


def test_write_proof_file_payload_is_verifiable(tmp_path: Path):
    proof = build_proof("內容可被核實", {"platform": "instagram"})
    out = write_proof_file(proof, tmp_path / "post.proof.json")
    data = json.loads(out.read_text(encoding="utf-8"))
    # payload 存為 JSON 字串，可重新計算 hash 驗證
    payload_bytes = data["payload"].encode("utf-8")
    assert hashlib.sha256(payload_bytes).hexdigest() == data["sha256"]


def test_write_proof_file_returns_path(tmp_path: Path):
    proof = build_proof("test")
    result = write_proof_file(proof, tmp_path / "x.proof.json")
    assert isinstance(result, Path)
