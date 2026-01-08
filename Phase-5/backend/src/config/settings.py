"""
Settings configuration for the Todo Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Todo Backend Phase 5"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todo_db")
    database_echo: bool = False

    # Kafka settings
    kafka_brokers: str = os.getenv("KAFKA_BROKERS", "localhost:9092")
    kafka_security_protocol: str = os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
    task_events_topic: str = os.getenv("TASK_EVENTS_TOPIC", "task-events")
    reminder_events_topic: str = os.getenv("REMINDER_EVENTS_TOPIC", "reminder-events")
    audit_events_topic: str = os.getenv("AUDIT_EVENTS_TOPIC", "audit-events")

    # Dapr settings
    dapr_http_port: int = int(os.getenv("DAPR_HTTP_PORT", "3500"))
    dapr_grpc_port: int = int(os.getenv("DAPR_GRPC_PORT", "50001"))

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Redis settings (for caching)
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Email settings
    email_smtp_server: str = os.getenv("EMAIL_SMTP_SERVER", "localhost")
    email_smtp_port: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    email_username: str = os.getenv("EMAIL_USERNAME", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """
    Get the application settings
    """
    return Settings()