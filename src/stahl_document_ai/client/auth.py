"""Google Cloud 认证与 Token 管理"""
import os
from typing import Optional
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account


def get_gcp_access_token(credentials_path: Optional[str] = None) -> str:
    """
    获取有效的 Google Cloud OAuth2 Access Token
    优先级：
    1. 显式指定的 Service Account JSON 文件
    2. 环境变量 GOOGLE_APPLICATION_CREDENTIALS
    3. Application Default Credentials (ADC)
    """
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    
    if credentials_path and os.path.exists(credentials_path):
        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=scopes
        )
    elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]):
        creds = service_account.Credentials.from_service_account_file(
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scopes=scopes
        )
    else:
        creds, _ = google.auth.default(scopes=scopes)

    request = google.auth.transport.requests.Request()
    if not creds.valid:
        creds.refresh(request)
        
    return creds.token
