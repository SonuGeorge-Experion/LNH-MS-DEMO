import datetime
import decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


# class TimestampMixin:
#     created_at = Column(DateTime, default=func.now(), nullable=False)
#     updated_at = Column(
#         DateTime, default=func.now(), onupdate=func.now(), nullable=False
#     )
