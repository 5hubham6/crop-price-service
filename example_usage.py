"""Example usage of the crop price fetcher module.

This script demonstrates how to use the crop_price_fetcher module
to fetch crop prices for different states, districts, and crops.
"""

import asyncio
import json
from datetime import date

from crop_price_fetcher import get_crop_prices, get_crop_prices_sync


def print_price_response(response):
    """Pretty print a PriceResponse object."""
    print("\n" + "=" * 80)
    print(f"Success: {response.success}")
    print(f"Count: {response.count}")
    print(f"State: {response.state}")
    print(f"District: {response.district or 'All districts'}")
    print(f"Crop: {response.crop_name or 'All crops'}")
    print(f"Fetched at: {response.fetched_at}")
    print(f"Message: {response.message}")
    print("\nPrice Data:")
    print("-" * 80)

    if response.data:
        for i, price in enumerate(response.data, 1):
            print(f"\n{i}. {price.crop_name} - {price.market_name}")
            print(f"   District: {price.district}, State: {price.state}")
            print(f"   Min Price: ₹{price.min_price:.2f}/Quintal")
            print(f"   Max Price: ₹{price.max_price:.2f}/Quintal")
            print(f"   Modal Price: ₹{price.modal_price:.2f}/Quintal")
            print(f"   Date: {price.price_date}")
    else:
        print("No price data available.")

    print("\n" + "=" * 80)


async def example_async_usage():
    """Example of async usage."""
    print("\n=== Example 1: Fetch all crops for Delhi (Dev Mode - Instant) ===")
    response = await get_crop_prices(state="Delhi", use_mock_only=True)
    print_price_response(response)

    print("\n=== Example 2: Fetch specific crop for a district (Dev Mode) ===")
    response = await get_crop_prices(
        state="Delhi", district="North Delhi", crop_name="Wheat", use_mock_only=True
    )
    print_price_response(response)

    print("\n=== Example 3: Fetch prices for Punjab (Dev Mode) ===")
    response = await get_crop_prices(state="Punjab", use_mock_only=True)
    print_price_response(response)

    print("\n=== Example 4: Fetch specific date (Dev Mode) ===")
    response = await get_crop_prices(
        state="Delhi", price_date=date.today(), crop_name="Tomato", use_mock_only=True
    )
    print_price_response(response)


def example_sync_usage():
    """Example of synchronous usage."""
    print("\n=== Example 5: Synchronous usage - Fetch all crops for Maharashtra (Dev Mode) ===")
    response = get_crop_prices_sync(state="Maharashtra", use_mock_only=True)
    print_price_response(response)

    print("\n=== Example 6: Get JSON output for API response (Dev Mode) ===")
    response = get_crop_prices_sync(state="Tamil Nadu", crop_name="Turmeric", use_mock_only=True)
    json_output = response.model_dump_json(indent=2)
    print("\nJSON Output:")
    print(json_output)


def example_json_output():
    """Example showing clean JSON output for API integration."""
    print("\n=== Example 7: Clean JSON output for API (Dev Mode) ===")
    response = get_crop_prices_sync(
        state="Delhi", district="North Delhi", crop_name="Wheat", use_mock_only=True
    )

    # Convert to dict and then to JSON for clean output
    response_dict = response.model_dump()
    json_output = json.dumps(response_dict, indent=2, default=str)

    print(json_output)

    # Example of filtering the response
    if response.success and response.data:
        print("\n=== Filtered: Only price ranges ===")
        filtered_data = [
            {
                "crop": p.crop_name,
                "market": p.market_name,
                "min_price": p.min_price,
                "max_price": p.max_price,
                "modal_price": p.modal_price,
            }
            for p in response.data
        ]
        print(json.dumps(filtered_data, indent=2))


if __name__ == "__main__":
    print("Crop Price Fetcher - Example Usage")
    print("=" * 80)

    # Run async examples
    asyncio.run(example_async_usage())

    # Run sync examples
    example_sync_usage()

    # Show JSON output
    example_json_output()

    print("\n" + "=" * 80)
    print("Examples completed!")
