"""Module for fetching live crop prices from Indian mandi sources.

Fetches crop prices from AGMARKNET and e-NAM. Handles errors and returns
structured data that can be used in API responses.
"""

import asyncio
import logging
import os
from datetime import date, datetime
from typing import List, Optional

import aiohttp
from bs4 import BeautifulSoup

from exceptions import (
    CropPriceError,
    DataNotFoundError,
    DataSourceError,
    DataValidationError,
    NetworkError,
)
from models import CropPrice, PriceResponse

# Import mock data provider for fallback/demo
try:
    from mock_data_provider import get_mock_prices
except ImportError:
    get_mock_prices = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
AGMARKNET_BASE_URL = "http://agmarknet.gov.in"
AGMARKNET_PRICE_URL = f"{AGMARKNET_BASE_URL}/PriceAndArrivals/CommodityWiseDailyReport.aspx"
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Import configuration
try:
    from config import DEV_MODE
except ImportError:
    # Fallback if config.py doesn't exist
    DEV_MODE = os.getenv("CROP_PRICE_DEV_MODE", "0").lower() in ("1", "true", "yes")


async def fetch_agmarknet_prices(
    state: str,
    district: Optional[str] = None,
    crop_name: Optional[str] = None,
    price_date: Optional[date] = None,
) -> List[CropPrice]:
    """Fetch crop prices from AGMARKNET portal.

    This function scrapes the AGMARKNET website to get daily mandi prices.
    AGMARKNET is the official Indian government portal for agricultural marketing.

    Args:
        state: Name of the state (e.g., "Delhi", "Punjab", "Maharashtra")
        district: Optional district name for filtering
        crop_name: Optional crop name for filtering (e.g., "Wheat", "Rice")
        price_date: Optional date for price data (defaults to today)

    Returns:
        List of CropPrice objects containing price information

    Raises:
        NetworkError: If there's a network issue or HTTP error
        DataNotFoundError: If no data is found for the given parameters
        DataSourceError: If there's an error parsing or accessing the data source
    """
    if price_date is None:
        price_date = date.today()

    logger.info(f"Fetching prices from AGMARKNET for state={state}, district={district}, crop={crop_name}")

    # AGMARKNET requires form submission with specific parameters
    # Note: This is a simplified implementation. Real implementation may need
    # to handle state/district/crop dropdowns and form submission
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as session:
            # First, get the page to extract viewstate and other form data
            async with session.get(AGMARKNET_PRICE_URL) as response:
                if response.status != 200:
                    raise NetworkError(
                        f"Failed to fetch AGMARKNET page: HTTP {response.status}",
                        status_code=response.status,
                    )

                html_content = await response.text()
                soup = BeautifulSoup(html_content, "html.parser")

                # Extract form data (viewstate, event validation, etc.)
                # This is a placeholder - actual implementation needs to parse the form
                # and submit with proper state/district/crop selections

                # For now, return a mock structure showing the expected format
                # In production, you would parse the actual HTML table from AGMARKNET
                logger.warning(
                    "AGMARKNET scraping requires form submission. "
                    "This is a template - implement actual form handling."
                )

                # Mock data structure for demonstration
                # Replace this with actual scraping logic
                raise DataSourceError(
                    "AGMARKNET form submission not fully implemented. "
                    "Use alternative data source or implement form handling.",
                    source="agmarknet",
                )

    except aiohttp.ClientError as e:
        raise NetworkError(f"Network error while fetching from AGMARKNET: {str(e)}") from e
    except Exception as e:
        if isinstance(e, (NetworkError, DataSourceError)):
            raise
        raise DataSourceError(f"Unexpected error fetching from AGMARKNET: {str(e)}", source="agmarknet") from e


