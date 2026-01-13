import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Time,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum

from app.db.base_class import Base


class CleanRooms(Base):
    __tablename__ = "clean_rooms"
    __table_args__ = (
        CheckConstraint(
            "serial_number >= 1 AND serial_number <= 10",
            name="clean_rooms_serial_number_check",
        ),
        PrimaryKeyConstraint("room_id", name="clean_rooms_pkey"),
        UniqueConstraint("serial_number", name="clean_rooms_serial_number_key"),
    )

    room_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    serial_number: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "available",
            "sterilizing",
            "in_use",
            "maintenance",
            "sterilized",
            name="room_status_enum",
        ),
        server_default=text("'available'::room_status_enum"),
    )
    max_technicians: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("4")
    )
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    # room_assignments: Mapped[list['RoomAssignments']] = relationship('RoomAssignments', back_populates='room')
    # machines: Mapped[list['Machines']] = relationship('Machines', back_populates='machine_room')
    # materials: Mapped[list['Materials']] = relationship('Materials', back_populates='materials_room')
    # tracking_logs: Mapped[list['TrackingLogs']] = relationship('TrackingLogs', back_populates='room')


class RoomAssignments(Base):
    __tablename__ = "room_assignments"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"], ["processes.process_id"], name="fk_process_link"
        ),
        ForeignKeyConstraint(
            ["room_id"], ["clean_rooms.room_id"], name="room_assignments_room_id_fkey"
        ),
        ForeignKeyConstraint(
            ["shift_id"], ["shifts.shift_id"], name="room_assignments_shift_id_fkey"
        ),
        PrimaryKeyConstraint("assignment_id", name="room_assignments_pkey"),
        UniqueConstraint("process_id", name="room_assignments_process_id_key"),
        UniqueConstraint("room_id", "shift_id", name="unique_room_shift"),
    )

    assignment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    room_id: Mapped[Optional[int]] = mapped_column(Integer)
    shift_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )
    technician_count: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("0")
    )
    status: Mapped[Optional[str]] = mapped_column(
        Enum("pending", "active", "completed", name="assignment_status_enum"),
        server_default=text("'pending'::assignment_status_enum"),
    )
    target_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    queue_sequence: Mapped[Optional[int]] = mapped_column(Integer)
    download_status: Mapped[Optional[str]] = mapped_column(
        String(20), server_default=text("'pending'::character varying")
    )

    # processes: Mapped[list['Processes']] = relationship('Processes', foreign_keys='[Processes.room_assignment_id]', back_populates='room_assignment')
    # process: Mapped[Optional['Processes']] = relationship('Processes', foreign_keys=[process_id], back_populates='room_assignments')
    # room: Mapped[Optional['CleanRooms']] = relationship('CleanRooms', back_populates='room_assignments')
    # shift: Mapped[Optional['Shifts']] = relationship('Shifts', back_populates='room_assignments')
    # assignment_technicians: Mapped[list['AssignmentTechnicians']] = relationship('AssignmentTechnicians', back_populates='assignment')


class Shifts(Base):
    __tablename__ = "shifts"
    __table_args__ = (PrimaryKeyConstraint("shift_id", name="shifts_pkey"),)

    shift_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    # room_assignments: Mapped[list['RoomAssignments']] = relationship('RoomAssignments', back_populates='shift')
