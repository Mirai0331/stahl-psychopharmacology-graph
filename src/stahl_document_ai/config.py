"""配置管理模块"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # GCP Document AI 配置
    gcp_project_id: str = ""
    gcp_location: str = "us"  # 例如: us, eu, global
    gcp_processor_id: str = ""
    google_application_credentials: Optional[str] = None

    # 处理配置
    chunk_size_pages: int = 15  # Document AI online process 推荐单批次页数（最大15页）
    max_concurrent_requests: int = 3
    request_timeout_seconds: float = 120.0
    
    # 缓存与输出
    cache_dir: Path = Path("cache")
    output_dir: Path = Path("output")


settings = Settings()
