"""Configuration management for the MCP server."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    def __init__(self):
        self.api_url = os.getenv("CLASSIC_MODELS_API_URL", "http://localhost:8000").rstrip("/")
        self.api_username = os.getenv("API_USERNAME", "demo")
        self.api_password = os.getenv("API_PASSWORD", "demo123")
        self.sse_port = int(os.getenv("SSE_PORT", "3000"))
        self.sse_bearer_token = os.getenv("SSE_BEARER_TOKEN", "demo-token")
        
        # Determine transport from CLI args or env var
        import sys
        transport_arg = next((arg for arg in sys.argv if arg.startswith("--transport=")), None)
        if transport_arg:
            self.transport = transport_arg.split("=")[1]
        else:
            self.transport = os.getenv("TRANSPORT", "stdio")


# Global config instance
config = Config()