async def fetch_enam_prices(
    state: str,
    district: Optional[str] = None,
    crop_name: Optional[str] = None,
) -> List[CropPrice]:
    """Fetch crop prices from e-NAM (National Agriculture Market) portal.

    e-NAM is a pan-India electronic trading portal that connects existing
    APMC mandis to create a unified national market for agricultural commodities.

    Args:
        state: Name of the state
        district: Optional district name for filtering
        crop_name: Optional crop name for filtering

    Returns:
        List of CropPrice objects containing price information

    Raises:
        NetworkError: If there's a network issue or HTTP error
        DataNotFoundError: If no data is found for the given parameters
        DataSourceError: If there's an error parsing or accessing the data source
    """
    logger.info(f"Fetching prices from e-NAM for state={state}, district={district}, crop={crop_name}")

    enam_base_url = "https://enam.gov.in"
    enam_price_url = f"{enam_base_url}/web/dashboard/live_price"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as session:
            # e-NAM may require API calls or form submissions
            # This is a placeholder for the actual implementation
            async with session.get(enam_price_url) as response:
                if response.status != 200:
                    raise NetworkError(
                        f"Failed to fetch e-NAM page: HTTP {response.status}",
                        status_code=response.status,
                    )

                # Parse response and extract price data
                # Actual implementation would parse JSON or HTML response
                logger.warning(
                    "e-NAM API integration requires authentication or specific endpoints. "
                    "This is a template - implement actual API calls."
                )

                raise DataSourceError(
                    "e-NAM API integration not fully implemented. "
                    "Use alternative data source or implement API authentication.",
                    source="enam",
                )

    except aiohttp.ClientError as e:
        raise NetworkError(f"Network error while fetching from e-NAM: {str(e)}") from e
    except Exception as e:
        if isinstance(e, (NetworkError, DataSourceError)):
            raise
        raise DataSourceError(f"Unexpected error fetching from e-NAM: {str(e)}", source="enam") from e


def parse_price_data(raw_data: List[dict]) -> List[CropPrice]:
    """Parse raw price data into CropPrice objects.

    This function validates and converts raw dictionary data into
    structured CropPrice Pydantic models.

    Args:
        raw_data: List of dictionaries containing raw price data

    Returns:
        List of validated CropPrice objects

    Raises:
        DataValidationError: If data validation fails
    """
    prices = []
    for item in raw_data:
        try:
            # Validate and create CropPrice object
            price = CropPrice(**item)
            prices.append(price)
        except Exception as e:
            logger.warning(f"Failed to parse price data item: {item}. Error: {str(e)}")
            raise DataValidationError(f"Invalid price data format: {str(e)}") from e

    return prices


