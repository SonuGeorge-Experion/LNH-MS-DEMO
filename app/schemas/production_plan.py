from typing import Literal, Optional

from pydantic import BaseModel, Field


class ProductionPlanSchema(BaseModel):
    tissue_id: int = Field(..., description="Associated tissue ID")
    product_id: int = Field(..., description="Associated product ID")
    planned_quantity: int = Field(..., description="Planned quantity of product")
    status: Literal["draft", "approved", "executing"] = Field(
        default="draft", description="Status of the plan"
    )
    priority: Optional[int] = Field(default=0, description="Priority level of the plan")
    comments: Optional[str] = Field(
        default=None, max_length=255, description="Optional comments"
    )

    model_config = {
        "from_attributes": True,  # allows ORM mode in Pydantic v2
    }


class ProductionPlanSchemaOut(ProductionPlanSchema):
    plan_id: int = Field(..., description="Unique identifier for the plan")
    product_name: Optional[str] = Field(None, description="Name of the product")
    product_base_dimensions: Optional[dict] = Field(None, description="Base dimensions of the product")
    category_name: Optional[str] = Field(None, description="Name of the tissue category")
    tissue_type: Optional[str] = Field(None, description="Type of tissue from bundle details")
