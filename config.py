"""Configuration module for crop price fetcher.

This module provides configuration options that can be set via
environment variables or directly in code.
"""

import os
from typing import Optional

# Development mode: Skip real sources and use mock data directly
# Set CROP_PRICE_DEV_MODE=1 in environment to enable
DEV_MODE: bool = os.getenv("CROP_PRICE_DEV_MODE", "0").lower() in ("1", "true", "yes")

# Request timeout in seconds
REQUEST_TIMEOUT: int = int(os.getenv("CROP_PRICE_TIMEOUT", "30"))

# Maximum retry attempts
MAX_RETRIES: int = int(os.getenv("CROP_PRICE_MAX_RETRIES", "3"))

# Retry delay in seconds (base delay, increases with each retry)
RETRY_DELAY: int = int(os.getenv("CROP_PRICE_RETRY_DELAY", "2"))

# Default data source
DEFAULT_DATA_SOURCE: str = os.getenv("CROP_PRICE_DEFAULT_SOURCE", "agmarknet")

# Enable/disable mock fallback by default
DEFAULT_USE_MOCK_FALLBACK: bool = (
    os.getenv("CROP_PRICE_USE_MOCK_FALLBACK", "1").lower() in ("1", "true", "yes")
)


def get_config_summary() -> dict:
    """Get a summary of current configuration.

    Returns:
        Dictionary containing current configuration values
    """
    return {
        "dev_mode": DEV_MODE,
        "request_timeout": REQUEST_TIMEOUT,
        "max_retries": MAX_RETRIES,
        "retry_delay": RETRY_DELAY,
        "default_data_source": DEFAULT_DATA_SOURCE,
        "default_use_mock_fallback": DEFAULT_USE_MOCK_FALLBACK,
    }
