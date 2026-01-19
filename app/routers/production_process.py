from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.production_plan import get_donor_production_plan_with_workflow
from app.db.async_session import get_async_db

router = APIRouter()


from fastapi import HTTPException


@router.post("/")
async def populate_production_process(
    donor_id: int, db: AsyncSession = Depends(get_async_db)
):
    """
    Docstring for populate_production_process

    :param donor_id: Donor Id
    :type donor_id: int
    :param db: DB Session
    :type db: AsyncSession

    Step 1: Get Tissues from Donor ID from Tissue Table
    Step 2: Get approved tissue details from production plan
    Step 3: Populate process details from production plan
    Step 3a: Populate workflow id based on tissue category
    """
    try:
        rows = await get_donor_production_plan_with_workflow(donor_id, db)
        return rows
    except Exception as e:
        # Optionally log the error here
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
