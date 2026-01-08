from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donor as donor_crud
from app.db.async_session import get_async_db
from app.schemas.donor import DonorSchema
from typing import List
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

@router.get("/", 
            status_code= status.HTTP_200_OK,
            response_model=List[DonorSchema])
async def read_donors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    try:
        donors = await donor_crud.get_donors(db, skip=skip, limit=limit)
        return donors
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    
@router.put("/{donor_id}",
            status_code= status.HTTP_200_OK,
            response_model=DonorSchema)
async def update_donor_api(
    donor_id: int, 
    donor_in: DonorSchema, 
    db: AsyncSession = Depends(get_async_db)
):
    try:
        updated_record = await donor_crud.update_donor(db, donor_id, donor_in)
        
        if not updated_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Donor with ID {donor_id} not found"
            )
            
        return updated_record

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )