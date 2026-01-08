"""Configuration loader for different environments"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json
import yaml


class ConfigLoader:
    """Loads configuration from various sources based on environment"""

    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", os.getenv("ENV", "development")).lower()
        self.project_root = Path(__file__).parent.parent.parent.parent  # Go to Phase-3 root

    def load_config(self) -> Dict[str, Any]:
        """Load configuration based on environment"""
        config = {}

        # Load base configuration
        base_config = self._load_base_config()
        config.update(base_config)

        # Load environment-specific configuration
        env_config = self._load_environment_config()
        config.update(env_config)

        # Override with environment variables
        env_override = self._load_from_environment()
        config.update(env_override)

        return config

    def _load_base_config(self) -> Dict[str, Any]:
        """Load base configuration from base config file"""
        base_config_path = self.project_root / "config" / "base.json"

        if base_config_path.exists():
            with open(base_config_path, 'r') as f:
                return json.load(f)
        return {}

    def _load_environment_config(self) -> Dict[str, Any]:
        """Load environment-specific configuration"""
        env_config_path = self.project_root / "config" / f"{self.environment}.json"

        if env_config_path.exists():
            with open(env_config_path, 'r') as f:
                return json.load(f)
        return {}

    def _load_from_environment(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}

        # Database configuration
        if os.getenv("DATABASE_URL"):
            config["database_url"] = os.getenv("DATABASE_URL")

        # API configuration
        if os.getenv("PORT"):
            config["api_port"] = int(os.getenv("PORT"))

        if os.getenv("API_HOST"):
            config["api_host"] = os.getenv("API_HOST")

        # MCP Server configuration
        if os.getenv("MCP_SERVER_URL"):
            config["mcp_server_url"] = os.getenv("MCP_SERVER_URL")

        # Security configuration
        if os.getenv("CORS_ORIGINS"):
            config["cors_origins"] = os.getenv("CORS_ORIGINS")

        if os.getenv("ENABLE_RATE_LIMITING"):
            config["enable_rate_limiting"] = os.getenv("ENABLE_RATE_LIMITING").lower() in ("true", "1", "yes")

        # Logging configuration
        if os.getenv("LOG_LEVEL"):
            config["log_level"] = os.getenv("LOG_LEVEL")

        if os.getenv("LOG_FORMAT_JSON"):
            config["log_format_json"] = os.getenv("LOG_FORMAT_JSON").lower() in ("true", "1", "yes")

        # Caching configuration
        if os.getenv("ENABLE_CACHING"):
            config["enable_caching"] = os.getenv("ENABLE_CACHING").lower() in ("true", "1", "yes")

        # Feature flags
        if os.getenv("ENABLE_METRICS"):
            config["enable_metrics"] = os.getenv("ENABLE_METRICS").lower() in ("true", "1", "yes")

        if os.getenv("DEBUG"):
            config["debug"] = os.getenv("DEBUG").lower() in ("true", "1", "yes")

        return config

    def get_environment_name(self) -> str:
        """Get current environment name"""
        return self.environment

    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"

    def is_staging(self) -> bool:
        """Check if running in staging"""
        return self.environment == "staging"

    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == "development"

    def get_config_dir(self) -> Path:
        """Get configuration directory path"""
        return self.project_root / "config"


class EnvironmentConfig(BaseModel):
    """Environment-specific configuration model"""

    # Environment settings
    environment: str = "development"
    debug: bool = True

    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/todo_chatbot"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo: bool = False

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    api_workers: int = 1

    # MCP Server settings
    mcp_server_url: str = "http://localhost:8000"
    mcp_timeout: int = 30

    # Security settings
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    enable_rate_limiting: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    enable_cors: bool = True

    # Logging settings
    log_level: str = "INFO"
    log_format_json: bool = False
    log_file: Optional[str] = "logs/todo_chatbot.log"

    # Caching settings
    enable_caching: bool = True
    cache_ttl_default: int = 300
    cache_ttl_search: int = 300
    cache_ttl_list: int = 120

    # Feature flags
    enable_metrics: bool = True
    enable_health_checks: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_environment_config() -> EnvironmentConfig:
    """Load environment-specific configuration"""
    loader = ConfigLoader()
    config_dict = loader.load_config()

    # Create EnvironmentConfig with loaded values
    return EnvironmentConfig(**config_dict)


# Global configuration loader instance
config_loader = ConfigLoader()


def get_config() -> EnvironmentConfig:
    """Get the current environment configuration"""
    return load_environment_config()


def get_config_loader() -> ConfigLoader:
    """Get the configuration loader instance"""
    return config_loader