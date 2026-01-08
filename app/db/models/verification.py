import datetime
from typing import Optional, Text
from unicodedata import decimal

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


class Verifications(Base):
    __tablename__ = "verifications"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"],
            ["processes.process_id"],
            name="verifications_process_id_fkey",
        ),
        ForeignKeyConstraint(
            ["signed_by_user_id"],
            ["technicians.technician_id"],
            name="verifications_signed_by_user_id_fkey",
        ),
        PrimaryKeyConstraint("verif_id", name="verifications_pkey"),
    )

    verif_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    role_type: Mapped[Optional[str]] = mapped_column(String(20))
    signed_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    signature_data: Mapped[Optional[str]] = mapped_column(Text)
    signed_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    # process: Mapped[Optional["Processes"]] = relationship(
    #     "Processes", back_populates="verifications"
    # )
    # signed_by_user: Mapped[Optional["Technicians"]] = relationship(
    #     "Technicians", back_populates="verifications"
    # )
