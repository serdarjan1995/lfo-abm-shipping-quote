from enum import Enum
from pydantic import BaseModel, Field


class ServiceLevelEnum(str, Enum):
    WhiteGlove = "White Glove"
    Threshold = "Threshold"
    Doorstep = "Doorstep"


class ShippingRequest(BaseModel):
    pickup_zip: int = Field(..., description="Pickup Zipcode")
    delivery_zip: int = Field(..., description="Delivery Zipcode")
    service_level: ServiceLevelEnum = Field(..., description="Service level")
    total_cu_ft: float = Field(..., description="Total cubic feet")
    max_weight: int = Field(..., description="Max weight / lbs")


class ShippingQuotesSummary(BaseModel):
    delivery_surcharge: float | str = Field(..., description="Delivery Surcharge")
    fuel_surcharge: float | str = Field(..., description="Fuel Surcharge")
    remote_charges: float | str = Field(..., description="Remote Charges")
    outsource_charges: float | str = Field(..., description="Ferry / Outsource Charges")
    insurance: float | str = Field(..., description="Insurance Charges")
    total_charge: float | str = Field(..., description="Total Charge")


class ShippingQuotesDetails(BaseModel):
    origin_state: str = Field(..., description="Origin State")
    origin_zone: str = Field(..., description="Origin Zone")
    origin_zip: int = Field(..., description="Origin Zip")
    destination_state: str = Field(..., description="Destination State")
    destination_zone: str = Field(..., description="Destination Zone")
    destination_zip: int = Field(..., description="Destination Zip")
    cubes: float = Field(..., description="Cubes")
    weight: int = Field(..., description="Weight")
    service_level: ServiceLevelEnum = Field(..., description="Level of Service")
    carrier: str = Field(..., description="Carrier")
    area_type: str = Field(..., description="Area Type")
    service_threshold_charges: float | str = Field(..., description="Threshold charges")
    service_white_glove_charges: float | str = Field(..., description="White Glove charges")
    service_doorstep_charges: float | str = Field(..., description="Doorstep charges")


class ShippingQuotesResponse(BaseModel):
    summary: ShippingQuotesSummary = Field(..., description="Shipping Summary")
    details: ShippingQuotesDetails = Field(..., description="Shipping Details")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "summary": {
                        "delivery_surcharge": 101.75,
                        "fuel_surcharge": 26.96,
                        "remote_charges": 0.0,
                        "outsource_charges": 0.0,
                        "total_charge": 128.71
                    },
                    "details": {
                        "origin_state": "CA",
                        "origin_zone": "Zone 2 L",
                        "origin_zip": 90210,
                        "destination_state": "CA",
                        "destination_zone": "Zone 2 L",
                        "destination_zip": 90211,
                        "cubes": 24.0,
                        "weight": 299,
                        "service_level": "Doorstep",
                        "carrier": "Metropolitan",
                        "area_type": "Standard Area",
                        "service_threshold_charges": 107.1,
                        "service_white_glove_charges": 182.7,
                        "service_doorstep_charges": 101.75
                    }
                }
            ]
        }
    }
