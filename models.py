"""Pydantic models for crop price data validation and serialization."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class CropPrice(BaseModel):
    """Model representing a single crop price entry from a mandi."""

    crop_name: str = Field(..., description="Name of the crop/commodity")
    min_price: float = Field(..., ge=0, description="Minimum price per quintal (Rs.)")
    max_price: float = Field(..., ge=0, description="Maximum price per quintal (Rs.)")
    modal_price: float = Field(..., ge=0, description="Modal (most common) price per quintal (Rs.)")
    market_name: str = Field(..., description="Name of the mandi/market")
    district: str = Field(..., description="District name")
    state: str = Field(..., description="State name")
    price_date: date = Field(..., description="Date when the price was recorded")
    unit: str = Field(default="Quintal", description="Unit of measurement")

    @field_validator("max_price")
    @classmethod
    def validate_max_price(cls, v: float, info) -> float:
        """Ensure max_price is greater than or equal to min_price."""
        if "min_price" in info.data and v < info.data["min_price"]:
            raise ValueError("max_price must be greater than or equal to min_price")
        return v

    @field_validator("modal_price")
    @classmethod
    def validate_modal_price(cls, v: float, info) -> float:
        """Ensure modal_price is between min_price and max_price."""
        if "min_price" in info.data and "max_price" in info.data:
            min_p = info.data["min_price"]
            max_p = info.data["max_price"]
            if not (min_p <= v <= max_p):
                raise ValueError("modal_price must be between min_price and max_price")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "crop_name": "Wheat",
                "min_price": 2100.0,
                "max_price": 2300.0,
                "modal_price": 2200.0,
                "market_name": "Azadpur Mandi",
                "district": "North Delhi",
                "state": "Delhi",
                "price_date": "2024-01-15",
                "unit": "Quintal",
            }
        }


class PriceResponse(BaseModel):
    """Model representing the response containing multiple crop prices."""

    success: bool = Field(..., description="Whether the request was successful")
    data: List[CropPrice] = Field(default_factory=list, description="List of crop price entries")
    count: int = Field(..., description="Number of price entries returned")
    state: str = Field(..., description="State for which prices were fetched")
    district: Optional[str] = Field(None, description="District filter applied (if any)")
    crop_name: Optional[str] = Field(None, description="Crop filter applied (if any)")
    fetched_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp when data was fetched"
    )
    message: Optional[str] = Field(None, description="Additional message or error description")

    @field_validator("count", mode="before")
    @classmethod
    def set_count(cls, v: int, info) -> int:
        """Automatically set count based on data length."""
        if "data" in info.data:
            return len(info.data["data"])
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "success": True,
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
                        "unit": "Quintal",
                    }
                ],
                "count": 1,
                "state": "Delhi",
                "district": "North Delhi",
                "crop_name": "Wheat",
                "fetched_at": "2024-01-15T10:30:00",
                "message": "Data fetched successfully",
            }
        }
