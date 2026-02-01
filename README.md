# Crop Price Service

A Python module for fetching live mandi (market) crop prices in India. This is part of the Krishi Shayak project - an agriculture assistance application for farmers.

## What it does

This module fetches crop prices from Indian agricultural data sources like AGMARKNET and e-NAM. It returns structured data with crop names, prices (min/max/modal), market names, and location info that you can use directly in your backend API.

## Features

- Fetch prices by state, district, and crop name
- Async/await support for better performance
- Type-safe data models using Pydantic
- Error handling with retries and fallbacks
- Mock data provider for development and testing
- Clean JSON output ready for API responses

## Installation

First, clone the repository:

```bash
git clone https://github.com/5hubham6/crop-price-service.git
cd crop-price-service
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from crop_price_fetcher import get_crop_prices_sync

# Fetch all crops for a state
response = get_crop_prices_sync(state="Delhi")

# Fetch specific crop in a district
response = get_crop_prices_sync(
    state="Delhi",
    district="North Delhi",
    crop_name="Wheat"
)

# Check results
if response.success:
    for price in response.data:
        print(f"{price.crop_name}: ₹{price.modal_price}/Quintal")
```

### Development Mode (Fast Testing)

For development, you can skip real sources and use mock data directly to avoid waiting for timeouts:

```python
# Use mock data directly (instant response)
response = get_crop_prices_sync(state="Delhi", use_mock_only=True)
```

Or set an environment variable:

```bash
# Windows PowerShell
$env:CROP_PRICE_DEV_MODE="1"

# Linux/Mac
export CROP_PRICE_DEV_MODE=1
```

### Async Usage

```python
import asyncio
from crop_price_fetcher import get_crop_prices

async def main():
    response = await get_crop_prices(
        state="Punjab",
        district="Ludhiana",
        crop_name="Wheat"
    )
    return response

response = asyncio.run(main())
```

## Running the Examples

Check out the example scripts to see how everything works:

```bash
# Run all examples (uses dev mode by default)
python example_usage.py

# Test dev mode vs normal mode
python test_dev_mode.py

# Run basic tests
python test_module.py
```

## Integration with FastAPI

I've included a FastAPI integration example. Here's how to use it:

```bash
# Install FastAPI and uvicorn if you haven't
pip install fastapi uvicorn

# Run the example server
python fastapi_integration_example.py
```

Then access the API at `http://localhost:8000` and check the docs at `http://localhost:8000/docs`.

Example API call:
```
GET /api/v1/crop-prices?state=Delhi&district=North%20Delhi&crop_name=Wheat
```

## Project Structure

```
.
├── crop_price_fetcher.py    # Main fetching module
├── models.py                # Pydantic data models
├── exceptions.py            # Custom exceptions
├── mock_data_provider.py    # Mock data for testing
├── config.py                # Configuration settings
├── example_usage.py         # Usage examples
├── fastapi_integration_example.py  # FastAPI integration
├── test_module.py           # Basic tests
├── test_dev_mode.py         # Dev mode test
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Data Sources

The module is designed to work with:

1. **AGMARKNET** - Official Indian government portal for agricultural marketing
2. **e-NAM** - National Agriculture Market platform

Currently, the real data source integration is in progress. The module includes a mock data provider that returns realistic sample data for development and testing purposes.

## Response Format

The module returns a `PriceResponse` object that can be easily converted to JSON:

```json
{
  "success": true,
  "data": [
    {
      "crop_name": "Wheat",
      "min_price": 2100.0,
      "max_price": 2300.0,
      "modal_price": 2200.0,
      "market_name": "Azadpur Mandi",
      "district": "North Delhi",
      "state": "Delhi",
      "price_date": "2024-01-15",
      "unit": "Quintal"
    }
  ],
  "count": 1,
  "state": "Delhi",
  "district": "North Delhi",
  "crop_name": "Wheat",
  "fetched_at": "2024-01-15T10:30:00",
  "message": "Successfully fetched 1 price entries"
}
```

## Configuration

You can configure the module using environment variables:

- `CROP_PRICE_DEV_MODE=1` - Enable development mode (use mock data directly)
- `CROP_PRICE_TIMEOUT=30` - Request timeout in seconds
- `CROP_PRICE_MAX_RETRIES=3` - Maximum retry attempts
- `CROP_PRICE_DEFAULT_SOURCE=agmarknet` - Default data source

## Error Handling

The module handles various error scenarios:

- Network errors with automatic retries
- Data source failures with fallback mechanisms
- No data found scenarios
- Validation errors

All errors are logged and returned in a structured format.

## Development Notes

This module is part of a larger project (Krishi Shayak) and is being developed independently. It will be merged with the main project later. The current implementation focuses on:

- Clean, modular code structure
- Type safety with Pydantic
- Async support for performance
- Easy integration with web frameworks
- Comprehensive error handling

## Future Improvements

- Complete AGMARKNET web scraping implementation
- e-NAM API integration
- Database storage for caching
- Scheduled refresh jobs
- Historical price tracking

## License

This project is part of the Krishi Shayak application for educational purposes.

## Contributing

This is currently a personal project, but feel free to open issues or suggest improvements.
