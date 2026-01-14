from typing import Optional

from pydantic import BaseModel, Field


class MaterialSchema(BaseModel):
    name: str = Field(..., description="Name of the material")
    scancode: Optional[str] = Field(None, description="Scannable code for the material")
    quantity_available: Optional[int] = Field(0, description="Available quantity of the material")
    materials_room_id: Optional[int] = Field(None, description="Associated clean room id for the material")
    unit: Optional[str] = Field(None, description="Measurement unit for the material (e.g., ml, g, units)")

    class Config:
        from_attributes = True

class MaterialSchemaCreate(MaterialSchema):
    pass

class MaterialSchemaOut(MaterialSchema):
    material_id: Optional[int] = Field(None, description="Unique identifier for material")
    pass
