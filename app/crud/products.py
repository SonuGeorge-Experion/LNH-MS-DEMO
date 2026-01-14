from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.models.products import TissueCategories, Tissues, Products
from app.schemas.products import TissueCategorySchema, TissuesSchema, ProductsSchema
from app.db.models.donor import Donors
from sqlalchemy import and_, cast, String, select
from typing import Optional, List
from datetime import datetime

async def add_tissue_category(db: AsyncSession, request:TissueCategorySchema):
    new_tissue_category = TissueCategories(
        category_id = request.category_id,
        name = request.name,
        num_products = request.num_products
    )

    db.add(new_tissue_category)
    await db.commit()
    await db.refresh(new_tissue_category)
    return new_tissue_category

async def add_tissue(db: AsyncSession, request: TissuesSchema):
    new_tissue = Tissues(
        tissue_id = request.tissue_id,
        donor_id = request.donor_id,
        category_id = request.category_id,
        bundle_details = request.bundle_details,
        status = request.status,
    )

    db.add(new_tissue)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        msg = "Failed to add tissue. Ensure donor_id and category_id reference existing records."
        raise ValueError(msg) from e

    await db.refresh(new_tissue)
    return new_tissue

async def add_product(db: AsyncSession, request: ProductsSchema):
    new_product = Products(
        product_id=request.product_id,
        name=request.name,
        category_id=request.category_id,
        base_dimensions=request.base_dimensions,
        is_active=request.is_active,
    )

    db.add(new_product)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        msg = "Failed to add product. Ensure category_id references an existing tissue category and name/PK are valid."
        raise ValueError(msg) from e

    await db.refresh(new_product)
    return new_product

async def get_tissues_list(
    db: AsyncSession,
    donor_ids: Optional[List[int]] = None,
    statuses: Optional[List[str]] = None,
    donor_search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 10
):
    query = select(
        Tissues,
        Donors.name.label("donor_name"),
        Donors.znumber.label("znumber"),
        TissueCategories.name.label("category_name")
    ).join(Donors, Tissues.donor_id == Donors.donor_id
    ).join(TissueCategories, Tissues.category_id == TissueCategories.category_id)

    filters = []

    # 1. Checkbox Filter: Multiple Donor IDs
    if donor_ids:
        filters.append(Tissues.donor_id.in_(donor_ids))

    # 2. Checkbox Filter: Multiple Statuses
    if statuses:
        filters.append(Tissues.status.in_(statuses))

    # 3. Search Functionality: Donor ID (partial match as string)
    if donor_search:
        filters.append(cast(Tissues.donor_id, String).ilike(f"%{donor_search}%"))

    # 4. Date Range Filter
    if start_date:
        filters.append(Tissues.created_at >= start_date)
    if end_date:
        filters.append(Tissues.created_at <= end_date)

    if filters:
        query = query.where(and_(*filters))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    
    # Process results to combine Join data into the response
    rows = result.all()
    tissues_data = []
    for row in rows:
        tissue_obj = row[0] # The Tissues model instance
        data = {
            **tissue_obj.__dict__,
            "donor_name": row.donor_name,
            "znumber": row.znumber,
            "category_name": row.category_name
        }
        tissues_data.append(data)
        
    return tissues_data