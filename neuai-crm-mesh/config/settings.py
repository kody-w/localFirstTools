"""
Configuration settings for NeuAI CRM Data Mesh.
"""

import os
from typing import List
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Application settings."""

    # Server settings
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8080")))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

    # CORS settings
    cors_origins: List[str] = field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(",")
    )

    # Logging
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Data persistence
    data_dir: str = field(default_factory=lambda: os.getenv("DATA_DIR", "./data"))

    # Feature flags
    enable_ai_queries: bool = field(
        default_factory=lambda: os.getenv("ENABLE_AI_QUERIES", "true").lower() == "true"
    )

    # Duplicate detection
    duplicate_threshold: float = field(
        default_factory=lambda: float(os.getenv("DUPLICATE_THRESHOLD", "0.8"))
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the current settings instance."""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global settings
    settings = Settings()
    return settings
