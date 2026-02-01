"""Quick test to demonstrate dev mode vs normal mode."""

import time
from crop_price_fetcher import get_crop_prices_sync

print("=" * 80)
print("Testing Dev Mode vs Normal Mode")
print("=" * 80)

# Test 1: Dev Mode (should be instant)
print("\n1. Testing DEV MODE (use_mock_only=True) - Should be INSTANT:")
start = time.time()
response = get_crop_prices_sync(state="Delhi", use_mock_only=True)
elapsed = time.time() - start
print(f"   Completed in {elapsed:.2f} seconds")
print(f"   Found {response.count} price entries")
print(f"   Success: {response.success}")

# Test 2: Normal Mode (will try real sources first, then fallback)
print("\n2. Testing NORMAL MODE (will try real sources first):")
print("   Note: This will take ~90 seconds if real sources are unavailable...")
print("   (Skipping this test to save time. Uncomment to test.)")
# start = time.time()
# response = get_crop_prices_sync(state="Delhi", use_mock_only=False)
# elapsed = time.time() - start
# print(f"   Completed in {elapsed:.2f} seconds")

print("\n" + "=" * 80)
print("Recommendation: Use use_mock_only=True for development/testing")
print("Set CROP_PRICE_DEV_MODE=1 environment variable for default behavior")
print("=" * 80)
