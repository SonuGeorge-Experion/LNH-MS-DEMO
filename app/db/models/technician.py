from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum

from app.db.base_class import Base


class Technicians(Base):
    __tablename__ = "technicians"
    __table_args__ = (
        PrimaryKeyConstraint("technician_id", name="technicians_pkey"),
        UniqueConstraint("user_id", name="technicians_user_id_key"),
    )

    technician_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    role: Mapped[Optional[str]] = mapped_column(
        Enum("technician", "supervisor", name="tech_role_enum"),
        server_default=text("'technician'::tech_role_enum"),
    )
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    # assignment_technicians: Mapped[list["AssignmentTechnicians"]] = relationship(
    #     "AssignmentTechnicians", back_populates="technician"
    # )
    # process_comments: Mapped[list["ProcessComments"]] = relationship(
    #     "ProcessComments", back_populates="user"
    # )
    # tracking_logs: Mapped[list["TrackingLogs"]] = relationship(
    #     "TrackingLogs", back_populates="user"
    # )
    # verifications: Mapped[list["Verifications"]] = relationship(
    #     "Verifications", back_populates="signed_by_user"
    # )


class AssignmentTechnicians(Base):
    __tablename__ = "assignment_technicians"
    __table_args__ = (
        ForeignKeyConstraint(
            ["assignment_id"],
            ["room_assignments.assignment_id"],
            name="assignment_technicians_assignment_id_fkey",
        ),
        ForeignKeyConstraint(
            ["technician_id"],
            ["technicians.technician_id"],
            name="assignment_technicians_technician_id_fkey",
        ),
        PrimaryKeyConstraint("assign_tech_id", name="assignment_technicians_pkey"),
        UniqueConstraint("assignment_id", "technician_id", name="unique_assign_tech"),
    )

    assign_tech_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assignment_id: Mapped[Optional[int]] = mapped_column(Integer)
    technician_id: Mapped[Optional[int]] = mapped_column(Integer)

    # assignment: Mapped[Optional["RoomAssignments"]] = relationship(
    #     "RoomAssignments", back_populates="assignment_technicians"
    # )
    # technician: Mapped[Optional["Technicians"]] = relationship(
    #     "Technicians", back_populates="assignment_technicians"
    # )
