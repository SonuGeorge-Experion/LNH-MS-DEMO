from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import production_plan as prod_plan_crud
from app.db.async_session import get_async_db
from app.schemas.production_plan import ProductionPlanSchema, ProductionPlanSchemaOut

router = APIRouter()


@router.post(
    "/plan/",
    status_code=status.HTTP_201_CREATED,
)
async def create_production_plan(
    request: ProductionPlanSchema, db: AsyncSession = Depends(get_async_db)
):
    try:
        product_plan_info = await prod_plan_crud.create_production_plan(request, db)
        return {"resp": f"New Product plan created {product_plan_info.plan_id}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )

@router.get(
    "/plans",
    status_code=status.HTTP_200_OK,
    response_model=List[ProductionPlanSchemaOut],
)
async def list_production_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    production_plan_status: Optional[str] = Query(None),
    donor_ids: Optional[List[int]] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        plans = await prod_plan_crud.list_production_plans(
            db, skip=skip, limit=limit, status=production_plan_status, donor_ids=donor_ids
        )
        return plans
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )