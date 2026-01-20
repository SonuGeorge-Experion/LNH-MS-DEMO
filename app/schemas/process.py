from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProcessSchema(BaseModel):
    plan_id: Optional[int] = None
    workflow_id: Optional[int] = None
    donor_id: Optional[int] = None
    tissue_id: Optional[int] = None
    status: Optional[Literal["planned", "in_progress", "completed", "deviated"]] = (
        "planned"
    )
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WorkflowSchema(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=100)
    template_json: Optional[Dict[str, Any]] = None
    version: Optional[str] = Field(None, max_length=10)
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class WorkflowStepsSchema(BaseModel):
    process_id: Optional[int] = None
    step_num: Optional[int] = None
    initials: Optional[str] = None
    verified_by_initials: Optional[str] = None
    spin_program: Optional[str] = None
    spin_count: Optional[int] = None
    actual_duration: Optional[str] = None
    temp_start: Optional[Decimal] = None
    temp_stop: Optional[Decimal] = None
    temp_compliant: Optional[bool] = None
    na_performed: Optional[bool] = None
    deviation_notes: Optional[str] = None
    start_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # @field_validator("start_time", "completed_at", mode="before")
    # @classmethod
    # def parse_iso_datetime(cls, v):
    #     if v is None or isinstance(v, datetime):
    #         return v
    #     if isinstance(v, str):
    #         s = v.strip()
    #         # Support trailing 'Z' for UTC
    #         if s.endswith("Z"):
    #             s = s[:-1] + "+00:00"
    #         try:
    #             return datetime.fromisoformat(s)
    #         except Exception:
    #             raise ValueError(
    #                 "Invalid datetime format. Expected ISO 8601, e.g., 2024-01-31T13:45:00 or 2024-01-31T13:45:00+00:00"
    #             )
    #     raise ValueError("Invalid type for datetime field")

    @model_validator(mode="after")
    def validate_times(self):
        # completed_at requires start_time
        if self.completed_at is not None and self.start_time is None:
            raise ValueError("completed_at requires start_time to be set")
        # completed_at must be >= start_time when both are provided
        if (
            self.start_time is not None
            and self.completed_at is not None
            and self.completed_at < self.start_time
        ):
            raise ValueError("completed_at must be greater than or equal to start_time")
        return self

    model_config = ConfigDict(from_attributes=True)


class WorkflowStepIn(BaseModel):
    step_id: Optional[int] = None
    process_id: int
    step_num: int
    initials: Optional[str] = None
    verified_by_initials: Optional[str] = None
    spin_program: Optional[str] = None
    spin_count: Optional[int] = None
    actual_duration: Optional[str] = None
    # temp_start: condecimal(max_digits=5, decimal_places=2) | None = None
    temp_start: Decimal | None = Field(None, max_digits=5, decimal_places=2)
    temp_stop: Decimal | None = Field(None, max_digits=5, decimal_places=2)
    temp_compliant: Optional[bool] = None
    na_performed: Optional[bool] = None
    deviation_notes: Optional[str] = None
    start_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    step_data: Optional[Dict] = None


class WorkflowListStepsSchema(BaseModel):
    steps: List[WorkflowStepIn]
