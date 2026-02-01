"""FastAPI integration example for the crop price module.

This file demonstrates how to integrate the crop price fetcher
into a FastAPI backend application.
"""

from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from crop_price_fetcher import get_crop_prices
from exceptions import CropPriceError, DataNotFoundError, NetworkError
from models import PriceResponse

# Initialize FastAPI app
app = FastAPI(
    title="Krishi Shayak - Crop Prices API",
    description="API for fetching live mandi crop prices",
    version="1.0.0",
)

# Configure CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint for health check."""
    return {"message": "Krishi Shayak Crop Prices API", "status": "healthy"}


@app.get(
    "/api/v1/crop-prices",
    response_model=PriceResponse,
    status_code=status.HTTP_200_OK,
    tags=["Crop Prices"],
    summary="Fetch live crop prices",
    description="Fetch live or near-real-time mandi crop prices filtered by state, district, and crop name.",
)
async def fetch_crop_prices(
    state: str = Query(..., description="State name (e.g., 'Delhi', 'Punjab')", min_length=1),
    district: Optional[str] = Query(
        None, description="District name for filtering (optional)"
    ),
    crop_name: Optional[str] = Query(
        None, description="Crop name for filtering (e.g., 'Wheat', 'Rice') (optional)"
    ),
    price_date: Optional[date] = Query(
        None, description="Date for price data in YYYY-MM-DD format (defaults to today)"
    ),
    data_source: Optional[str] = Query(
        "agmarknet",
        description="Data source: 'agmarknet' or 'enam' (default: 'agmarknet')",
    ),
    use_mock_fallback: bool = Query(
        True,
        description="Use mock data if real sources fail (useful for development)",
    ),
    use_mock_only: Optional[bool] = Query(
        None,
        description="Skip real sources and use mock data directly (for development). Set CROP_PRICE_DEV_MODE=1 env var for default.",
    ),
):
    """Fetch live crop prices from mandi sources.

    Returns price data including:
    - Crop name
    - Minimum, maximum, and modal prices (per quintal)
    - Market (mandi) name
    - District and state
    - Date of price update

    Example:
        GET /api/v1/crop-prices?state=Delhi&district=North%20Delhi&crop_name=Wheat
    """
    try:
        response = await get_crop_prices(
            state=state,
            district=district,
            crop_name=crop_name,
            price_date=price_date,
            data_source=data_source,
            use_mock_fallback=use_mock_fallback,
            use_mock_only=use_mock_only,
        )

        # If no data found, return 404
        if not response.success or response.count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response.message or "No price data found for the given parameters",
            )

        return response

    except DataNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except NetworkError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Network error: {str(e)}",
        ) from e
    except CropPriceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching prices: {str(e)}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        ) from e


@app.get(
    "/api/v1/crop-prices/states",
    tags=["Crop Prices"],
    summary="List available states",
    description="Get a list of states for which price data is available.",
)
async def list_states():
    """List available states (example implementation)."""
    # In production, this could query your database or data source
    states = [
        "Delhi",
        "Punjab",
        "Maharashtra",
        "Tamil Nadu",
        "Karnataka",
        "Gujarat",
        "Rajasthan",
        "Uttar Pradesh",
        "Haryana",
        "West Bengal",
    ]
    return {"states": states, "count": len(states)}


@app.get(
    "/api/v1/crop-prices/crops",
    tags=["Crop Prices"],
    summary="List available crops",
    description="Get a list of crops for which price data is available.",
)
async def list_crops(state: Optional[str] = Query(None, description="Filter by state")):
    """List available crops (example implementation)."""
    # In production, this could query your database or data source
    crops = [
        "Wheat",
        "Rice",
        "Tomato",
        "Potato",
        "Onion",
        "Cotton",
        "Sugarcane",
        "Turmeric",
        "Maize",
        "Soybean",
    ]
    return {"crops": crops, "count": len(crops), "state": state}


# Error handler for validation errors
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


# Run with: uvicorn fastapi_integration_example:app --reload
# Or: python -m uvicorn fastapi_integration_example:app --reload

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