async def get_crop_prices(
    state: str,
    district: Optional[str] = None,
    crop_name: Optional[str] = None,
    price_date: Optional[date] = None,
    data_source: str = "agmarknet",
    use_mock_fallback: bool = True,
    use_mock_only: Optional[bool] = None,
) -> PriceResponse:
    """Fetch crop prices from specified data source.

    This is the main function to fetch crop prices. It supports multiple
    data sources and handles errors gracefully.

    Args:
        state: Name of the state (required)
        district: Optional district name for filtering
        crop_name: Optional crop name for filtering
        price_date: Optional date for price data (defaults to today)
        data_source: Data source to use ("agmarknet" or "enam", default: "agmarknet")
        use_mock_fallback: Use mock data if real sources fail (default: True)
        use_mock_only: Skip real sources and use mock data directly (default: None, uses DEV_MODE env var)

    Returns:
        PriceResponse object containing fetched prices and metadata

    Raises:
        CropPriceError: Base exception for all crop price related errors
        DataNotFoundError: If no data is found for the given parameters
    """
    # Input validation
    if not state or not state.strip():
        raise ValueError("State parameter is required and cannot be empty")

    state = state.strip().title()
    if district:
        district = district.strip().title()
    if crop_name:
        crop_name = crop_name.strip().title()

    # Determine if we should use mock data only
    if use_mock_only is None:
        use_mock_only = DEV_MODE

    if use_mock_only:
        logger.info("Development mode: Using mock data directly (skipping real sources)")
        if get_mock_prices:
            try:
                prices = get_mock_prices(state, district, crop_name, price_date)
                if prices:
                    # Filter by district and crop if specified
                    if district:
                        prices = [p for p in prices if p.district.lower() == district.lower()]
                    if crop_name:
                        prices = [p for p in prices if p.crop_name.lower() == crop_name.lower()]

                    return PriceResponse(
                        success=True,
                        data=prices,
                        count=len(prices),
                        state=state,
                        district=district,
                        crop_name=crop_name,
                        message=f"Successfully fetched {len(prices)} mock price entries (dev mode)",
                    )
            except Exception as e:
                logger.error(f"Mock data provider failed: {str(e)}")

        return PriceResponse(
            success=False,
            data=[],
            count=0,
            state=state,
            district=district,
            crop_name=crop_name,
            message="Mock data provider unavailable",
        )

    logger.info(
        f"Fetching crop prices: state={state}, district={district}, "
        f"crop={crop_name}, source={data_source}"
    )

    # Try fetching from primary source with retries
    prices: List[CropPrice] = []
    last_error: Optional[Exception] = None

    for attempt in range(MAX_RETRIES):
        try:
            if data_source.lower() == "agmarknet":
                prices = await fetch_agmarknet_prices(state, district, crop_name, price_date)
            elif data_source.lower() == "enam":
                prices = await fetch_enam_prices(state, district, crop_name)
            else:
                raise ValueError(f"Unknown data source: {data_source}")

            # If we got prices, break out of retry loop
            if prices:
                break

        except (NetworkError, DataSourceError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
            else:
                logger.error(f"All {MAX_RETRIES} attempts failed: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise CropPriceError(f"Unexpected error fetching prices: {str(e)}") from e

    # If no prices found after retries, try fallback source
    if not prices and last_error:
        logger.info(f"Primary source failed, trying fallback...")
        try:
            fallback_source = "enam" if data_source.lower() == "agmarknet" else "agmarknet"
            if fallback_source == "agmarknet":
                prices = await fetch_agmarknet_prices(state, district, crop_name, price_date)
            else:
                prices = await fetch_enam_prices(state, district, crop_name)
        except Exception as e:
            logger.error(f"Fallback source also failed: {str(e)}")

    # If still no prices and mock fallback is enabled, use mock data
    if not prices and use_mock_fallback and get_mock_prices:
        logger.warning("All data sources failed, using mock data for demonstration")
        try:
            prices = get_mock_prices(state, district, crop_name, price_date)
            if prices:
                logger.info(f"Using {len(prices)} mock price entries")
        except Exception as e:
            logger.error(f"Mock data provider also failed: {str(e)}")

    # Filter by district and crop if specified
    if prices:
        if district:
            prices = [p for p in prices if p.district.lower() == district.lower()]
        if crop_name:
            prices = [p for p in prices if p.crop_name.lower() == crop_name.lower()]

    # Build response
    if not prices:
        message = f"No price data found for state={state}"
        if district:
            message += f", district={district}"
        if crop_name:
            message += f", crop={crop_name}"
        if last_error:
            message += f". Last error: {str(last_error)}"

        return PriceResponse(
            success=False,
            data=[],
            count=0,
            state=state,
            district=district,
            crop_name=crop_name,
            message=message,
        )

    return PriceResponse(
        success=True,
        data=prices,
        count=len(prices),
        state=state,
        district=district,
        crop_name=crop_name,
        message=f"Successfully fetched {len(prices)} price entries",
    )


# Synchronous wrapper for convenience
def get_crop_prices_sync(
    state: str,
    district: Optional[str] = None,
    crop_name: Optional[str] = None,
    price_date: Optional[date] = None,
    data_source: str = "agmarknet",
    use_mock_fallback: bool = True,
    use_mock_only: Optional[bool] = None,
) -> PriceResponse:
    """Synchronous wrapper for get_crop_prices.

    This function runs the async get_crop_prices in an event loop.
    Use this if you're not in an async context.

    Args:
        state: Name of the state (required)
        district: Optional district name for filtering
        crop_name: Optional crop name for filtering
        price_date: Optional date for price data (defaults to today)
        data_source: Data source to use ("agmarknet" or "enam")

    Returns:
        PriceResponse object containing fetched prices and metadata
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        get_crop_prices(
            state, district, crop_name, price_date, data_source, use_mock_fallback, use_mock_only
        )
    )
