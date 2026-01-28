import enum
from typing import Optional

from pydantic import BaseModel, Field

from app.db.models.resources import MachineTypeEnum, MachineStatusEnum


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

class MachineSchema(BaseModel):
    name: str = Field(..., description="Name of the machine")
    type: Optional[MachineTypeEnum] = Field(None, description="Type of machine (e.g., centrifuge, ultrasonic)")
    programs: Optional[list[dict]] = Field(None, description="Programs configuration for the machine")
    scancode: Optional[str] = Field(None, description="Scannable code for the machine")
    machine_room_id: Optional[int] = Field(None, description="Associated clean room id for the machine")
    status: Optional[MachineStatusEnum] = Field(None, description="Status of the machine (available, in_use, maintenance)")

    class Config:
        from_attributes = True


class MachineSchemaCreate(MachineSchema):
    pass


class MachineSchemaOut(MachineSchema):
    machine_id: Optional[int] = Field(None, description="Unique identifier for machine")
    pass
