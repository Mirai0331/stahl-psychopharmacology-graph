"""Google Cloud Document AI REST API 客户端封装"""
import base64
from typing import Dict, Any, Optional
import httpx
from stahl_document_ai.client.auth import get_gcp_access_token


class DocumentAIRestClient:
    """封装 Google Cloud Document AI v1 REST API 交互"""

    def __init__(
        self,
        project_id: str,
        location: str = "us",
        processor_id: str = "",
        credentials_path: Optional[str] = None,
        timeout: float = 120.0,
    ):
        self.project_id = project_id
        self.location = location.lower()
        self.processor_id = processor_id
        self.credentials_path = credentials_path
        self.timeout = timeout

        # 端点地址适配
        if self.location == "global":
            self.base_url = "https://documentai.googleapis.com/v1"
        else:
            self.base_url = f"https://{self.location}-documentai.googleapis.com/v1"

    def _get_headers(self) -> Dict[str, str]:
        token = get_gcp_access_token(self.credentials_path)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def process_document(
        self,
        pdf_bytes: bytes,
        mime_type: str = "application/pdf",
        enable_native_pdf_parsing: bool = False,
    ) -> Dict[str, Any]:
        """
        调用 Document AI :process 同步在线处理端点
        """
        endpoint = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}:process"
        
        encoded_content = base64.b64encode(pdf_bytes).decode("utf-8")
        
        payload: Dict[str, Any] = {
            "rawDocument": {
                "content": encoded_content,
                "mimeType": mime_type,
            },
            "processOptions": {
                "ocrConfig": {
                    "enableNativePdfParsing": enable_native_pdf_parsing,
                }
            }
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload, headers=self._get_headers())
            
            if response.status_code != 200:
                raise RuntimeError(
                    f"Document AI REST API error [HTTP {response.status_code}]: {response.text}"
                )
            
            return response.json()

    def batch_process_documents(
        self,
        gcs_input_uris: list[str],
        gcs_output_uri: str,
    ) -> Dict[str, Any]:
        """
        调用 Document AI :batchProcess 异步批量处理端点
        """
        endpoint = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}:batchProcess"

        documents = [{"gcsUri": uri, "mimeType": "application/pdf"} for uri in gcs_input_uris]
        
        payload = {
            "inputDocuments": {
                "gcsDocuments": {
                    "documents": documents
                }
            },
            "documentOutputConfig": {
                "gcsOutputConfig": {
                    "gcsUri": gcs_output_uri
                }
            }
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload, headers=self._get_headers())
            if response.status_code != 200:
                raise RuntimeError(
                    f"Document AI Batch REST API error [HTTP {response.status_code}]: {response.text}"
                )
            return response.json()

    def get_operation_status(self, operation_name: str) -> Dict[str, Any]:
        """
        查询异步 Batch 操作进度
        """
        endpoint = f"{self.base_url}/{operation_name}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(endpoint, headers=self._get_headers())
            if response.status_code != 200:
                raise RuntimeError(
                    f"Get Operation Status error [HTTP {response.status_code}]: {response.text}"
                )
            return response.json()
