from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class DonorSchema(BaseModel):
    donor_id: Optional[int] = Field(None, description="Unique identifier for the donor")
    znumber: Optional[int] = Field(None, description="Unique Z number for the donor")
    name: Optional[str] = Field(None, max_length=100, description="Name of the donor")
    age: Optional[int] = Field(None, ge=0, description="Age of the donor")
    region: Optional[str] = Field(
        None, max_length=50, description="Region of the donor"
    )
    other_factors: Optional[dict] = Field(
        None, description="Additional factors related to the donor"
    )

    class Config:
        from_attributes = True
