"""
DaprIntegrationService - Wrapper for Dapr building block interactions.

Provides state management, service invocation, and secret retrieval via Dapr.
"""
import json
import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = 3500
STATE_STORE_NAME = "todo-statestore"
SECRET_STORE_NAME = "todo-secretstore"


class DaprIntegrationService:
    """Interacts with Dapr building blocks (state, secrets, service invocation)."""

    def __init__(self, dapr_url: Optional[str] = None):
        self.dapr_url = dapr_url or f"http://localhost:{DAPR_HTTP_PORT}"
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client

    # --- State Management ---

    async def save_state(self, key: str, value: Any) -> bool:
        try:
            client = await self._get_client()
            url = f"{self.dapr_url}/v1.0/state/{STATE_STORE_NAME}"
            data = [{"key": key, "value": value}]
            response = await client.post(url, json=data)
            return response.status_code in (200, 204)
        except httpx.ConnectError:
            logger.warning("Dapr sidecar not available for state save")
            return False

    async def get_state(self, key: str) -> Optional[Any]:
        try:
            client = await self._get_client()
            url = f"{self.dapr_url}/v1.0/state/{STATE_STORE_NAME}/{key}"
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except httpx.ConnectError:
            logger.warning("Dapr sidecar not available for state get")
            return None

    async def delete_state(self, key: str) -> bool:
        try:
            client = await self._get_client()
            url = f"{self.dapr_url}/v1.0/state/{STATE_STORE_NAME}/{key}"
            response = await client.delete(url)
            return response.status_code in (200, 204)
        except httpx.ConnectError:
            logger.warning("Dapr sidecar not available for state delete")
            return False

    # --- Secret Management ---

    async def get_secret(self, secret_name: str) -> Optional[dict]:
        try:
            client = await self._get_client()
            url = f"{self.dapr_url}/v1.0/secrets/{SECRET_STORE_NAME}/{secret_name}"
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except httpx.ConnectError:
            logger.warning("Dapr sidecar not available for secret retrieval")
            return None

    # --- Service Invocation ---

    async def invoke_service(
        self, app_id: str, method: str, data: Optional[dict] = None, http_method: str = "POST"
    ) -> Optional[dict]:
        try:
            client = await self._get_client()
            url = f"{self.dapr_url}/v1.0/invoke/{app_id}/method/{method}"
            if http_method == "GET":
                response = await client.get(url)
            else:
                response = await client.post(url, json=data or {})
            if response.status_code == 200:
                return response.json()
            return None
        except httpx.ConnectError:
            logger.warning("Dapr sidecar not available for service invocation")
            return None

    # --- Health Check ---

    async def health_check(self) -> bool:
        try:
            client = await self._get_client()
            response = await client.get(f"{self.dapr_url}/v1.0/healthz")
            return response.status_code == 200
        except httpx.ConnectError:
            return False

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
