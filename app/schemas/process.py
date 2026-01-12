from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


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

    model_config = ConfigDict(from_attributes=True)
