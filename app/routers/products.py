from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
# from app.crud.products import Tissues as crud_tissues
from app.crud import products as product_crud
from app.db.async_session import get_async_db
from app.schemas.products import TissueCategorySchema, TissuesSchema, ProductsSchema, ListTissuesSchema, TissueStatus, ListProductsSchema
from typing import List, Optional, Annotated
from datetime import datetime

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
    
@router.post( 
        "/product", 
        status_code=status.HTTP_201_CREATED, 
) 
async def add_product( 
    request: ProductsSchema, 
    db: AsyncSession = Depends(get_async_db), 
): 
    try: 
        product = await product_crud.add_product(db, request) 
        return {"resp": f"Product {product.product_id} has been created"} 
    except ValueError as e: 
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=str(e), ) 
    except IntegrityError: 
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="Integrity constraint violated while creating product.", ) 
    except Exception as e: 
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error Occurred. Please try later. {e}", )
    
@router.get(
        "/", 
        response_model=List[ListTissuesSchema],
        status_code=status.HTTP_200_OK
)
async def read_tissues(
    # Multi-select filters (Checkboxes)
    donor_ids: Optional[List[int]] = Query(None, description="Select multiple Donor IDs"),
    statuses: Optional[List[TissueStatus]] = Query([], description="Select multiple statuses"),
    
    # Search and Date Range
    donor_search: Optional[str] = Query(None, description="Search by Donor ID string"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_async_db)
):
    try:
        tissues = await product_crud.get_tissues_list(
            db, 
            donor_ids=donor_ids, 
            statuses=statuses, 
            donor_search=donor_search,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        return tissues
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tissues: {str(e)}"
        )

@router.get(
    "/products",
    response_model=List[ListProductsSchema],
    status_code=status.HTTP_200_OK,
)
async def list_products(
    category_ids: Optional[List[int]] = Query(None, description="Filter by multiple category IDs"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        products = await product_crud.get_products_list(
            db,
            category_ids=category_ids,
            skip=skip,
            limit=limit,
        )
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}",
        )