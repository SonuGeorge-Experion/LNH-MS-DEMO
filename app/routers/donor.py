from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donor as donor_crud
from app.db.async_session import get_async_db
from app.schemas.donor import DonorSchema

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model = DonorSchema,
    # dependencies = [Depends(require_role("Super Admin"))],
)
async def add_donor(
    # request: DonorSchema = Body(examples=[]),
    request: DonorSchema,
    db: AsyncSession = Depends(get_async_db),
):

    try:
        donor_info = await donor_crud.add_donor(request, db)
        return {"resp": f"Donor {donor_info.name} has been created"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Donor already exists.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )
