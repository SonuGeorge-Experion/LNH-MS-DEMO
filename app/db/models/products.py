import datetime
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


class TissueCategories(Base):
    __tablename__ = "tissue_categories"
    __table_args__ = (
        PrimaryKeyConstraint("category_id", name="tissue_categories_pkey"),
        UniqueConstraint("name", name="tissue_categories_name_key"),
    )

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    num_products: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text("0")
    )

    # products: Mapped[list["Products"]] = relationship(
    #     "Products", back_populates="category"
    # )
    # tissues: Mapped[list["Tissues"]] = relationship(
    #     "Tissues", back_populates="category"
    # )
    # workflows: Mapped[list["Workflows"]] = relationship(
    #     "Workflows", back_populates="category"
    # )


class Tissues(Base):
    __tablename__ = "tissues"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["tissue_categories.category_id"],
            name="tissues_category_id_fkey",
        ),
        ForeignKeyConstraint(
            ["donor_id"], ["donors.donor_id"], name="tissues_donor_id_fkey"
        ),
        PrimaryKeyConstraint("tissue_id", name="tissues_pkey"),
    )

    tissue_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    donor_id: Mapped[Optional[int]] = mapped_column(Integer)
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    bundle_details: Mapped[Optional[dict]] = mapped_column(JSONB)
    status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "collected", "planned", "processed", "discarded", name="tissue_status_enum"
        ),
        server_default=text("'collected'::tissue_status_enum"),
    )
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    # processes: Mapped[list["Processes"]] = relationship(
    #     "Processes", back_populates="tissue"
    # )
    # category: Mapped[Optional["TissueCategories"]] = relationship(
    #     "TissueCategories", back_populates="tissues"
    # )
    # donor: Mapped[Optional["Donors"]] = relationship("Donors", back_populates="tissues")
    # production_plans: Mapped[list["ProductionPlans"]] = relationship(
    #     "ProductionPlans", back_populates="tissue"
    # )


class Products(Base):
    __tablename__ = "products"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["tissue_categories.category_id"],
            name="products_category_id_fkey",
        ),
        PrimaryKeyConstraint("product_id", name="products_pkey"),
    )

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    base_dimensions: Mapped[Optional[dict]] = mapped_column(JSONB)
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    # category: Mapped[Optional["TissueCategories"]] = relationship(
    #     "TissueCategories", back_populates="products"
    # )
    # production_plans: Mapped[list["ProductionPlans"]] = relationship(
    #     "ProductionPlans", back_populates="product"
    # )
