"""Mock data provider for testing and demonstration purposes.

This module provides sample crop price data that can be used for development
and testing when real data sources are unavailable or rate-limited.
"""

from datetime import date, timedelta
from typing import List, Optional

from models import CropPrice


def get_mock_prices(
    state: str,
    district: Optional[str] = None,
    crop_name: Optional[str] = None,
    price_date: Optional[date] = None,
) -> List[CropPrice]:
    """Generate mock crop price data for testing.

    This function returns realistic sample data that matches the structure
    of real mandi price data. Use this for development and testing.

    Args:
        state: State name
        district: Optional district name
        crop_name: Optional crop name filter
        price_date: Optional date (defaults to today)

    Returns:
        List of CropPrice objects with mock data
    """
    if price_date is None:
        price_date = date.today()

    # Sample crop data with realistic Indian mandi prices (per quintal)
    all_crops = [
        {
            "crop_name": "Wheat",
            "min_price": 2100.0,
            "max_price": 2300.0,
            "modal_price": 2200.0,
            "market_name": "Azadpur Mandi",
            "district": "North Delhi",
            "state": "Delhi",
        },
        {
            "crop_name": "Rice",
            "min_price": 1800.0,
            "max_price": 2000.0,
            "modal_price": 1900.0,
            "market_name": "Azadpur Mandi",
            "district": "North Delhi",
            "state": "Delhi",
        },
        {
            "crop_name": "Tomato",
            "min_price": 1200.0,
            "max_price": 1500.0,
            "modal_price": 1350.0,
            "market_name": "Azadpur Mandi",
            "district": "North Delhi",
            "state": "Delhi",
        },
        {
            "crop_name": "Potato",
            "min_price": 800.0,
            "max_price": 1000.0,
            "modal_price": 900.0,
            "market_name": "Azadpur Mandi",
            "district": "North Delhi",
            "state": "Delhi",
        },
        {
            "crop_name": "Onion",
            "min_price": 1500.0,
            "max_price": 1800.0,
            "modal_price": 1650.0,
            "market_name": "Azadpur Mandi",
            "district": "North Delhi",
            "state": "Delhi",
        },
        {
            "crop_name": "Wheat",
            "min_price": 2050.0,
            "max_price": 2250.0,
            "modal_price": 2150.0,
            "market_name": "Khanna Mandi",
            "district": "Ludhiana",
            "state": "Punjab",
        },
        {
            "crop_name": "Rice",
            "min_price": 1750.0,
            "max_price": 1950.0,
            "modal_price": 1850.0,
            "market_name": "Khanna Mandi",
            "district": "Ludhiana",
            "state": "Punjab",
        },
        {
            "crop_name": "Cotton",
            "min_price": 5500.0,
            "max_price": 6000.0,
            "modal_price": 5750.0,
            "market_name": "Yavatmal Mandi",
            "district": "Yavatmal",
            "state": "Maharashtra",
        },
        {
            "crop_name": "Sugarcane",
            "min_price": 280.0,
            "max_price": 320.0,
            "modal_price": 300.0,
            "market_name": "Kolhapur Mandi",
            "district": "Kolhapur",
            "state": "Maharashtra",
        },
        {
            "crop_name": "Turmeric",
            "min_price": 12000.0,
            "max_price": 14000.0,
            "modal_price": 13000.0,
            "market_name": "Erode Mandi",
            "district": "Erode",
            "state": "Tamil Nadu",
        },
    ]

    # Filter by state
    filtered = [crop for crop in all_crops if crop["state"].lower() == state.lower()]

    # Filter by district if specified
    if district:
        filtered = [crop for crop in filtered if crop["district"].lower() == district.lower()]

    # Filter by crop if specified
    if crop_name:
        filtered = [crop for crop in filtered if crop["crop_name"].lower() == crop_name.lower()]

    # Convert to CropPrice objects
    prices = []
    for crop_data in filtered:
        prices.append(
            CropPrice(
                crop_name=crop_data["crop_name"],
                min_price=crop_data["min_price"],
                max_price=crop_data["max_price"],
                modal_price=crop_data["modal_price"],
                market_name=crop_data["market_name"],
                district=crop_data["district"],
                state=crop_data["state"],
                price_date=price_date,
            )
        )

    return prices
