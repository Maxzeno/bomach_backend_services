from ninja import Schema
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PropertyIn(Schema):
    name: str
    property_type: str
    category: str
    location: str
    price: Decimal
    size: Decimal
    bedrooms: int = 0
    bathrooms: int = 0
    parking_spaces: int = 0
    description: Optional[str] = ""
    status: str = "available"
    client_id: Optional[str] = None


class PropertyUpdate(Schema):
    name: Optional[str] = None
    property_type: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    price: Optional[Decimal] = None
    size: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    parking_spaces: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None
    client_id: Optional[str] = None


class PropertyOut(Schema):
    id: int
    name: str
    property_type: str
    category: str
    location: str
    price: Decimal
    size: Decimal
    bedrooms: int
    bathrooms: int
    parking_spaces: int
    description: str
    status: str
    client_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class PropertyStatsOut(Schema):
    total_properties: int
    available: int
    reserved: int
    sold_rented: int
    for_sale: int
    for_rent: int
    for_lease: int
