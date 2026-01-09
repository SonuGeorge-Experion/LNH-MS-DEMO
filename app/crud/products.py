from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.products import TissueCategories
from app.schemas.products import TissueCategorySchema

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