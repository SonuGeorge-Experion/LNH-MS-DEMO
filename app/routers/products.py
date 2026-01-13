from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import products as product_crud
from app.db.async_session import get_async_db
from app.schemas.products import TissueCategorySchema, TissuesSchema
from typing import List
router = APIRouter()


@router.post(
    "/tissue_category",
    status_code=status.HTTP_201_CREATED,
    # response_model = TissueCategorySchema,
    # dependencies = [Depends(require_role("Super Admin"))],
)
async def add_tissue_category(
    # request: TissueCategorySchema = Body(examples=[]),
    request: TissueCategorySchema,
    db: AsyncSession = Depends(get_async_db),
):

    try:
        category_info = await product_crud.add_tissue_category(db, request)
        return {"resp": f"Tissue Category {category_info.name} has been created"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tissue Category already exists.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.post(
    "/tissue",
    status_code=status.HTTP_201_CREATED,
)
async def add_tissue(
    request: TissuesSchema,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        tissue = await product_crud.add_tissue(db, request)
        return {"resp": f"Tissue {tissue.tissue_id} has been created"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Integrity constraint violated while creating tissue.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )