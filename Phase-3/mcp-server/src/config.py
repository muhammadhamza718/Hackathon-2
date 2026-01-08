import os
from typing import Optional


class MCPConfig:
    """Configuration for the MCP Server."""

    # Server settings
    MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8001"))

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # Gemini API settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Backend connection
    BACKEND_API_URL: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")

    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # MCP Protocol settings
    MCP_PROTOCOL_VERSION: str = "1.0"
    MCP_SERVER_NAME: str = "TodoMCP"
    MCP_SERVER_DESCRIPTION: str = "MCP Server for Todo Operations"

    @classmethod
    def validate(cls) -> bool:
        """Validate the configuration."""
        required_vars = ["DATABASE_URL"]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")

        return True