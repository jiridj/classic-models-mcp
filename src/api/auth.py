"""Authentication manager for Classic Models API."""
import httpx
from typing import Optional
from .types import LoginResponse
from ..config import config


class AuthManager:
    """Manages JWT authentication for the Classic Models API."""
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.client = httpx.AsyncClient(
            base_url=config.api_url,
            headers={"Content-Type": "application/json"},
        )
    
    async def login(self) -> None:
        """Login with hardcoded credentials and store tokens."""
        try:
            response = await self.client.post(
                "/classic-models/api/auth/login/",
                json={
                    "username": config.api_username,
                    "password": config.api_password,
                },
            )
            response.raise_for_status()
            data = LoginResponse(**response.json())
            
            self.access_token = data.access
            self.refresh_token = data.refresh
            
            # Update client headers
            self.client.headers["Authorization"] = f"Bearer {self.access_token}"
        except httpx.HTTPError as e:
            raise Exception(f"Failed to login: {e}")
    
    async def refresh_access_token(self) -> None:
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            raise Exception("No refresh token available. Please login first.")
        
        try:
            response = await self.client.post(
                "/classic-models/api/auth/refresh/",
                json={"refresh": self.refresh_token},
            )
            response.raise_for_status()
            data = response.json()
            
            self.access_token = data["access"]
            self.refresh_token = data["refresh"]
            
            # Update client headers
            self.client.headers["Authorization"] = f"Bearer {self.access_token}"
        except httpx.HTTPError:
            # If refresh fails, try to login again
            await self.login()
    
    async def ensure_authenticated(self) -> None:
        """Ensure we have a valid access token."""
        if not self.access_token:
            await self.login()
    
    def get_headers(self) -> dict:
        """Get headers with authentication."""
        if not self.access_token:
            raise Exception("Not authenticated. Call ensure_authenticated() first.")
        return {"Authorization": f"Bearer {self.access_token}"}
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

