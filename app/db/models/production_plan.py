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


class ProductionPlans(Base):
    __tablename__ = "production_plans"
    __table_args__ = (
        ForeignKeyConstraint(
            ["product_id"],
            ["products.product_id"],
            name="production_plans_product_id_fkey",
        ),
        ForeignKeyConstraint(
            ["tissue_id"], ["tissues.tissue_id"], name="production_plans_tissue_id_fkey"
        ),
        PrimaryKeyConstraint("plan_id", name="production_plans_pkey"),
    )

    plan_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tissue_id: Mapped[Optional[int]] = mapped_column(Integer)
    product_id: Mapped[Optional[int]] = mapped_column(Integer)
    planned_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(
        Enum("draft", "approved", "executing", name="plan_status_enum"),
        server_default=text("'draft'::plan_status_enum"),
    )
    priority: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("0"))
    comments: Mapped[Optional[str]] = mapped_column(String(255))

    # processes: Mapped[list["Processes"]] = relationship(
    #     "Processes", back_populates="plan"
    # )
    # product: Mapped[Optional["Products"]] = relationship(
    #     "Products", back_populates="production_plans"
    # )
    # tissue: Mapped[Optional["Tissues"]] = relationship(
    #     "Tissues", back_populates="production_plans"
    # )
