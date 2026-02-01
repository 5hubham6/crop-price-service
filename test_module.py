"""Simple test script to verify the crop price module works correctly."""

import asyncio
from datetime import date

from crop_price_fetcher import get_crop_prices, get_crop_prices_sync
from models import PriceResponse


def test_sync_function():
    """Test the synchronous function."""
    print("Testing synchronous function...")
    try:
        response = get_crop_prices_sync(state="Delhi")
        assert isinstance(response, PriceResponse), "Response should be PriceResponse"
        assert response.state == "Delhi", "State should match"
        print("PASSED: Synchronous function test")
        return True
    except Exception as e:
        print(f"FAILED: Synchronous function test - {e}")
        return False


async def test_async_function():
    """Test the async function."""
    print("Testing async function...")
    try:
        response = await get_crop_prices(state="Punjab")
        assert isinstance(response, PriceResponse), "Response should be PriceResponse"
        assert response.state == "Punjab", "State should match"
        print("PASSED: Async function test")
        return True
    except Exception as e:
        print(f"FAILED: Async function test - {e}")
        return False


def test_filtering():
    """Test filtering by district and crop."""
    print("Testing filtering...")
    try:
        response = get_crop_prices_sync(
            state="Delhi", district="North Delhi", crop_name="Wheat"
        )
        assert isinstance(response, PriceResponse), "Response should be PriceResponse"
        print("PASSED: Filtering test")
        return True
    except Exception as e:
        print(f"FAILED: Filtering test - {e}")
        return False


def test_json_output():
    """Test JSON serialization."""
    print("Testing JSON output...")
    try:
        response = get_crop_prices_sync(state="Maharashtra")
        json_str = response.model_dump_json()
        assert isinstance(json_str, str), "Should return JSON string"
        assert "success" in json_str, "JSON should contain 'success' field"
        print("PASSED: JSON output test")
        return True
    except Exception as e:
        print(f"FAILED: JSON output test - {e}")
        return False


async def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Crop Price Module Tests")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Sync Function", test_sync_function()))
    results.append(("Async Function", await test_async_function()))
    results.append(("Filtering", test_filtering()))
    results.append(("JSON Output", test_json_output()))

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
