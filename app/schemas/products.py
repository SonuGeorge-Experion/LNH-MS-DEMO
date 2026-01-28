from typing import Optional

from pydantic import BaseModel, Field
from enum import Enum

class TissueCategorySchema(BaseModel):
    category_id: int = Field(None, description="Unique identifier for category")
    name: str = Field (None, description="Name of the tissue category")
    num_products: Optional[int] = Field(None, description="Number of products")

    class Config:
        from_attributes = True
class TissueStatus(str, Enum):
    collected = "collected"
    planned = "planned"
    processed = "processed"
    discarded = "discarded"

class TissuesSchema(BaseModel):
    tissue_id: int = Field(None, description="Unique identifier for tissue")
    donor_id: Optional[int] = Field(None, description="Identifier for the donor")
    category_id: Optional[int] = Field(None, description="Category of the tissue")
    bundle_details: Optional[dict] = Field(None, description="Bundle details of the tissue")
    status: Optional[str] = Field(None, description="Status of the tissue")

    class Config:
        from_attributes = True

class ProductsSchema(BaseModel):
    product_id: int = Field(None, description="Unique identifier for product")
    name: str = Field(None, description="Name of the product", max_length=100)
    category_id: Optional[int] = Field(None, description="Category of the product")
    base_dimensions: Optional[dict] = Field(None, description="Base dimensions JSON")
    is_active: Optional[bool] = Field(True, description="Whether the product is active")

    class Config:
        from_attributes = True

class ListTissuesSchema (TissuesSchema):
    donor_name: Optional[str]
    znumber: Optional[int]
    category_name: Optional[str]

    class Config:
        from_attributes = True

class ListProductsSchema (ProductsSchema):
    category_name: Optional[str]

    class Config:
        from_attributes = True