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


async def backup_to_drive(proof: ProofResult, filename: str) -> dict:
    """把存證 payload 上傳到 Google Drive，回傳 {drive_file_id, drive_file_url}。

    TODO(W2)：用 google-api-python-client 上傳。目前為骨架。
    """
    raise NotImplementedError("Google Drive 上傳尚未串接（W2）")
