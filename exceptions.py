"""Custom exception classes for crop price fetching operations."""


class CropPriceError(Exception):
    """Base exception for all crop price related errors."""

    pass


class DataSourceError(CropPriceError):
    """Raised when there's an error accessing the data source."""

    def __init__(self, message: str, source: str = "unknown"):
        """Initialize DataSourceError.

        Args:
            message: Error message
            source: Name of the data source that failed
        """
        self.source = source
        super().__init__(f"[{source}] {message}")


class NetworkError(CropPriceError):
    """Raised when there's a network-related error."""

    def __init__(self, message: str, status_code: int | None = None):
        """Initialize NetworkError.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        self.status_code = status_code
        super().__init__(message)


class DataNotFoundError(CropPriceError):
    """Raised when no data is found for the given parameters."""

    def __init__(self, message: str, state: str | None = None, district: str | None = None):
        """Initialize DataNotFoundError.

        Args:
            message: Error message
            state: State for which data was requested
            district: District for which data was requested
        """
        self.state = state
        self.district = district
        super().__init__(message)


class DataValidationError(CropPriceError):
    """Raised when fetched data fails validation."""

    pass
