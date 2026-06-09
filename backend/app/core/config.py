"""全專案唯一設定來源：從環境變數讀取設定。

使用 pydantic-settings，缺少必填值時會在啟動時就報錯，
而不是等到真正呼叫某個 API 才壞掉。
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_env: str = "development"
    secret_key: str = "change-me"
    backend_cors_origins: str = "http://localhost:3000"

    # Database
    database_url: str = (
        "postgresql+psycopg://photoflow:photoflow@localhost:5432/photoflow"
    )

    # Redis / Celery
    redis_url: str = "redis://localhost:6379/0"

    # Meta (Threads / Instagram)
    meta_app_id: str = ""
    meta_app_secret: str = ""
    meta_redirect_uri: str = "http://localhost:8000/api/v1/auth/meta/callback"

    # X (Twitter) API v2
    x_api_key: str = ""
    x_api_secret: str = ""
    x_bearer_token: str = ""

    # Google Drive
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"
    google_drive_backup_folder_id: str = ""

    # Claude AI
    anthropic_api_key: str = ""
    anthropic_model_deep: str = "claude-opus-4-8"
    anthropic_model_fast: str = "claude-sonnet-4-6"

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_basic: str = ""
    stripe_price_pro: str = ""

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.backend_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """以快取方式回傳設定，整個程式共用同一份。"""
    return Settings()


settings = get_settings()
