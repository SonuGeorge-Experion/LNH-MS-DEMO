from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.models.products import TissueCategories, Tissues, Products
from app.schemas.products import TissueCategorySchema, TissuesSchema, ProductsSchema

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