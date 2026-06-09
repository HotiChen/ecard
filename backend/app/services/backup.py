"""備份引擎：把發文內容備份到 Google Drive，並產生 SHA-256 存證。

存證設計：
  - 將貼文內容（含 metadata）序列化成 bytes，算 SHA-256 當作未竄改的指紋。
  - 記錄產生當下的時間戳。
  - W2 會把檔案實際上傳到 Google Drive，並回填 drive_file_id。

注意（見 docs/ROADMAP.md 風險）：若要對外宣稱「法律存證」，時間戳來源建議改用
可信第三方時間戳服務（RFC 3161 TSA），而非僅伺服器本機時間。
"""

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ProofResult:
    sha256: str
    proof_timestamp: str
    payload_bytes: bytes


def build_proof(content: str, metadata: dict | None = None) -> ProofResult:
    """為一篇貼文產生 SHA-256 + 時間戳存證資料。

    可被獨立測試，不依賴外部服務（W2 單元測試的核心）。
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = {
        "content": content,
        "metadata": metadata or {},
        "proof_timestamp": timestamp,
    }
    payload_bytes = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(
        "utf-8"
    )
    digest = hashlib.sha256(payload_bytes).hexdigest()
    return ProofResult(
        sha256=digest, proof_timestamp=timestamp, payload_bytes=payload_bytes
    )


def write_proof_file(proof: ProofResult, filepath: Path) -> Path:
    """把存證資料寫成 JSON 檔（.proof.json）。

    檔案內容包含 sha256、proof_timestamp 與 payload（UTF-8 字串）。
    可用 sha256(payload.encode()) 重新驗證雜湊，確保未竄改。
    """
    data = {
        "sha256": proof.sha256,
        "proof_timestamp": proof.proof_timestamp,
        "payload": proof.payload_bytes.decode("utf-8"),
    }
    filepath = Path(filepath)
    filepath.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return filepath


@dataclass
class MetricsSnapshot:
    likes: int = 0
    comments: int = 0
    replies: int = 0
    reposts: int = 0
    views: int = 0

    @property
    def total_interactions(self) -> int:
        return self.likes + self.comments + self.replies + self.reposts


def read_proof_file(filepath: Path) -> dict:
    """讀取已寫入的存證 JSON 檔，回傳原始 dict。"""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Proof file not found: {filepath}")
    return json.loads(filepath.read_text(encoding="utf-8"))


def update_proof_with_metrics(filepath: Path, metrics: MetricsSnapshot) -> None:
    """在既有存證檔中加入 metrics 欄位（保留 sha256 等原有欄位不變）。"""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Proof file not found: {filepath}")
    data = json.loads(filepath.read_text(encoding="utf-8"))
    data["metrics"] = {
        "likes": metrics.likes,
        "comments": metrics.comments,
        "replies": metrics.replies,
        "reposts": metrics.reposts,
        "views": metrics.views,
        "total_interactions": metrics.total_interactions,
    }
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


async def backup_to_drive(proof: ProofResult, filename: str) -> dict:
    """把存證 payload 上傳到 Google Drive，回傳 {drive_file_id, drive_file_url}。

    TODO(W2)：用 google-api-python-client 上傳。目前為骨架。
    """
    raise NotImplementedError("Google Drive 上傳尚未串接（W2）")
