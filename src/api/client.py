"""HTTP client for Classic Models API."""
import httpx
from typing import Any, Optional
from .auth import AuthManager
from ..config import config


class APIClient:
    """Client for interacting with Classic Models API."""
    
    def __init__(self):
        self.auth = AuthManager()
        self.base_url = config.api_url
    
    async def initialize(self) -> None:
        """Initialize the client and authenticate."""
        await self.auth.ensure_authenticated()
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        """Make an authenticated HTTP request."""
        await self.auth.ensure_authenticated()
        
        url = f"{self.base_url}{endpoint}"
        headers = self.auth.get_headers()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                    timeout=30.0,
                )
                
                # If unauthorized, try to refresh token and retry
                if response.status_code == 401:
                    await self.auth.refresh_access_token()
                    headers = self.auth.get_headers()
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=data,
                        params=params,
                        timeout=30.0,
                    )
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"API request failed: {e.response.status_code}"
            if e.response.text:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('detail', e.response.text)}"
                except:
                    error_msg += f" - {e.response.text}"
            raise Exception(error_msg)
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}")
    
    async def get(self, endpoint: str, params: Optional[dict] = None) -> Any:
        """GET request."""
        return await self._request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, data: dict) -> Any:
        """POST request."""
        return await self._request("POST", endpoint, data=data)
    
    async def put(self, endpoint: str, data: dict) -> Any:
        """PUT request."""
        return await self._request("PUT", endpoint, data=data)
    
    async def patch(self, endpoint: str, data: dict) -> Any:
        """PATCH request."""
        return await self._request("PATCH", endpoint, data=data)
    
    async def delete(self, endpoint: str) -> None:
        """DELETE request."""
        await self._request("DELETE", endpoint)
    
    async def close(self) -> None:
        """Close the client."""
        await self.auth.close()

