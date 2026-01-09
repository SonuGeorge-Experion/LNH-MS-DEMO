from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.production_plan import ProductionPlans
from app.schemas.production_plan import ProductionPlanSchema


async def create_production_plan(request: ProductionPlanSchema, db: AsyncSession):
    prod_plan = ProductionPlans(**request.model_dump())
    db.add(prod_plan)
    await db.commit()
    await db.refresh(prod_plan)
    return prod_plan
