import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Donors(Base):
    __tablename__ = "donors"
    __table_args__ = (
        PrimaryKeyConstraint("donor_id", name="donors_pkey"),
        UniqueConstraint("znumber", name="donors_znumber_key"),
    )

    donor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    znumber: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    region: Mapped[Optional[str]] = mapped_column(String(50))
    other_factors: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    # processes: Mapped[list['Processes']] = relationship('Processes', back_populates='donor')
    # tissues: Mapped[list['Tissues']] = relationship('Tissues', back_populates='donor')
