from pydantic import BaseModel, Field
from typing import Optional
import enum
from datetime import datetime, date, time

sampleAddCleanRoom = {
    "name": "Room 1 (Bone)",
    "serial_number": 1,
    "status": "in_use",
    "max_technicians": 4,
    "is_active": True,
}

sampleAddRoomAssignment = {
    "process_id": 5001,
    "room_id": 1,
    "shift_id": 1,
    "assigned_at": "2026-01-08 06:01:49.914942",
    "technician_count": 0,
    "status": "pending",
    "target_date": "2026-01-08",
    "queue_sequence": "",
    "download_status": "",
}

sampleAddShift = {
    "name": "Morning",
    "start_time": "06:00:00",
    "end_time": "14:30:00",
}


class ErrorResp(BaseModel):
    detail: str


class Status(str, enum.Enum):
    AVAILABLE = "available"
    STERILIZING = "sterilizing"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    STERILIZED = "sterilized"


class AssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class CleanRoomsSchema(BaseModel):
    # room_id: int
    name: str = Field(..., max_length=50)
    serial_number: Optional[int] = None
    status: Optional[Status] = Status.AVAILABLE
    max_technicians: Optional[int] = 4
    is_active: Optional[bool] = True


class CleanRoomsCreateResp(CleanRoomsSchema):
    room_id: int


class RoomAssignmentsSchema(BaseModel):
    # assignment_id: int
    process_id: Optional[int] = None
    room_id: Optional[int] = None
    shift_id: Optional[int] = None
    assigned_at: Optional[datetime] = None
    technician_count: Optional[int] = 0
    status: Optional[AssignmentStatus] = AssignmentStatus.PENDING
    target_date: Optional[date] = None
    queue_sequence: Optional[int] = None
    download_status: Optional[str] = Field("pending", max_length=20)


class ShiftsSchema(BaseModel):
    # shift_id: int
    name: str = Field(..., max_length=50)
    start_time: time = None
    end_time: time = None
