from __future__ import annotations

from typing import Any, Dict
import requests


class AnythingLLMClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        workspace_slug: str,
        chat_path: str,
        timeout_seconds: int = 120,
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.workspace_slug = workspace_slug
        self.chat_path = chat_path
        self.timeout_seconds = timeout_seconds
        self.verify_ssl = verify_ssl

    def _build_url(self) -> str:
        path = self.chat_path.replace("{workspace_slug}", self.workspace_slug)
        return f"{self.base_url}{path}"

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def healthcheck(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/api/docs",
                timeout=min(self.timeout_seconds, 20),
                verify=self.verify_ssl,
            )
            if response.ok:
                return True, "AnythingLLM instance reachable."
            return False, f"AnythingLLM returned HTTP {response.status_code}."
        except Exception as exc:
            return False, str(exc)

    def chat(self, message: str, mode: str = "chat") -> Dict[str, Any]:
        payload = {
            "message": message,
            "mode": mode,
        }
        response = requests.post(
            self._build_url(),
            headers=self.headers,
            json=payload,
            timeout=self.timeout_seconds,
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        return response.json()
