"""Application configuration management for different environments"""
import os
from typing import Optional

from enum import Enum
from .config_loader import load_environment_config, EnvironmentConfig


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AppConfig:
    """Application configuration settings with environment management"""

    def __init__(self, env_config: Optional[EnvironmentConfig] = None):
        if env_config is None:
            self._config = load_environment_config()
        else:
            self._config = env_config

    @property
    def environment(self) -> str:
        return self._config.environment

    @property
    def debug(self) -> bool:
        return self._config.debug

    @property
    def database_url(self) -> str:
        return self._config.database_url

    @property
    def database_pool_size(self) -> int:
        return self._config.database_pool_size

    @property
    def database_max_overflow(self) -> int:
        return self._config.database_max_overflow

    @property
    def database_echo(self) -> bool:
        return self._config.database_echo

    @property
    def api_host(self) -> str:
        return self._config.api_host

    @property
    def api_port(self) -> int:
        return self._config.api_port

    @property
    def api_workers(self) -> int:
        return self._config.api_workers

    @property
    def mcp_server_url(self) -> str:
        return self._config.mcp_server_url

    @property
    def mcp_timeout(self) -> int:
        return self._config.mcp_timeout

    @property
    def cors_origins(self) -> str:
        return self._config.cors_origins

    @property
    def log_level(self) -> str:
        return self._config.log_level

    @property
    def log_format_json(self) -> bool:
        return self._config.log_format_json

    @property
    def log_file(self) -> Optional[str]:
        return self._config.log_file

    @property
    def enable_rate_limiting(self) -> bool:
        return self._config.enable_rate_limiting

    @property
    def rate_limit_requests(self) -> int:
        return self._config.rate_limit_requests

    @property
    def rate_limit_window(self) -> int:
        return self._config.rate_limit_window

    @property
    def enable_cors(self) -> bool:
        return self._config.enable_cors

    @property
    def enable_caching(self) -> bool:
        return self._config.enable_caching

    @property
    def cache_ttl_default(self) -> int:
        return self._config.cache_ttl_default

    @property
    def cache_ttl_search(self) -> int:
        return self._config.cache_ttl_search

    @property
    def cache_ttl_list(self) -> int:
        return self._config.cache_ttl_list

    @property
    def enable_metrics(self) -> bool:
        return self._config.enable_metrics

    @property
    def enable_health_checks(self) -> bool:
        return self._config.enable_health_checks

    @property
    def cors_origins_list(self) -> list:
        """Get CORS origins as a list"""
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == "production"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging environment"""
        return self.environment == "staging"

    def get_database_config(self) -> dict:
        """Get database configuration as dictionary"""
        return {
            "pool_size": self.database_pool_size,
            "max_overflow": self.database_max_overflow,
            "echo": self.database_echo,
        }

    def get_rate_limit_config(self) -> dict:
        """Get rate limiting configuration"""
        return {
            "requests": self.rate_limit_requests,
            "window": self.rate_limit_window,
        }

    def get_cache_config(self) -> dict:
        """Get cache configuration"""
        return {
            "default_ttl": self.cache_ttl_default,
            "search_ttl": self.cache_ttl_search,
            "list_ttl": self.cache_ttl_list,
        }


# Global configuration instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get the application configuration instance"""
    return config


def configure_app(environment: Optional[str] = None) -> AppConfig:
    """Configure the application with specific environment settings"""
    global config

    if environment:
        # Create new config with specific environment
        from .config_loader import EnvironmentConfig
        env_config = EnvironmentConfig(environment=environment)
        config = AppConfig(env_config=env_config)
    else:
        # Load config from environment variables and files
        config = AppConfig()

    return config