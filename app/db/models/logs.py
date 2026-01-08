import datetime
import decimal
from typing import Optional, Text

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


class TrackingLogs(Base):
    __tablename__ = "tracking_logs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["room_id"], ["clean_rooms.room_id"], name="tracking_logs_room_id_fkey"
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["technicians.technician_id"],
            name="tracking_logs_user_id_fkey",
        ),
        PrimaryKeyConstraint("log_id", name="tracking_logs_pkey"),
    )

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[Optional[str]] = mapped_column(
        Enum("tissue", "process", "plan", name="entity_type_enum")
    )
    entity_id: Mapped[Optional[int]] = mapped_column(Integer)
    event_type: Mapped[Optional[str]] = mapped_column(
        Enum(
            "collected",
            "planned",
            "step_completed",
            "deviated",
            "movement",
            "verification",
            name="event_type_enum",
        )
    )
    room_id: Mapped[Optional[int]] = mapped_column(Integer)
    details: Mapped[Optional[dict]] = mapped_column(JSONB)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    # room: Mapped[Optional["CleanRooms"]] = relationship(
    #     "CleanRooms", back_populates="tracking_logs"
    # )
    # user: Mapped[Optional["Technicians"]] = relationship(
    #     "Technicians", back_populates="tracking_logs"
    # )
