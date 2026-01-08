from typing import Optional

from sqlalchemy import (
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


class Machines(Base):
    __tablename__ = "machines"
    __table_args__ = (
        ForeignKeyConstraint(
            ["machine_room_id"],
            ["clean_rooms.room_id"],
            name="machines_machine_room_id_fkey",
        ),
        PrimaryKeyConstraint("machine_id", name="machines_pkey"),
        UniqueConstraint("scancode", name="machines_scancode_key"),
    )

    machine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(
        Enum("centrifuge", "ultrasonic", name="machine_type_enum")
    )
    programs: Mapped[Optional[dict]] = mapped_column(JSONB)
    scancode: Mapped[Optional[str]] = mapped_column(String(50))
    machine_room_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(
        Enum("available", "in_use", "maintenance", name="machine_status_enum"),
        server_default=text("'available'::machine_status_enum"),
    )

    # machine_room: Mapped[Optional["CleanRooms"]] = relationship(
    #     "CleanRooms", back_populates="machines"
    # )


class Materials(Base):
    __tablename__ = "materials"
    __table_args__ = (
        ForeignKeyConstraint(
            ["materials_room_id"],
            ["clean_rooms.room_id"],
            name="materials_materials_room_id_fkey",
        ),
        PrimaryKeyConstraint("material_id", name="materials_pkey"),
        UniqueConstraint("scancode", name="materials_scancode_key"),
    )

    material_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    scancode: Mapped[Optional[str]] = mapped_column(String(50))
    quantity_available: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("0")
    )
    materials_room_id: Mapped[Optional[int]] = mapped_column(Integer)
    unit: Mapped[Optional[str]] = mapped_column(String(20))

    # materials_room: Mapped[Optional['CleanRooms']] = relationship('CleanRooms', back_populates='materials')
