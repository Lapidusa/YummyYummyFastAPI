from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time
from uuid import UUID
from shapely.geometry import Polygon

from app.schemas.category import Category
from app.schemas.city import City

class PolygonCoordinates(BaseModel):
  type: str = Field("Polygon", description="Type of the geometry")
  coordinates: List[List[List[float]]] = Field(..., description="Coordinates of the polygon")

class Store(BaseModel):
  id: UUID = Field(..., description="Unique store identifier")  # Unique store identifier
  address: str = Field(..., description="Store address")  # Store address
  start_working_hours: time = Field(..., description="Start of working hours")  # Start of working hours
  end_working_hours: time = Field(..., description="End of working hours")  # End of working hours
  start_delivery_time: time = Field(..., description="Start of delivery time")  # Start of delivery time
  end_delivery_time: time = Field(..., description="End of delivery time")  # End of delivery time
  phone_number: str = Field(..., description="Store phone number")  # Store phone number
  area: PolygonCoordinates = Field(..., description="Geographical area of the store as a polygon")
  categories: List[Category] = Field(default_factory=list, description="List of related categories")  # Related categories
  city: City = Field(..., description="City associated with the store")  # City associated with the store
  min_order_price: int = Field(..., description="Minimum order price")
  class Config:
    arbitrary_types_allowed = True  # Allow arbitrary types

class CreateStore(BaseModel):
  address: str
  start_working_hours: time
  end_working_hours: time
  start_delivery_time: time
  end_delivery_time: time
  phone_number: str
  area: PolygonCoordinates = Field(..., description="Geographical area of the store as a polygon")
  min_order_price: int = Field(..., description="Minimum order price")

  class Config:
    arbitrary_types_allowed = True  # Allow arbitrary types

class UpdateStore(BaseModel):
  id: UUID
  address: str
  start_working_hours: time
  end_working_hours: time
  start_delivery_time: time
  end_delivery_time: time
  phone_number: str
  area: PolygonCoordinates = Field(..., description="Geographical area of the store as a polygon")
  min_order_price: int = Field(..., description="Minimum order price")

  class Config:
    arbitrary_types_allowed = True  # Allow arbitrary types