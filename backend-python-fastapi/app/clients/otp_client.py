import asyncio
from typing import Any

import httpx

from app.schemas.isochrone import IsochroneQuery


class OtpClientError(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class OtpClient:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        router_id: str,
        retries: int,
        backoff_seconds: float,
    ) -> None:
        self._client = http_client
        self._router_id = router_id
        self._retries = retries
        self._backoff = backoff_seconds

    async def fetch_isochrone(self, query: IsochroneQuery) -> dict[str, Any]:
        url = f"/routers/{self._router_id}/isochrone"
        params = query.to_query_params()

        for attempt in range(1, self._retries + 1):
            try:
                response = await self._client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                if (
                    500 <= status_code < 600
                    and attempt < self._retries
                ):
                    await asyncio.sleep(self._backoff * attempt)
                    continue
                raise OtpClientError(
                    status_code=status_code,
                    message=f"OTP 요청이 실패했습니다: {exc.response.text}",
                ) from exc
            except httpx.RequestError as exc:
                if attempt < self._retries:
                    await asyncio.sleep(self._backoff * attempt)
                    continue
                raise OtpClientError(
                    status_code=502,
                    message=f"OTP 서비스에 연결할 수 없습니다: {exc!s}",
                ) from exc
        raise OtpClientError(status_code=502, message="OTP 요청 재시도 한도를 초과했습니다.")

