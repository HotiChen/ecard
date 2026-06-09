"""
Tests for updating a proof record with latest interaction metrics.
Pure-logic tests — no DB, no external services.
"""
import json
from pathlib import Path

import pytest

from app.services.backup import (
    build_proof,
    update_proof_with_metrics,
    read_proof_file,
    MetricsSnapshot,
)


def test_metrics_snapshot_fields():
    m = MetricsSnapshot(likes=10, comments=5, replies=2, reposts=1, views=200)
    assert m.total_interactions == 18


def test_update_proof_adds_metrics_key(tmp_path):
    proof = build_proof("測試內容")
    filepath = tmp_path / "test.proof.json"
    filepath.write_text(
        json.dumps(
            {
                "sha256": proof.sha256,
                "proof_timestamp": proof.proof_timestamp,
                "payload": proof.payload_bytes.decode(),
            },
            ensure_ascii=False,
        )
    )
    metrics = MetricsSnapshot(likes=50, comments=10, replies=3, reposts=2, views=500)
    update_proof_with_metrics(filepath, metrics)
    data = json.loads(filepath.read_text())
    assert "metrics" in data


def test_update_proof_stores_correct_values(tmp_path):
    proof = build_proof("測試內容")
    filepath = tmp_path / "test.proof.json"
    filepath.write_text(
        json.dumps(
            {
                "sha256": proof.sha256,
                "proof_timestamp": proof.proof_timestamp,
                "payload": proof.payload_bytes.decode(),
            }
        )
    )
    metrics = MetricsSnapshot(likes=50, comments=10, replies=3, reposts=2, views=500)
    update_proof_with_metrics(filepath, metrics)
    data = json.loads(filepath.read_text())
    assert data["metrics"]["likes"] == 50
    assert data["metrics"]["views"] == 500
    assert data["metrics"]["total_interactions"] == 65


def test_update_proof_preserves_sha256(tmp_path):
    proof = build_proof("測試內容")
    filepath = tmp_path / "test.proof.json"
    filepath.write_text(
        json.dumps(
            {
                "sha256": proof.sha256,
                "proof_timestamp": proof.proof_timestamp,
                "payload": proof.payload_bytes.decode(),
            }
        )
    )
    update_proof_with_metrics(filepath, MetricsSnapshot(likes=1))
    data = json.loads(filepath.read_text())
    assert data["sha256"] == proof.sha256


def test_read_proof_file(tmp_path):
    proof = build_proof("內容")
    filepath = tmp_path / "proof.json"
    filepath.write_text(
        json.dumps(
            {
                "sha256": proof.sha256,
                "proof_timestamp": proof.proof_timestamp,
                "payload": proof.payload_bytes.decode(),
            }
        )
    )
    data = read_proof_file(filepath)
    assert data["sha256"] == proof.sha256


def test_update_nonexistent_file_raises():
    with pytest.raises(FileNotFoundError):
        update_proof_with_metrics(Path("/nonexistent/file.json"), MetricsSnapshot())
