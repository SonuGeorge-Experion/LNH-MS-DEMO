from typing import Optional

from pydantic import BaseModel, Field

class TissueCategorySchema(BaseModel):
    category_id: int = Field(None, description="Unique identifier for category")
    name: str = Field (None, description="Name of the tissue category")
    num_products: Optional[int] = Field(None, description="Number of products")

    class Config:
        from_attributes = True